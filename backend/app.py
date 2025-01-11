# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from PIL import Image
# import io
# from ultralytics import YOLO  # Import YOLO from ultralytics
# import torch
# from torchvision import transforms

# from PIL import Image

# img = Image.open('./test1 (3).jpg')
# img.show()  # Display the image to confirm its contents


# # Load the PyTorch model using YOLO
# model_path = "./best (2).pt"  # Replace with the correct path to your model file
# model = YOLO(model_path)  # Load the YOLO model

# # Define labels for the model's output (assuming a binary classification, adjust as needed)
# labels = {0: "No Mask", 1: "Mask"}  # Adjust based on your model's configuration

# # Define image preprocessing (standardize if needed)
# preprocess = transforms.Compose([
#     transforms.Resize((416, 416)),  # Resize to a size that YOLO expects
#     transforms.ToTensor(),  # Convert to tensor
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Normalize
# ])



# # Initialize FastAPI app
# app = FastAPI()

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Allow multiple frontend origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Endpoint for prediction
# @app.post("/predict/")
# async def predict(file: UploadFile = File(...)):
#     try:
#         # Log the file upload
#         print(f"Received file: {file.filename}")

#         # Load and validate the image
#         try:
#             image = Image.open(io.BytesIO(await file.read()))
#             if image.mode != "RGB":
#                 image = image.convert("RGB")
#         except Exception as img_error:
#             print(f"Error loading image: {img_error}")
#             return JSONResponse({"error": "Invalid image file."}, status_code=400)

#         # Preprocess the image
#         input_tensor = preprocess(image).unsqueeze(0)  # Add batch dimension

#         # Predict using the YOLO model
#         with torch.no_grad():
#             results = model(input_tensor)  # Predict using the YOLO model
#             print(f"Results: {results}")

#         # Check if any detection was made
#         if len(results) == 0 or len(results[0].boxes) == 0:
#             return JSONResponse({"error": "No objects detected in the image."}, status_code=400)

#         # Get the first detected object's class index
#         predicted_class = results[0].boxes.cls[0].item()  # Access the class index of the first box
#         predicted_class_name = results[0].names[predicted_class]  # Access the name of the class

#         # Validate class index
#         if predicted_class not in labels:
#             print(f"Unexpected class index: {predicted_class}")
#             return JSONResponse({"error": "Unexpected prediction result."}, status_code=500)

#         # Create prediction message
#         prediction_message = (
#             f"Prediction: {predicted_class_name}. The person is "
#             + ("wearing a mask." if predicted_class == 1 else "not wearing a mask.")
#         )

#         # Log prediction
#         print(f"Prediction: {prediction_message}")

#         # Return the prediction as a JSON response
#         return JSONResponse({"prediction": prediction_message})

#     except Exception as e:
#         # Log error details and return error message
#         print(f"Error during prediction: {e}")
#         return JSONResponse({"error": "An unexpected error occurred during prediction."}, status_code=500)




from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image, UnidentifiedImageError
import io

# Load pre-trained model and processor
model_name = "facebook/deit-base-distilled-patch16-224"
processor = AutoImageProcessor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)

# FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint for prediction
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Log the file upload
        print(f"Received file: {file.filename}")

        # Check file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Uploaded file is not an image.")

        # Load and process the image
        try:
            image = Image.open(io.BytesIO(await file.read()))
            inputs = processor(images=image, return_tensors="pt")
        except UnidentifiedImageError:
            raise HTTPException(status_code=400, detail="Invalid image file.")

        # Predict using the model
        outputs = model(**inputs)
        predicted_class = outputs.logits.argmax(-1).item()

        # Dynamically fetch labels from model config
        labels = list(model.config.id2label.values())
        if predicted_class >= len(labels):
            raise ValueError("Predicted class index out of range.")

        prediction = labels[predicted_class]

        # Log prediction
        print(f"Prediction: {prediction}")

        return JSONResponse({"prediction": prediction})
    except HTTPException as e:
        print(f"HTTP Error: {e.detail}")
        return JSONResponse({"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        # Log unexpected errors
        print(f"Error during prediction: {e}")
        return JSONResponse({"error": "An unexpected error occurred."}, status_code=500)























































