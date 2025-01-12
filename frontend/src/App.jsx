import React, { useState } from "react";
import axios from "axios";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setSuccessMessage(""); // Clear success message
    setErrorMessage(""); // Clear any error message
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      setErrorMessage("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://localhost:8000/predict/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      const prediction = response.data.prediction;

      // Log prediction to console
      console.log(`Prediction: ${prediction}`);

      // Check if the prediction contains the word "mask"
      if (prediction.toLowerCase().includes("mask")) {
        setSuccessMessage("Mask detected successfully!");
      } else {
        setSuccessMessage("No mask detected.");
      }

      setErrorMessage(""); // Clear any error message on success
    } catch (error) {
      console.error("Error:", error.message);
      setErrorMessage("An error occurred while processing the file.");
      setSuccessMessage(""); // Clear success message on error
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Face Mask Detection</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload and Detect</button>
      </form>
      {successMessage && <h3 style={{ color: "green" }}>{successMessage}</h3>}
      {errorMessage && <h3 style={{ color: "red" }}>{errorMessage}</h3>}
    </div>
  );
}

export default App;
