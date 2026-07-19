import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { chatWithAI } from "../hcpSlice";
import { Card, CardHeader, CardTitle, CardContent, Input, Button } from "../../../components/ui";

const AiAssistantChat = () => {
  const [inputMsg, setInputMsg] = useState("");
  const dispatch = useDispatch();
  const { status, error } = useSelector((state) => state.hcp);

  const handleSend = () => {
    if (!inputMsg.trim()) return;
    dispatch(chatWithAI(inputMsg));
    setInputMsg("");
  };

  return (
    <Card style={{ height: "100%" }}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <span>🧠</span> AI Assistant
        </CardTitle>
        <p className="text-xs text-muted mt-1">Log interaction via chat</p>
      </CardHeader>
      
      <CardContent style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
        
        {/* Chat History / Instructions Area */}
        <div className="flex-1" style={{ overflowY: "auto", display: "flex", flexDirection: "column", gap: "1rem" }}>
          
          {/* Default Instruction Bubble */}
          <div className="glass-panel" style={{ padding: '1rem', borderRadius: 'var(--radius-lg) var(--radius-lg) var(--radius-lg) 0', alignSelf: 'flex-start', maxWidth: '90%' }}>
            <p className="text-sm">
              Describe the interaction below...
            </p>
          </div>
          
          {/* (Future enhancement: Render chat messages from Redux store here) */}
          
          {status === "loading" && (
            <div className="text-sm text-primary animate-pulse">AI is thinking...</div>
          )}
          {error && (
            <div className="text-sm" style={{ color: 'hsl(var(--color-error))' }}>Error: {error}</div>
          )}
        </div>

        {/* Input Area */}
        <div className="flex gap-2 mt-4 pt-4 border-t" style={{ borderColor: 'hsl(var(--color-border))' }}>
          <Input 
            value={inputMsg}
            onChange={(e) => setInputMsg(e.target.value)}
            placeholder="Describe interaction..." 
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <Button 
            variant="primary" 
            onClick={handleSend}
            disabled={status === "loading"}
          >
            Log
          </Button>
        </div>
        
      </CardContent>
    </Card>
  );
};

export default AiAssistantChat;
