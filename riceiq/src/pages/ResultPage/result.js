import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import axios from "axios";
import { Sidebar } from "../../components/sideBar/SideBar";

ChartJS.register(ArcElement, Tooltip, Legend);

const RiceAnalysisResults = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [response, setResponse] = useState([]);
  const location = useLocation();
  const { resultID: resultID } = location.state || {}; // Handle missing state gracefully

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  useEffect(() => {
    if (!resultID) return; // Prevent API call if resultID is missing

    (async () => {
      try {
        const { data } = await axios.get(
          `http://localhost:5001/result/${resultID}`
        );
        console.log("Result fetched:", data);
        setResponse(data);
      } catch (error) {
        console.error(
          "Error fetching result:",
          error.response?.data || error.message
        );
      }
    })();
  }, [resultID]);

  const adulterationStatus =
     response.adulteration === false
      ? "No Adulteration Detected"
      : "Adulteration Detected";

      const chartData = {
        labels: response.variety || [],
        datasets: [
          {
            label: "Rice Variety Composition",
            data: response.variety?.map((v) => response.percentage?.[v] || 0) || [],
            backgroundColor: ["#1E3A8A", "#4CAF50", "#FFC107", "#2196F3", "#FF5722"],
            borderColor: ["#4CAF50", "#FFC107", "#2196F3", "#FF5722"],
            borderWidth: 1,
          },
        ],
      };
      

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: "top" } },
  };

  const currentDate = new Date().toLocaleDateString("en-GB", {
    timeZone: "Asia/Karachi",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
      <div className="flex-1 pl-20 flex flex-col overflow-y-auto">
        <div className="container mt-12 mx-auto p-4">
          <div className="bg-gray-100 min-h-screen flex flex-col">
            {/* Header */}
            <header className="bg-[#00AAAA] text-white m-6 py-6 text-center">
              <h1 className="text-2xl font-bold">
                Rice Sample Analysis Results
              </h1>
              <p>
                Sample ID: {resultID || "Unknown"} | Analysis Date:{" "}
                {currentDate}
              </p>
            </header>

            {/* Main Content */}
            <main className="flex-1 p-6">
              {/* Adulteration Status Card */}
              <div className="bg-white rounded-lg shadow-md p-6 mb-6 border border-gray-200">
                <h2 className="text-xl text-green-700 font-bold mb-4">
                  Adulteration Status
                </h2>
                <p className="text-lg text-gray-700">{adulterationStatus}</p>
              </div>

              {/* Rice Variety Composition Card */}
              <div className="bg-white rounded-lg shadow-md p-6 mb-6 border border-gray-200">
                <h2 className="text-xl font-bold mb-4 text-green-700">
                  Rice Variety Composition
                </h2>
                <div className="flex justify-center align-middle my-6">
                  <div style={{ width: "300px", height: "300px" }}>
                    <Pie data={chartData} options={chartOptions} />
                  </div>
                </div>
                <table className="w-full border-collapse border border-gray-300 mt-6">
                  <thead>
                    <tr className="bg-[#00AAAA] text-white">
                      <th className="border border-gray-300 px-4 py-2 text-left">
                        Variety Name
                      </th>
                      <th className="border border-gray-300 px-4 py-2 text-left">
                        Percentage
                      </th>
                      <th className="border border-gray-300 px-4 py-2 text-left">
                        Confidence Level
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {response.variety?.map((variety, index) => (
                      <tr key={index}>
                        <td className="border border-gray-300 px-4 py-2">
                          {variety}
                        </td>
                        <td className="border border-gray-300 px-4 py-2">
                          {response.percentage?.[variety] || 0}%
                        </td>
                        <td className="border border-gray-300 px-4 py-2">
                          {response.confidence}
                        </td>
                      </tr>
                    )) || []}
                  </tbody>
                </table>
              </div>
            </main>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RiceAnalysisResults;
