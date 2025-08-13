import React, { useState } from "react";
import {
  BarChart,
  LineChart,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Bar,
  Cell,
  Line,
  ResponsiveContainer,
} from "recharts";
import {
  Leaf,
  FileText,
  FlaskConical,
  TrendingUp,
  AlertCircle,
  Table,
  Users,
  Menu,
  X,
  ChevronRight,
} from "lucide-react";
import { Sidebar } from "../../components/sideBar/SideBar";
// Sidebar Component

const RiceIQDashboard = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  // Sample data for charts
  const monthlyData = [
    { name: "Jan", identification: 65, adulteration: 45 },
    { name: "Feb", identification: 59, adulteration: 49 },
    { name: "Mar", identification: 80, adulteration: 40 },
    { name: "Apr", identification: 81, adulteration: 56 },
    { name: "May", identification: 56, adulteration: 38 },
    { name: "Jun", identification: 55, adulteration: 70 },
  ];

  const adulterationData = [
    { name: "Pure", value: 65 },
    { name: "Adulterated", value: 35 },
  ];

  // Sample data for tables
  const recentIdentifications = [
    {
      id: 1,
      image: "/api/placeholder/50/50",
      date: "2025-05-02",
      varietyName: "Basmati",
      grainsTotal: 120,
      confidenceScore: 95,
    },
    {
      id: 2,
      image: "/api/placeholder/50/50",
      date: "2025-05-01",
      varietyName: "Jasmine",
      grainsTotal: 110,
      confidenceScore: 88,
    },
    {
      id: 3,
      image: "/api/placeholder/50/50",
      date: "2025-04-30",
      varietyName: "Arborio",
      grainsTotal: 105,
      confidenceScore: 92,
    },
  ];

  const recentAdulterations = [
    {
      id: 1,
      image: "/api/placeholder/50/50",
      date: "2025-05-02",
      seller: "ABC Rice Mills",
      status: "Adulterated",
      confidence: 89,
    },
    {
      id: 2,
      image: "/api/placeholder/50/50",
      date: "2025-05-01",
      seller: "XYZ Exports",
      status: "Pure",
      confidence: 95,
    },
    {
      id: 3,
      image: "/api/placeholder/50/50",
      date: "2025-04-30",
      seller: "Global Rice Co.",
      status: "Suspicious",
      confidence: 78,
    },
  ];

  const sellerTrends = [
    { id: 1, name: "ABC Rice Mills", total: 56, adulterated: 12, rate: "21%" },
    { id: 2, name: "XYZ Exports", total: 42, adulterated: 5, rate: "12%" },
    { id: 3, name: "Global Rice Co.", total: 38, adulterated: 8, rate: "21%" },
  ];

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case "pure":
        return "bg-green-100 text-green-800 border-green-200";
      case "adulterated":
        return "bg-red-100 text-red-800 border-red-200";
      case "suspicious":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  return (
    <div className="flex h-screen bg-green-50">
      <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />

      <div
        className={`transition-all duration-300 ${
          sidebarOpen ? "ml-64" : "ml-20"
        } w-full p-6 overflow-y-auto`}
      >
        <h1 className="text-3xl font-bold text-emerald-800 mb-6 flex items-center">
          <Leaf className="h-8 w-8 mr-2 text-emerald-600" />
          RiceIQ Dashboard
        </h1>

        {/* Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-emerald-500">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm text-gray-500 font-medium">
                  Total Analysis
                </p>
                <h3 className="text-2xl font-bold text-gray-800 mt-1">1,254</h3>
              </div>
              <div className="bg-emerald-100 p-3 rounded-lg">
                <FlaskConical className="h-6 w-6 text-emerald-600" />
              </div>
            </div>
            <p className="text-xs text-emerald-600 mt-2 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              <span>12% increase this month</span>
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm text-gray-500 font-medium">
                  Rice Identified
                </p>
                <h3 className="text-2xl font-bold text-gray-800 mt-1">865</h3>
              </div>
              <div className="bg-blue-100 p-3 rounded-lg">
                <FileText className="h-6 w-6 text-blue-600" />
              </div>
            </div>
            <p className="text-xs text-blue-600 mt-2 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              <span>5% increase this month</span>
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm text-gray-500 font-medium">
                  Adulterations Detected
                </p>
                <h3 className="text-2xl font-bold text-gray-800 mt-1">389</h3>
              </div>
              <div className="bg-red-100 p-3 rounded-lg">
                <AlertCircle className="h-6 w-6 text-red-600" />
              </div>
            </div>
            <p className="text-xs text-red-600 mt-2 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              <span>8% increase this month</span>
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm text-gray-500 font-medium">
                  Registered Sellers
                </p>
                <h3 className="text-2xl font-bold text-gray-800 mt-1">42</h3>
              </div>
              <div className="bg-purple-100 p-3 rounded-lg">
                <Users className="h-6 w-6 text-purple-600" />
              </div>
            </div>
            <p className="text-xs text-purple-600 mt-2 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              <span>3 new this month</span>
            </p>
          </div>
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Line Graph */}
          <div className="bg-white rounded-lg shadow-md p-6 col-span-2">
            <h2 className="text-lg font-bold text-emerald-800 mb-4">
              Analysis Trends
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart
                data={monthlyData}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="identification"
                  stroke="#10b981"
                  activeDot={{ r: 8 }}
                  name="Identification"
                />
                <Line
                  type="monotone"
                  dataKey="adulteration"
                  stroke="#ef4444"
                  name="Adulteration"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Adulteration vs Pure Pie */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-bold text-emerald-800 mb-4">
              Adulteration Status
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                layout="vertical"
                data={adulterationData}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" />
                <Tooltip />
                <Bar dataKey="value" barSize={30} radius={[0, 4, 4, 0]}>
                  {adulterationData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={index === 0 ? "#10b981" : "#ef4444"}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
            <div className="flex justify-center mt-4">
              <div className="flex items-center mr-4">
                <div className="w-3 h-3 bg-emerald-500 rounded-full mr-1"></div>
                <span className="text-sm text-gray-600">Pure (65%)</span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-red-500 rounded-full mr-1"></div>
                <span className="text-sm text-gray-600">Adulterated (35%)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Tables Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Recent Identifications */}
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="flex justify-between items-center p-4 border-b border-gray-200">
              <h2 className="text-lg font-bold text-emerald-800 flex items-center">
                <FileText className="h-5 w-5 mr-2 text-emerald-600" />
                Recent Identifications
              </h2>
              <button className="text-sm text-emerald-600 hover:text-emerald-800 font-medium">
                View All
              </button>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Rice
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Variety
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Confidence
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {recentIdentifications.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="h-10 w-10 rounded-md overflow-hidden border-2 border-emerald-200">
                            <img
                              src={item.image}
                              alt="Rice Sample"
                              className="h-full w-full object-cover"
                            />
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                        {item.varietyName}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                        {item.date}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="w-16 bg-gray-200 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full ${
                                item.confidenceScore >= 90
                                  ? "bg-green-500"
                                  : item.confidenceScore >= 70
                                  ? "bg-yellow-500"
                                  : "bg-red-500"
                              }`}
                              style={{ width: `${item.confidenceScore}%` }}
                            ></div>
                          </div>
                          <span className="ml-2 text-xs font-medium text-gray-500">
                            {item.confidenceScore}%
                          </span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Recent Adulterations */}
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="flex justify-between items-center p-4 border-b border-gray-200">
              <h2 className="text-lg font-bold text-emerald-800 flex items-center">
                <AlertCircle className="h-5 w-5 mr-2 text-emerald-600" />
                Adulteration Analysis
              </h2>
              <button className="text-sm text-emerald-600 hover:text-emerald-800 font-medium">
                View All
              </button>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Sample
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Seller
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {recentAdulterations.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="h-10 w-10 rounded-md overflow-hidden border-2 border-emerald-200">
                            <img
                              src={item.image}
                              alt="Rice Sample"
                              className="h-full w-full object-cover"
                            />
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                        {item.seller}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                        {item.date}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(
                            item.status
                          )}`}
                        >
                          {item.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Seller Adulteration Trends */}
        {/* <div className="bg-white rounded-lg shadow-md overflow-hidden mb-6">
          <div className="flex justify-between items-center p-4 border-b border-gray-200">
            <h2 className="text-lg font-bold text-emerald-800 flex items-center">
              <Users className="h-5 w-5 mr-2 text-emerald-600" />
              Seller Adulteration Trends
            </h2>
            <button className="text-sm text-emerald-600 hover:text-emerald-800 font-medium">
              View All Sellers
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Seller Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total Samples
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Adulterated
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Adulteration Rate
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Risk Level
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {sellerTrends.map((seller) => {
                  let riskLevel;
                  const rate = parseInt(seller.rate);
                  if (rate < 15) {
                    riskLevel = "Low";
                    riskClass = "bg-green-100 text-green-800";
                  } else if (rate < 25) {
                    riskLevel = "Medium";
                    riskClass = "bg-yellow-100 text-yellow-800";
                  } else {
                    riskLevel = "High";
                    riskClass = "bg-red-100 text-red-800";
                  }
                  let riskClass;

                  return (
                    <tr key={seller.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {seller.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {seller.total}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {seller.adulterated}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {seller.rate}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${riskClass}`}
                        >
                          {riskLevel}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div> */}
      </div>
    </div>
  );
};

export default RiceIQDashboard;
