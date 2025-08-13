// /src/routes/AppRoutes.js
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from '../pages/HomePage/home';
import ImageUploadPage from '../pages/ImageUploadPage/imageUpload';
import RiceAnalysisResults from '../pages/ResultPage/result';
import ExpandableTable from '../pages/multidropdown/dropdown';
import data from '../pages/multidropdown/dummydata';
const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<ImageUploadPage />} />
        <Route path="/result" element={<RiceAnalysisResults />} />
        <Route path="/expandable-table" element={<ExpandableTable data={data} />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;
