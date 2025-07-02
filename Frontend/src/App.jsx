// App.jsx

import React, { useState, useEffect } from "react";
import PredictionCard from "./components/PredictionCard";
import { PhotographIcon } from "@heroicons/react/outline";

const App = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview);
    };
  }, [preview]);

  const handleFile = (file) => {
    setFile(file);
    setPreview(URL.createObjectURL(file));
    setPrediction(null);
    setError(null);
  };

  const handleFileChange = (e) => {
    if (e.target.files[0]) handleFile(e.target.files[0]);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
  };

  const handleDragOver = (e) => e.preventDefault();

  const handleSubmit = async () => {
    if (!file) return;
    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Prediction failed");
      const data = await res.json();
      setPrediction(data);
    } catch (err) {
      console.error(err);
      setError(
        "Oops! Something went wrong. Is your backend running and reachable?"
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-50 via-white to-indigo-50 flex flex-col">
      {/* Header */}
      <header className="bg-gradient-to-r from-indigo-600 to-teal-500 text-white py-8 shadow-md">
        <div className="max-w-3xl mx-auto text-center px-4">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight">
            Fish Species Classifier
          </h1>
          <p className="mt-2 text-lg opacity-90">
            Upload an underwater shot and let AI identify your catch.
          </p>
        </div>
      </header>

      <main className="flex-grow container mx-auto px-4 py-12">
        {/* Drop Zone */}
        <div
          className={`relative group border-4 ${
            file ? "border-teal-400 bg-teal-50" : "border-gray-300 bg-white"
          } border-dashed rounded-2xl p-12 flex flex-col items-center justify-center transition-all hover:border-indigo-500 hover:bg-indigo-50 cursor-pointer`}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={() => document.getElementById("fileInput").click()}
        >
          <input
            id="fileInput"
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="hidden"
          />
          <p className="text-gray-600 text-center">
            {file
              ? file.name
              : "Drag & drop an image here, or click to select one"}
          </p>
          {/* subtle glow */}
          <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-30 bg-gradient-to-r from-indigo-200 to-teal-200 transition-opacity pointer-events-none" />
        </div>

        {/* Preview */}
        {preview && (
          <div className="mt-8 flex justify-center">
            <div className="w-32 h-32 rounded-xl overflow-hidden shadow-lg bg-white ring-1 ring-gray-200">
              <img
                src={preview}
                alt="Preview"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        )}

        {/* Action Button */}
        <div className="mt-10 flex justify-center">
          <button
            onClick={handleSubmit}
            disabled={!file || isLoading}
            className={`flex items-center space-x-2 px-8 py-3 rounded-full font-semibold text-white shadow-md transition ${
              !file || isLoading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-indigo-600 hover:bg-indigo-700"
            }`}
          >
            {isLoading && (
              <svg
                className="animate-spin h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8v8H4z"
                />
              </svg>
            )}
            <span>{isLoading ? "Analyzing..." : "Identify Fish Species"}</span>
          </button>
        </div>

        {/* Error */}
        {error && (
          <div className="mt-6 max-w-md mx-auto bg-red-50 border border-red-300 text-red-800 p-4 rounded-lg shadow-sm">
            {error}
          </div>
        )}

        {/* Prediction */}
        {prediction && (
          <div className="mt-8 max-w-2xl mx-auto">
            <PredictionCard prediction={prediction} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white py-6 text-center text-gray-500 text-sm ring-t ring-gray-200">
        © {new Date().getFullYear()} MarineAI Labs. All rights reserved.
      </footer>
    </div>
  );
};

export default App;
