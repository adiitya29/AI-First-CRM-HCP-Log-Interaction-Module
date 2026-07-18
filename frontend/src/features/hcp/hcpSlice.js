import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

const API_BASE = "http://localhost:8000/api/v1/hcp";

export const fetchHcps = createAsyncThunk("hcp/fetchHcps", async (_, { rejectWithValue }) => {
  try {
    const response = await axios.get(`${API_BASE}/professionals/`);
    return response.data;
  } catch (err) {
    return rejectWithValue(err.response?.data || "Failed to fetch HCPs");
  }
});

export const createInteraction = createAsyncThunk("hcp/createInteraction", async (interactionData, { rejectWithValue }) => {
  try {
    const response = await axios.post(`${API_BASE}/interactions/`, interactionData);
    return response.data;
  } catch (err) {
    return rejectWithValue(err.response?.data || "Failed to create interaction");
  }
});

export const chatWithAI = createAsyncThunk("hcp/chatWithAI", async (message, { rejectWithValue }) => {
  try {
    const response = await axios.post(`${API_BASE}/chat/`, { message });
    return response.data; // Expected format: { status: "success", parsed_data: { ... } }
  } catch (err) {
    return rejectWithValue(err.response?.data?.error || "AI chat failed");
  }
});

const initialState = {
  hcps: [],
  interactions: [],
  chatMessages: [],
  parsedAiData: null, // Holds the structured data returned by AI
  status: "idle", // 'idle' | 'loading' | 'succeeded' | 'failed'
  error: null,
};

const hcpSlice = createSlice({
  name: "hcp",
  initialState,
  reducers: {
    clearError(state) {
      state.error = null;
    },
    clearParsedAiData(state) {
      state.parsedAiData = null;
    },
    addChatMessage(state, action) {
      state.chatMessages.push(action.payload);
    }
  },
  extraReducers: (builder) => {
    builder
      // fetchHcps
      .addCase(fetchHcps.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchHcps.fulfilled, (state, action) => {
        state.status = "succeeded";
        // Handle paginated response ({ count, next, previous, results }) or flat array
        state.hcps = action.payload.results || action.payload || [];
      })
      .addCase(fetchHcps.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload;
      })
      // createInteraction
      .addCase(createInteraction.pending, (state) => {
        state.status = "loading";
      })
      .addCase(createInteraction.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.interactions.unshift(action.payload);
        state.parsedAiData = null; // Clear AI parsed data after successful log
      })
      .addCase(createInteraction.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload;
      })
      // chatWithAI
      .addCase(chatWithAI.pending, (state) => {
        state.status = "loading";
      })
      .addCase(chatWithAI.fulfilled, (state, action) => {
        state.status = "succeeded";
        if (action.payload.parsed_data) {
          state.parsedAiData = action.payload.parsed_data;
        }
      })
      .addCase(chatWithAI.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload;
      });
  },
});

export const { clearError, clearParsedAiData, addChatMessage } = hcpSlice.actions;
export default hcpSlice.reducer;
