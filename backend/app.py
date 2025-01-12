




from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image, UnidentifiedImageError
import io
import serial  # For serial communication with Arduino

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

# Arduino serial connection (update the port and baudrate as per your setup)
try:
    arduino = serial.Serial(port="COM7", baudrate=9600, timeout=1)
    print("Connected to Arduino on COM7")
except Exception as e:
    print(f"Error connecting to Arduino: {e}")
    arduino = None

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

        # Check if prediction contains the word 'mask'
        if "mask" in prediction.lower():
            arduino_message = "Mask detected successfully"
        else:
            arduino_message = "No mask detected"

        # Send the result to Arduino
        if arduino and arduino.is_open:
            arduino.write(f"{arduino_message}\n".encode())
            print(f"Sent to Arduino: {arduino_message}")
        else:
            print("Arduino is not connected. Skipping message sending.")

        return JSONResponse({"prediction": prediction})
    except HTTPException as e:
        print(f"HTTP Error: {e.detail}")
        return JSONResponse({"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        # Log unexpected errors
        print(f"Error during prediction: {e}")
        return JSONResponse({"error": "An unexpected error occurred."}, status_code=500)

# Endpoint to send messages to Arduino
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

        # Check if prediction contains the word 'mask'
        if "mask" in prediction.lower():
            arduino_message = "Mask detected"
        else:
            arduino_message = "No mask detected"

        # Send the result to Arduino
        if arduino and arduino.is_open:
            arduino.write(f"{arduino_message}\n".encode())
            print(f"Sent to Arduino: {arduino_message}")
        else:
            print("Arduino is not connected. Skipping message sending.")

        return JSONResponse({"prediction": prediction})
    except HTTPException as e:
        print(f"HTTP Error: {e.detail}")
        return JSONResponse({"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        # Log unexpected errors
        print(f"Error during prediction: {e}")
        return JSONResponse({"error": "An unexpected error occurred."}, status_code=500)
