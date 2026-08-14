import api from "./client";

export interface AIChatRequest {
  message: string;
  application_id?: number | null;
}

export interface AIChatResponse {
  answer: string;
  application_id: number | null;
}

export async function chatWithAI(
  payload: AIChatRequest,
): Promise<AIChatResponse> {
  const response = await api.post<AIChatResponse>(
    "/ai/chat",
    payload,
  );

  return response.data;
}
