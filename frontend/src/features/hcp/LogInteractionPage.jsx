import React from "react";
import InteractionForm from "./components/InteractionForm";
import AiAssistantChat from "./components/AiAssistantChat";

const LogInteractionPage = () => {
  return (
    <div className="flex flex-col h-full min-h-screen" style={{ backgroundColor: "var(--color-background)", padding: "2rem" }}>
      <h1 className="text-2xl font-bold mb-6" style={{ color: "hsl(var(--color-text))" }}>
        Log HCP Interaction
      </h1>
      
      <div 
        className="grid gap-6" 
        style={{ 
          gridTemplateColumns: "1fr 350px", 
          alignItems: "start",
          flex: 1
        }}
      >
        {/* Left Pane: Structured Form */}
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
          <InteractionForm />
        </div>

        {/* Right Pane: Sticky AI Assistant Chat */}
        <div style={{ position: "sticky", top: "2rem", height: "calc(100vh - 4rem)", minHeight: "500px" }}>
          <AiAssistantChat />
        </div>
      </div>
    </div>
  );
};

export default LogInteractionPage;
