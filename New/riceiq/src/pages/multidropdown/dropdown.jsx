import React, { useState } from "react";
import { ChevronDown, ChevronRight, Eye, Trash2, Menu, X, Leaf, FileText, FlaskConical } from "lucide-react";
import { Sidebar } from "../../components/sideBar/SideBar";

// // Sidebar component included directly to simplify the example
// const Sidebar = ({ isOpen, toggleSidebar }) => {
//   return (
//     <div
//       className={`fixed h-screen bg-emerald-900 text-white transition-all duration-300 ease-in-out ${
//         isOpen ? "w-64" : "w-20"
//       }`}
//     >
//       <div className="flex items-center justify-between p-4 border-b border-emerald-700">
//         <div className="flex items-center space-x-2">
//           <Leaf className="text-emerald-400" size={24} />
//           {isOpen && <span className="font-bold text-xl">RiceIQ</span>}
//         </div>
//         <button onClick={toggleSidebar} className="text-emerald-300 hover:text-white">
//           {isOpen ? <X size={20} /> : <Menu size={20} />}
//         </button>
//       </div>
      
//       <div className="mt-6">
//         <div className="px-4 py-3 flex items-center text-emerald-300 hover:bg-emerald-800 cursor-pointer">
//           <div className="flex items-center">
//             <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6z" />
//               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6z" />
//               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2z" />
//               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
//             </svg>
//             {isOpen && <span className="ml-3">Dashboard</span>}
//           </div>
//         </div>
        
//         <div className="px-4 py-3 flex items-center text-emerald-300 hover:bg-emerald-800 cursor-pointer">
//           <div className="flex items-center">
//             <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
//             </svg>
//             {isOpen && <span className="ml-3">Image Upload</span>}
//           </div>
//         </div>
        
//         <div className="px-4 py-3 flex items-center bg-emerald-800 text-white cursor-pointer">
//           <div className="flex items-center">
//             <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
//             </svg>
//             {isOpen && <span className="ml-3">Records</span>}
//           </div>
//         </div>
        
//         <div className="px-4 py-3 flex items-center text-emerald-300 hover:bg-emerald-800 cursor-pointer">
//           <div className="flex items-center">
//             <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
//               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
//             </svg>
//             {isOpen && <span className="ml-3">Settings</span>}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

export const IdentificationTable = ({ data, onSwitchView }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  return (
    <div className="flex h-screen bg-green-50">
      <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />

      <div
        className={`transition-all duration-300 ${
          sidebarOpen ? "ml-64" : "ml-20"
        } w-full p-8`}
      >
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex flex-col space-y-4 mb-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-emerald-800 flex items-center">
                <FileText className="h-7 w-7 mr-2 text-emerald-600" />
                Rice Identification Records
              </h2>
              <div className="text-sm text-gray-500">Total: {data.length} records</div>
            </div>
            
            <div className="flex space-x-4">
              <button 
                onClick={onSwitchView}
                className="px-4 py-2 bg-emerald-600 text-white rounded-md flex items-center justify-center shadow-sm hover:bg-emerald-700 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500"
              >
                <FlaskConical className="w-4 h-4 mr-2" />
                Analysis Records
              </button>
              <button 
                className="px-4 py-2 bg-emerald-100 text-emerald-800 font-medium rounded-md flex items-center justify-center shadow-sm hover:bg-emerald-200 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500"
              >
                <FileText className="w-4 h-4 mr-2" />
                Identification Records
              </button>
            </div>
          </div>

          <div className="overflow-hidden rounded-lg border border-emerald-100 shadow-sm">
            <table className="min-w-full divide-y divide-emerald-200">
              <thead className="bg-emerald-50">
                <tr>
                  <th scope="col" className="px-6 py-4 text-left text-sm font-medium text-emerald-900">Image</th>
                  <th scope="col" className="px-6 py-4 text-left text-sm font-medium text-emerald-900">Date</th>
                  <th scope="col" className="px-6 py-4 text-center text-sm font-medium text-emerald-900">Rice Grains Total</th>
                  <th scope="col" className="px-6 py-4 text-left text-sm font-medium text-emerald-900">Variety Name</th>
                  <th scope="col" className="px-6 py-4 text-center text-sm font-medium text-emerald-900">Confidence Score</th>
                  <th scope="col" className="px-6 py-4 text-center text-sm font-medium text-emerald-900">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-emerald-100 bg-white">
                {data.map((record) => (
                  <tr key={record.id} className="hover:bg-emerald-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="h-14 w-14 rounded-md overflow-hidden border-2 border-emerald-200">
                          <img src={record.image || "/api/placeholder/100/100"} alt="Rice Sample" className="h-full w-full object-cover" />
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                      {record.date}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-center text-gray-700">
                      <span className="inline-flex items-center justify-center px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 font-medium">
                        {record.grainsTotal}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-emerald-900">
                      {record.varietyName}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center">
                      <div className="flex items-center justify-center">
                        <div className="w-full bg-gray-200 rounded-full h-2.5">
                          <div 
                            className={`h-2.5 rounded-full ${
                              record.confidenceScore >= 80 ? 'bg-green-600' : 
                              record.confidenceScore >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                            }`} 
                            style={{ width: `${record.confidenceScore}%` }}
                          ></div>
                        </div>
                        <span className="ml-2 text-sm font-medium text-gray-700">{record.confidenceScore}%</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center">
                      <button className="inline-flex items-center p-1.5 border border-red-300 rounded-md shadow-sm bg-white hover:bg-red-50 text-red-700 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export const ExpandableTable = ({ data, onSwitchView }) => {
  const [expandedRows, setExpandedRows] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  const handleRowClick = (recordId) => {
    setExpandedRows((prev) =>
      prev.includes(recordId) ? prev.filter((id) => id !== recordId) : [...prev, recordId]
    );
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'pure':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'adulterated':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'suspicious':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="flex h-screen bg-green-50">
      <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />

      <div
        className={`transition-all duration-300 ${
          sidebarOpen ? "ml-64" : "ml-20"
        } w-full p-8`}
      >
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex flex-col space-y-4 mb-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-emerald-800 flex items-center">
                <FlaskConical className="h-7 w-7 mr-2 text-emerald-600" />
                Rice Analysis Records
              </h2>
              <div className="text-sm text-gray-500">Total: {data.length} records</div>
            </div>
            
            <div className="flex space-x-4">
              <button 
                className="px-4 py-2 bg-emerald-100 text-emerald-800 font-medium rounded-md flex items-center justify-center shadow-sm hover:bg-emerald-200 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500"
              >
                <FlaskConical className="w-4 h-4 mr-2" />
                Analysis Records
              </button>
              <button 
                onClick={onSwitchView}
                className="px-4 py-2 bg-emerald-600 text-white rounded-md flex items-center justify-center shadow-sm hover:bg-emerald-700 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500"
              >
                <FileText className="w-4 h-4 mr-2" />
                Identification Records
              </button>
            </div>
          </div>

          <div className="overflow-hidden rounded-lg border border-emerald-100 shadow-sm">
            <table className="min-w-full divide-y divide-emerald-200">
              <thead className="bg-emerald-50">
                <tr>
                  <th scope="col" className="px-6 py-4 text-left text-sm font-medium text-emerald-900">Name</th>
                  <th scope="col" className="px-6 py-4 text-left text-sm font-medium text-emerald-900">Details</th>
                  <th scope="col" className="px-6 py-4 text-center text-sm font-medium text-emerald-900">Total Samples</th>
                  <th scope="col" className="px-6 py-4 text-center text-sm font-medium text-emerald-900">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-emerald-100 bg-white">
                {data.map((record) => {
                  const isExpanded = expandedRows.includes(record.id);
                  return (
                    <React.Fragment key={record.id}>
                      <tr 
                        className={`hover:bg-emerald-50 transition-colors ${isExpanded ? 'bg-emerald-50' : ''}`}
                      >
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-emerald-900">
                          {record.name}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                          {record.details}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-center text-gray-700">
                          <span className="inline-flex items-center justify-center px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 font-medium">
                            {record.subRecords.length}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-center">
                          <button
                            onClick={() => handleRowClick(record.id)}
                            className={`inline-flex items-center justify-center px-3 py-1 border border-transparent text-sm font-medium rounded-md shadow-sm text-white ${isExpanded ? 'bg-emerald-600 hover:bg-emerald-700' : 'bg-emerald-500 hover:bg-emerald-600'} transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500`}
                          >
                            {isExpanded ? (
                              <>
                                <ChevronDown className="w-4 h-4 mr-1" /> Hide Samples
                              </>
                            ) : (
                              <>
                                <ChevronRight className="w-4 h-4 mr-1" /> View Samples
                              </>
                            )}
                          </button>
                        </td>
                      </tr>
                      {isExpanded && (
                        <tr>
                          <td colSpan="4" className="px-0 py-0 bg-emerald-50">
                            <div className="p-4">
                              <div className="bg-white rounded-lg shadow-sm overflow-hidden border border-emerald-100">
                                <table className="min-w-full divide-y divide-emerald-200">
                                  <thead className="bg-emerald-100">
                                    <tr>
                                      <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-emerald-900 uppercase tracking-wider">Sr No</th>
                                      <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-emerald-900 uppercase tracking-wider">Image</th>
                                      <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-emerald-900 uppercase tracking-wider">Adulteration Status</th>
                                      <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-emerald-900 uppercase tracking-wider">Date Analysed</th>
                                      <th scope="col" className="px-4 py-3 text-center text-xs font-medium text-emerald-900 uppercase tracking-wider">Actions</th>
                                    </tr>
                                  </thead>
                                  <tbody className="bg-white divide-y divide-emerald-100">
                                    {record.subRecords.map((subRecord, index) => (
                                      <tr key={subRecord.subId} className="hover:bg-emerald-50 transition-colors">
                                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700 text-center">
                                          {index + 1}
                                        </td>
                                        <td className="px-4 py-3 whitespace-nowrap">
                                          <div className="flex items-center justify-center">
                                            <div className="h-14 w-14 rounded-md overflow-hidden border-2 border-emerald-200">
                                              <img src={subRecord.image || "/api/placeholder/100/100"} alt="Sample" className="h-full w-full object-cover" />
                                            </div>
                                          </div>
                                        </td>
                                        <td className="px-4 py-3 whitespace-nowrap">
                                          <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(subRecord.adulterationStatus)}`}>
                                            {subRecord.adulterationStatus}
                                          </span>
                                        </td>
                                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                                          {subRecord.dateAnalysed}
                                        </td>
                                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                                          <div className="flex items-center justify-center space-x-2">
                                            <button className="inline-flex items-center p-1.5 border border-emerald-300 rounded-md shadow-sm bg-white hover:bg-emerald-50 text-emerald-700 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500">
                                              <Eye className="w-4 h-4" />
                                            </button>
                                            <button className="inline-flex items-center p-1.5 border border-red-300 rounded-md shadow-sm bg-white hover:bg-red-50 text-red-700 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                                              <Trash2 className="w-4 h-4" />
                                            </button>
                                          </div>
                                        </td>
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>
                            </div>
                          </td>
                        </tr>
                      )}
                    </React.Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};



