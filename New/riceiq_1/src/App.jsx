// import { Sidebar } from './components/sidebar';
// import EventManagementPage from './pages/eventManagement/EventManagementPage';
// import ImageUploadPage from './pages/ImageUploadPage/imageUpload';
// import AnalysisPage from './pages/AnalysisPage/analysisAnimation';
// import RiceAnalysisResults from './pages/ResultPage/result';
// import Home from './pages/HomePage/home';
// function App() {
//   return (
//     <Expa
//     // <Home/>
//     // <EventManagementPage/>
//     // <ImageUploadPage/>

//     // <AnalysisPage/>
//   //  <Sidebar/>
//   // <RiceAnalysisResults/>
//   );
// }

// export default App;

import AppRoutes from "./routes/routes"
export default function App() {
  return (
  <div>
   <AppRoutes/>
  </div>
  )
}

// import React from 'react';
// import ExpandableTable from './pages/multidropdown/dropdown';

// const App = () => {
//   const data = [
//     {
//       id: 1,
//       name: 'Record 1',
//       details: 'Main details of Record 1',
//       subRecords: [
//         { subId: 1.1, subName: 'Sub-record 1.1', subDetails: 'Details of Sub-record 1.1' },
//         { subId: 1.2, subName: 'Sub-record 1.2', subDetails: 'Details of Sub-record 1.2' },
//       ],
//     },
//     {
//       id: 2,
//       name: 'Record 2',
//       details: 'Main details of Record 2',
//       subRecords: [
//         { subId: 2.1, subName: 'Sub-record 2.1', subDetails: 'Details of Sub-record 2.1' },
//       ],
//     },
//     // Add more records as needed
//   ];

//   return (
//     <div className="App">
//       <ExpandableTable data={data} />
//     </div>
//   );
// };

// export default App;
