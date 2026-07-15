/**
 * HCP feature slice – scaffold.
 * Full thunks and state shape will be added in the next milestone.
 */
import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  hcps: [],
  interactions: [],
  chatMessages: [],
  activeMode: "form", // "form" | "chat"
  loading: false,
  error: null,
};

const hcpSlice = createSlice({
  name: "hcp",
  initialState,
  reducers: {
    setActiveMode(state, action) {
      state.activeMode = action.payload;
    },
    clearError(state) {
      state.error = null;
    },
  },
});

export const { setActiveMode, clearError } = hcpSlice.actions;
export default hcpSlice.reducer;
