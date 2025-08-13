import React, { useState } from "react";
import { X, AlertCircle } from "lucide-react";
import axios from "axios";
import { Sidebar } from "../../components/sideBar/SideBar";
import { useNavigate } from "react-router-dom";
// Simple Card Components
const SimpleCard = ({ children, className = "" }) => (
  <div className={`bg-white rounded-lg shadow-md ${className}`}>{children}</div>
);

const SimpleCardContent = ({ children, className = "" }) => (
  <div className={`p-6 ${className}`}>{children}</div>
);

// Loading Overlay Component
const LoadingOverlay = () => (
  <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-85 z-50">
    <div className="text-center items-center flex flex-col">
      <div className="loader  mb-4"></div>
      <p className="text-white text-lg font-medium">Analysis is running, please wait...</p>
    </div>
    <style>{`
      .loader {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3498db;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
      }
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    `}</style>
  </div>
);

// Main Component
const ImageUploadPage = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);
  const navigate = useNavigate(); 

  const handleFileInput = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && validateFile(selectedFile)) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setError("");
    } else {
      setFile(null);
      setPreview(null);
    }
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && validateFile(droppedFile)) {
      setFile(droppedFile);
      setPreview(URL.createObjectURL(droppedFile));
      setError("");
    }
  };

  const validateFile = (file) => {
    const validTypes = ["image/jpeg", "image/png", "image/gif", "image/webp"];
    if (!validTypes.includes(file.type)) {
      setError(
        "Unsupported file type. Please upload a JPEG, PNG, GIF, or WebP image."
      );
      return false;
    }
    if (file.size > 2 * 1024 * 1024) {
      setError("File size exceeds 2MB. Please upload a smaller file.");
      return false;
    }
    return true;
  };

  const removeFile = () => {
    setFile(null);
    setPreview(null);
    setError("");
  };

  const handleAnalysis = async () => {
    if (!file) return;
    setIsAnalyzing(true);

    try {
      const formData = new FormData();
      formData.append("image", file);
      const response = await axios.post(
        "http://localhost:5001/predict",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      if (response.status === 200) {
        setIsAnalyzing(false);
        console.log(response.data);
        navigate("/result", { state: response.data });
      }
    } catch (error) {
      console.error("Error during analysis:", error);
      alert("An error occurred during the analysis. Please try again.");
    } finally {
      setIsAnalyzing(false);
    }
  };



  // const handleAnalysis = async () => {
  //   if (!file) return;
  //   setIsAnalyzing(true);
    
  //   try {
  //     const formData = new FormData();
  //     formData.append("image", file);
  
  //     const response = {
  //       adulteration: "false",
  //       variety: [
  //         { name: "Basmati Supreme", percentage: "40%", confidence: "89.9%" },
  //         // { name: "Non-Basmati Blend", percentage: "60%", confidence: "57%" },
  //       ],
  //     };
  
  //     // Simulating a 5-second analysis delay
  //     await new Promise((resolve) => setTimeout(resolve, 5000));
  //     setIsAnalyzing(false);
  //     navigate("/result", { state: response });
  //   } catch (error) {
  //     console.error("Error during analysis:", error);
  //     alert("An error occurred during the analysis. Please try again.");
  //   } finally {
  //     setIsAnalyzing(false);
  //   }
  // };
  


  return (
    <div className="flex h-screen bg-white">
      {isAnalyzing && <LoadingOverlay />}
      <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
      <div className="flex-1 pl-20 flex flex-col overflow-y-auto">
        <div className="container mt-12 mx-auto p-4">
          <div className="max-w-4xl mx-auto px-4 w-full">
            <h1 className="text-3xl font-bold text-left mb-8 text-green-500 border-b-2 border-gray-200 pb-4">
              Upload Image
            </h1>

            {/* File Upload Area */}
            <SimpleCard className="mb-6 mt-4">
              <SimpleCardContent>
                <div
                  className={`relative border-2 border-dashed rounded-lg p-8 text-center ${
                    isDragging ? "border-blue-500 bg-blue-50" : "border-gray-300"
                  } ${!file ? "hover:border-blue-500 hover:bg-blue-50" : ""}`}
                  onDragEnter={handleDragEnter}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                >
                  {!file ? (
                    <>
                      <p className="text-lg mb-2">Drag and drop your image here</p>
                      <label className="mt-2 inline-block cursor-pointer">
                        <span className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                          Browse Files
                        </span>
                        <input
                          type="file"
                          className="hidden"
                          accept="image/*"
                          onChange={handleFileInput}
                        />
                      </label>
                    </>
                  ) : (
                    <>
                      {preview && (
                        <div className="relative max-w-md mx-auto">
                          <img
                            src={preview}
                            alt="Preview"
                            className="max-h-64 mx-auto rounded-lg"
                          />
                          <button
                            className="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-full hover:bg-red-600"
                            onClick={removeFile}
                          >
                            <X className="w-4 h-4" />
                          </button>
                        </div>
                      )}
                    </>
                  )}
                </div>
              </SimpleCardContent>
            </SimpleCard>

            {/* Action Button */}
            {file && !error && (
              <button
                onClick={handleAnalysis}
                disabled={isAnalyzing}
                className={`w-full mt-6 py-3 rounded-lg text-white ${
                  isAnalyzing
                    ? "bg-gray-600 cursor-not-allowed"
                    : "bg-blue-600 hover:bg-blue-700"
                }`}
              >
                {isAnalyzing ? "Analyzing..." : "Start Analysis"}
              </button>
            )}
            
            {/* Guidelines */}
            <SimpleCard className="mt-8">
              <SimpleCardContent>
                <h2 className="text-xl font-semibold mb-4">
                  Guidelines for Best Results:
                </h2>
                <ul className="space-y-2 text-gray-600">
                  <li>• Supported formats: JPEG, PNG</li>
                  <li>• Maximum file size: 4MB</li>
                  <li>• Higher resolution images yield better results</li>
                  <li>• Ensure the image is clear and well-lit</li>
                </ul>
              </SimpleCardContent>
            </SimpleCard>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageUploadPage;
