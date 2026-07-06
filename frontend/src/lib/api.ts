/*
import axios from "axios";

export const API_BASE_URL = "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface GenerateResponse {
  success: boolean;
  filename?: string;
  download_url?: string;
  message: string;
}

export async function generateForm93(payload: unknown): Promise<GenerateResponse> {
  const { data } = await api.post<GenerateResponse>("/generate", payload);
  return data;
}

export function downloadUrlFor(path: string): string {
  return `${API_BASE_URL}${path}`;
}
*/
import axios from "axios";

export const API_BASE_URL = "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function generateForm93(payload: unknown): Promise<void> {
  const response = await api.post("/generate", payload, {
    responseType: "blob",
  });

  // Get filename from backend (if available)
  const disposition = response.headers["content-disposition"];
  let filename = "new_pan_application.pdf";

  if (disposition) {
    const match = disposition.match(/filename="(.+)"/);
    if (match) {
      filename = match[1];
    }
  }

  const blob = new Blob([response.data], {
    type: "application/pdf",
  });

  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = filename;

  document.body.appendChild(a);
  a.click();

  a.remove();
  window.URL.revokeObjectURL(url);
}