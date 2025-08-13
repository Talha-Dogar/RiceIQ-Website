import React, { useState } from "react";
import { Sidebar } from "../../components/sideBar/SideBar";

const ExpandableTable = ({ data }) => {
  const [expandedRows, setExpandedRows] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  const handleRowClick = (recordId) => {
    setExpandedRows((prev) =>
      prev.includes(recordId) ? prev.filter((id) => id !== recordId) : [...prev, recordId]
    );
  };

  return (
    <div className="flex h-screen gap-8 bg-white">
      <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />

      <div
        className={`p-4 mt-6 transition-all duration-300 ${
          sidebarOpen ? "w-[calc(100%-250px)] " : " w-full"
        }`}
      >
        <h2 className="text-2xl font-semibold mb-4">Records</h2>
        <table className="min-w-full bg-white border border-gray-200">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b">Name</th>
              <th className="py-2 px-4 border-b">Details</th>
              <th className="py-2 px-4 border-b">Total Samples</th>
              <th className="py-2 px-4 border-b">Expand</th>
            </tr>
          </thead>
          <tbody>
            {data.map((record) => {
              const isExpanded = expandedRows.includes(record.id);
              return (
                <React.Fragment key={record.id}>
                  <tr
                    className="cursor-pointer hover:bg-gray-100"
                    onClick={() => handleRowClick(record.id)}
                  >
                    <td className="py-2 px-4 border-b text-center">{record.name}</td>
                    <td className="py-2 px-4 border-b text-center">{record.details}</td>
                    <td className="py-2 px-4 border-b text-center">{record.id}</td>
                    <td className="py-2 px-4 border-b text-center">
                      {isExpanded ? "▼" : "▶"}
                    </td>
                  </tr>
                  {isExpanded && (
                    <tr>
                      <td colSpan="4" className="p-4 bg-gray-50">
                        <table className="min-w-full bg-white border border-gray-200">
                          <thead>
                            <tr>
                              <th className="py-2 px-6 border-b">Sr No</th>
                              <th className="py-2 px-12 border-b">Image</th>
                              <th className="py-2 px-10 border-b">Adulteration Status</th>
                              <th className="py-2 px-10 border-b">Date Analysed</th>
                              <th className="py-2 px-8 border-b">View Detail</th>
                              <th className="py-2 px-8 border-b">Delete</th>
                            </tr>
                          </thead>
                          <tbody>
                            {record.subRecords.map((subRecord, index) => (
                              <tr key={subRecord.subId}>
                                <td className="py-2 px-6 border-b text-center">{index + 1}</td>
                                <td className="py-2 px-12 border-b text-center">
                                  <img src={subRecord.image} alt="Sample" className="h-12 w-12 object-cover" />
                                </td>
                                <td className="py-2 px-10 border-b text-center">{subRecord.adulterationStatus}</td>
                                <td className="py-2 px-10 border-b text-center">{subRecord.dateAnalysed}</td>
                                <td className="py-2 px-8 border-b text-center">
                                  <button className="bg-blue-500 text-white px-3 py-1 rounded">View</button>
                                </td>
                                <td className="py-2 px-8 border-b text-center">
                                  <button className="bg-red-500 text-white px-3 py-1 rounded">Delete</button>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
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
  );
};

export default ExpandableTable;

