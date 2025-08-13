// /src/routes/AppRoutes.js
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from '../pages/HomePage/home';
import ImageUploadPage from '../pages/ImageUploadPage/imageUpload';
import RiceAnalysisResults from '../pages/ResultPage/result';
// import ExpandableTable from '../pages/multidropdown/dropdown';
import ViewRecords from '../pages/multidropdown/viewRecords';
import AnalysisSelectionPage from '../pages/Analysis Selection Page/analysis_selection';
import {analysisData, identificationData} from '../pages/multidropdown/dummydata';
import RiceIQDashboard from '../pages/Dashboard/dashboard';
const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/analysis_selection" element={<AnalysisSelectionPage />} />
        <Route path="/upload" element={<ImageUploadPage />} />
        <Route path="/result" element={<RiceAnalysisResults />} />
        <Route path="/view_records" element={<ViewRecords analysisData={analysisData} identificationData={identificationData} />} />
        <Route path="/dashboard" element={<RiceIQDashboard />} />
        {/* Add more routes as needed */}
      </Routes>
    </Router>
  );
};

export default AppRoutes;
