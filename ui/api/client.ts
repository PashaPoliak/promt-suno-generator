import axios from "axios";
import { ClipDTO, PlaylistDTO, ProfileDTO } from "./types";

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      REACT_APP_API_URL: string;
    }
  }
}

const API_BASE = process.env.REACT_APP_API_URL ?? "http://localhost:8000/api/v1";
export const api = axios.create({ baseURL: API_BASE });