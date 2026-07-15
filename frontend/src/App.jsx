import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Pages (stubbed – real pages added in next milestones)
const Home = () => (
  <div style={{ padding: "2rem", textAlign: "center" }}>
    <h1 style={{ fontSize: "2rem", color: "var(--color-primary)", marginBottom: "1rem" }}>
      🧬 AI-First CRM – HCP Module
    </h1>
    <p style={{ color: "var(--text-secondary)" }}>
      Backend: <strong>Django + Supabase PostgreSQL</strong> &nbsp;|&nbsp;
      AI: <strong>LangGraph + Groq (gemma2-9b-it)</strong>
    </p>
    <p style={{ marginTop: "0.5rem", color: "var(--text-muted)" }}>
      Frontend scaffold is ready. Full UI coming in the next milestone.
    </p>
  </div>
);

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        {/* Interaction log route – wired up in Milestone 3 */}
        {/* <Route path="/log-interaction" element={<LogInteractionPage />} /> */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
