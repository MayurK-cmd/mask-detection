import React, { useState } from "react";
import axios from "axios";
import "./App.css"; // Ensure the CSS file with the dark theme is imported

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isMaskDetected, setIsMaskDetected] = useState(null); // New state to track mask detection

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setSuccessMessage("");
    setErrorMessage("");
    setIsMaskDetected(null); // Reset mask detection state
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

      console.log(`Prediction: ${prediction}`);

      if (prediction.toLowerCase().includes("mask")) {
        setSuccessMessage("Mask detected successfully!");
        setIsMaskDetected(true);
      } else {
        setSuccessMessage("No mask detected.");
        setIsMaskDetected(false);
      }

      setErrorMessage("");
    } catch (error) {
      console.error("Error:", error.message);
      setErrorMessage("An error occurred while processing the file.");
      setSuccessMessage("");
      setIsMaskDetected(null);
    }
  };

  return (
    <div>
      <h1>Face Mask Detection</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload and Detect</button>
      </form>
      {successMessage && (
        <h3 style={{ color: isMaskDetected === false ? "red" : "green" }}>
          {successMessage}
        </h3>
      )}
      {errorMessage && <h3 style={{ color: "red" }}>{errorMessage}</h3>}
    </div>
  );
}

export default App;
