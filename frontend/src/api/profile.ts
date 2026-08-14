import apiClient from "./client";

export type EmploymentType =
  | "salaried"
  | "self_employed"
  | "professional"
  | "business_owner"
  | "other";

export interface Profile {
  id: number;
  user_id: number;
  age: number | null;
  city: string | null;
  employment_type: EmploymentType | null;
  monthly_income: string | null;
  monthly_obligations: string | null;
  credit_score: number | null;
  employment_duration_months: number | null;
}

export interface ProfilePayload {
  age?: number | null;
  city?: string | null;
  employment_type?: EmploymentType | null;
  monthly_income?: number | null;
  monthly_obligations?: number | null;
  credit_score?: number | null;
  employment_duration_months?: number | null;
}

export async function getProfile(): Promise<Profile | null> {
  const response = await apiClient.get<Profile | null>("/profile");

  return response.data;
}

export async function updateProfile(
  payload: ProfilePayload,
): Promise<Profile> {
  const response = await apiClient.put<Profile>(
    "/profile",
    payload,
  );

  return response.data;
}
