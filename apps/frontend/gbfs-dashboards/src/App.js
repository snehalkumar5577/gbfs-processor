// src/App.js

import React from "react";
import Dashboard from "./Dashboard"; // Import the Dashboard component
import NewDashboard from "./NewDashboard";

function App() {
  return (
    <div className="App">
      {/* <Dashboard /> Render the Dashboard component */}
      <NewDashboard />  {/* Render the NewDashboard component */}
    </div>
  );
}

export default App;
