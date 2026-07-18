import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchHcps } from "../hcpSlice";
import { Card, CardHeader, CardTitle, CardContent, Input, Label, Textarea, Select, Button } from "../../../components/ui";

const InteractionForm = () => {
  const dispatch = useDispatch();
  const { hcps, parsedAiData } = useSelector((state) => state.hcp);

  useEffect(() => {
    dispatch(fetchHcps());
  }, [dispatch]);

  // If AI Assistant has parsed data, we can autofill the form with it
  const defaultValues = parsedAiData || {};

  return (
    <Card className="flex-1">
      <CardHeader>
        <CardTitle>Interaction Details</CardTitle>
      </CardHeader>
      
      <CardContent>
        {/* Row 1: HCP & Interaction Type */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label>HCP Name</Label>
            <Select defaultValue={defaultValues.hcp_name || ""}>
              <option value="" disabled>Search or select HCP...</option>
              {hcps.map((hcp) => (
                <option key={hcp.id} value={hcp.id}>
                  {hcp.first_name} {hcp.last_name} - {hcp.specialty}
                </option>
              ))}
            </Select>
          </div>
          <div>
            <Label>Interaction Type</Label>
            <Select defaultValue={defaultValues.interaction_type || "in_person"}>
              <option value="in_person">In-Person Meeting</option>
              <option value="virtual">Virtual Meeting</option>
              <option value="phone">Phone Call</option>
              <option value="email">Email</option>
              <option value="event">Event/Conference</option>
            </Select>
          </div>
        </div>

        {/* Row 2: Date & Time */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label>Date</Label>
            <Input type="date" defaultValue={defaultValues.date || ""} />
          </div>
          <div>
            <Label>Time</Label>
            <Input type="time" />
          </div>
        </div>

        {/* Attendees */}
        <div>
          <Label>Attendees</Label>
          <Input placeholder="Enter names or search..." />
        </div>

        {/* Topics Discussed */}
        <div>
          <Label>Topics Discussed</Label>
          <Textarea 
            placeholder="Enter key discussion points..." 
            defaultValue={defaultValues.notes || ""}
          />
          <div className="mt-2">
            <Button variant="secondary" className="text-xs">
              ✨ Summarize from Voice Note (Requires Consent)
            </Button>
          </div>
        </div>

        {/* Materials & Samples */}
        <div className="flex-col gap-2">
          <Label>Materials Shared / Samples Distributed</Label>
          
          <div className="glass-panel" style={{ padding: '1rem', borderRadius: 'var(--radius-md)', marginBottom: '0.5rem' }}>
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium">Materials Shared</span>
              <Button variant="outline" className="text-xs">🔍 Search/Add</Button>
            </div>
            <p className="text-xs text-muted italic">No materials added.</p>
            {defaultValues.products_discussed?.length > 0 && (
              <div className="mt-2 text-sm text-primary">
                AI extracted products: {defaultValues.products_discussed.join(", ")}
              </div>
            )}
          </div>

          <div className="glass-panel" style={{ padding: '1rem', borderRadius: 'var(--radius-md)' }}>
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium">Samples Distributed</span>
              <Button variant="outline" className="text-xs">📦 Add Sample</Button>
            </div>
            <p className="text-xs text-muted italic">No samples added.</p>
          </div>
        </div>

        {/* Sentiment */}
        <div>
          <Label>Observed/Inferred HCP Sentiment</Label>
          <div className="flex gap-4 mt-2">
            {["positive", "neutral", "negative"].map((sent) => (
              <label key={sent} className="flex items-center gap-1 text-sm cursor-pointer">
                <input 
                  type="radio" 
                  name="sentiment" 
                  value={sent} 
                  defaultChecked={(defaultValues.ai_sentiment || "neutral") === sent} 
                />
                <span className="capitalize">{sent}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Outcomes */}
        <div>
          <Label>Outcomes</Label>
          <Textarea placeholder="Key outcomes or agreements..." />
        </div>

        {/* Follow-up */}
        <div>
          <Label>Follow-up Actions</Label>
          <Textarea 
            placeholder="Enter next steps or tasks..." 
            defaultValue={defaultValues.follow_up_required ? `Follow up on: ${defaultValues.follow_up_date || 'TBD'}` : ""}
          />
        </div>

        {/* AI Suggestions */}
        <div>
          <Label className="text-primary">✨ AI Suggested Follow-ups:</Label>
          <ul className="text-sm mt-1" style={{ color: 'hsl(var(--color-primary))', paddingLeft: '1rem' }}>
            <li className="cursor-pointer hover:underline mb-1">Schedule follow-up meeting in 2 weeks</li>
            <li className="cursor-pointer hover:underline mb-1">Send OncoBoost Phase III PDF</li>
            <li className="cursor-pointer hover:underline">Add to advisory board invite list</li>
          </ul>
        </div>

      </CardContent>
    </Card>
  );
};

export default InteractionForm;
