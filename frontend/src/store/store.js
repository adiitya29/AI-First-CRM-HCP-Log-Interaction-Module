import { configureStore } from "@reduxjs/toolkit";
import hcpReducer from "../features/hcp/hcpSlice";

export const store = configureStore({
  reducer: {
    hcp: hcpReducer,
  },
});
