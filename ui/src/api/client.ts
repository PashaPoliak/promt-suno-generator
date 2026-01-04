import axios from "axios";

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      REACT_APP_API_URL: string;
    }
  }
}

const API_BASE = "https://promt-suno-generator.onrender.com";
export const api = axios.create({ baseURL: API_BASE });