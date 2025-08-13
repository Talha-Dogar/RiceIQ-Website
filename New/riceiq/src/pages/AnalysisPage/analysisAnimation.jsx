import React, { useState } from "react";

const AnalysisPage = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleStartAnalysis = () => {
    setIsAnalyzing(true);

    // Simulate backend request (replace this with actual API call logic)
    setTimeout(() => {
      setIsAnalyzing(false);
      // Navigate to the result page or handle response here
      console.log("Analysis complete!");
    }, 5000); // Simulating a 5-second analysis delay
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Image Upload and Analysis</h1>

      {!isAnalyzing ? (
        <div className="flex flex-col items-center">
          <input
            type="file"
            accept="image/*"
            className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
          />
          <button
            onClick={handleStartAnalysis}
            className="mt-4 px-6 py-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Start Analysis
          </button>
        </div>
      ) : (
        <div className="flex flex-col items-center">
          {/* Animation Section */}
          <div className="flex items-center justify-center h-16 w-16 border-4 border-blue-500 border-dashed rounded-full animate-spin"></div>
          <p className="mt-4 text-lg font-medium text-gray-700">Analyzing Results...</p>
        </div>
      )}
    </div>
  );
};

export default AnalysisPage;
