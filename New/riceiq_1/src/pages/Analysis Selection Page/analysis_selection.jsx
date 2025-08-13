import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Sidebar } from "../../components/sideBar/SideBar";
import { Sprout, Droplet, Leaf } from "lucide-react";

const AnalysisSelectionPage = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const navigate = useNavigate();

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  const handleAnalysisSelect = (type) => {
    navigate("/upload", { state: { analysisType: type } });
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-emerald-50 to-white">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -right-24 -top-24 w-96 h-96 bg-teal-600 rounded-full opacity-20"></div>
        <div className="absolute -left-32 top-1/3 w-64 h-64 bg-teal-600 rounded-full opacity-20"></div>
        <div className="absolute right-1/4 bottom-0 w-80 h-80 bg-emerald-300 rounded-full opacity-20"></div>
        
        {/* Rice grain patterns */}
        {/* <svg className="absolute top-20 right-1/3 text-emerald-300 opacity-10" width="120" height="40" viewBox="0 0 120 40">
          <path d="M20,0 Q40,20 20,40 Q0,20 20,0 Z" fill="currentColor"/>
        </svg>
        <svg className="absolute bottom-32 left-1/4 text-emerald-400 opacity-10" width="80" height="30" viewBox="0 0 80 30">
          <path d="M15,0 Q30,15 15,30 Q0,15 15,0 Z" fill="currentColor"/>
        </svg>
        <svg className="absolute top-1/2 right-1/4 text-emerald-300 opacity-10" width="100" height="35" viewBox="0 0 100 35">
          <path d="M17,0 Q34,17 17,35 Q0,17 17,0 Z" fill="currentColor"/>
        </svg> */}
      </div>
<div className="z-20">

      <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
</div>

      <div className="flex-1 pl-20 flex flex-col overflow-y-auto relative z-10">
        <div className="container mt-12 mx-auto p-4">
          <div className="max-w-4xl mx-auto px-4 w-full">
            <div className="flex items-center mb-6">
              <div className="relative">
                <div className="absolute -inset-1 bg-emerald-500 rounded-full opacity-20 blur-sm"></div>
                <Leaf className="text-emerald-600 relative" size={32} />
              </div>
              <h1 className="text-3xl font-bold text-emerald-700 ml-4">
                Select Analysis Type
              </h1>
            </div>
            
            <div className="h-1 w-32 bg-gradient-to-r from-emerald-500 to-emerald-300 rounded-full mb-6"></div>

            <p className="text-gray-700 mb-10 text-lg">
              Choose the type of analysis you would like to perform on your rice sample
            </p>

            <div className="grid md:grid-cols-2 gap-8 mt-8">
              {/* Variety Identification Card */}
              <div
                className="bg-white rounded-xl shadow-lg transition-all duration-300 cursor-pointer hover:shadow-xl border-2 border-transparent hover:border-emerald-200 group overflow-hidden"
                onClick={() => handleAnalysisSelect("variety")}
              >
                {/* <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div> */}
                <div className="p-8 relative">
                  <div className="flex items-center justify-center mb-6 w-20 h-20 rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 text-white mx-auto shadow-md group-hover:scale-110 transition-transform duration-300">
                    <Sprout size={36} />
                  </div>
                  <h3 className="text-2xl font-semibold text-center mb-4 text-emerald-800">Variety Identification</h3>
                  <p className="text-gray-600 text-center mb-6">
                    Identify the specific variety of rice from your sample image
                  </p>
                  {/* <div className="text-sm text-gray-500">
                    <ul className="space-y-3">
                      <li className="flex items-center">
                        <div className="w-2 h-2 rounded-full bg-emerald-500 mr-3"></div>
                        Detects multiple rice varieties
                      </li>
                      <li className="flex items-center">
                        <div className="w-2 h-2 rounded-full bg-emerald-500 mr-3"></div>
                        Shows percentage composition
                      </li>
                      <li className="flex items-center">
                        <div className="w-2 h-2 rounded-full bg-emerald-500 mr-3"></div>
                        High accuracy identification
                      </li>
                    </ul>
                  </div> */}
                </div>
              </div>

              {/* Adulteration Detection Card */}
              <div
                className="bg-white rounded-xl shadow-lg transition-all duration-300 cursor-pointer hover:shadow-xl border-2 border-transparent hover:border-emerald-200 group overflow-hidden"
                // className="relative bg-white rounded-xl shadow-lg transition-all duration-300 transform hover:scale-105 hover:shadow-2xl border-2 border-transparent  cursor-pointer"
                onClick={() => handleAnalysisSelect("adulteration")}
              >
                {/* <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div> */}
                <div className="p-8 relative">
                  <div className="flex items-center justify-center mb-6 w-20 h-20 rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 text-white mx-auto shadow-md group-hover:scale-110 transition-transform duration-300">
                    <Droplet size={36} />
                  </div>
                  <h3 className="text-2xl font-semibold text-center mb-4 text-emerald-800">Adulteration Detection</h3>
                  <p className="text-gray-600 text-center mb-6">
                    Check if your rice sample contains any adulterants or impurities
                  </p>
                  {/* <div className="text-sm text-gray-500">
                    <ul className="space-y-3">
                      <li className="flex items-center">
                        <div className="w-2 h-2 rounded-full bg-emerald-500 mr-3"></div>
                        Detects common adulterants
                      </li>
                      <li className="flex items-center">
                        <div className="w-2 h-2 rounded-full bg-emerald-500 mr-3"></div>
                        Provides contamination level
                      </li>
                      <li className="flex items-center">
                        <div className="w-2 h-2 rounded-full bg-emerald-500 mr-3"></div>
                        Food safety assessment
                      </li>
                    </ul>
                  </div> */}
                </div>
              </div>
            </div>

            <div className="mt-12 text-center text-emerald-600 text-sm font-medium">
              Select one of the options above to proceed
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisSelectionPage;