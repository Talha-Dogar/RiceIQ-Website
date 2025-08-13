import React, { useState } from "react";
import {IdentificationTable,ExpandableTable} from "./dropdown";
const ViewRecords = ({analysisData, identificationData})=> {
  const [viewMode, setViewMode] = useState('analysis'); // 'analysis' or 'identification'
  
  return (
    <div className="min-h-screen bg-green-50">
      {viewMode === 'analysis' ? (
        <ExpandableTable 
          data={analysisData} 
          onSwitchView={() => setViewMode('identification')} 
        />
      ) : (
        <IdentificationTable 
          data={identificationData} 
          onSwitchView={() => setViewMode('analysis')}
        />
      )}
    </div>
  );
};

export default ViewRecords;