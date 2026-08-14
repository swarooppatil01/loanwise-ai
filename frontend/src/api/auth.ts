import apiClient from "./client";

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: "user" | "admin";
  is_active: boolean;
}

export interface RegisterPayload {
  email: string;
  full_name: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export async function register(
  payload: RegisterPayload,
): Promise<User> {
  const response = await apiClient.post<User>(
    "/auth/register",
    payload,
  );

  return response.data;
}

export async function login(
  email: string,
  password: string,
): Promise<TokenResponse> {
  const body = new URLSearchParams();

  body.append("username", email);
  body.append("password", password);

  const response = await apiClient.post<TokenResponse>(
    "/auth/login",
    body,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    },
  );

  return response.data;
}

export async function getCurrentUser(): Promise<User> {
  const response = await apiClient.get<User>("/auth/me");

  return response.data;
}

export type UserResponse = User;

export async function getMe(): Promise<User> {
  return getCurrentUser();
}
