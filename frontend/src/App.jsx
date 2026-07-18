import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LogInteractionPage from "./features/hcp/LogInteractionPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LogInteractionPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
