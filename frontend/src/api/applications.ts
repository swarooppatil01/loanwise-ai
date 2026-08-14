import apiClient from "./client";
import type { LoanProduct } from "./loans";

export type ApplicationStatus =
  | "draft"
  | "submitted"
  | "processed"
  | "failed";

export interface RecommendationFactor {
  id: number;
  factor: string;
  value: string;
  weight: string;
  contribution: string;
  reason: string;
}

export interface Recommendation {
  id: number;
  application_id: number;
  loan_product_id: number;
  score: string;
  rank: number;
  eligible: boolean;
  explanation: string | null;
  loan_product: LoanProduct;
  factors: RecommendationFactor[];
}

export interface LoanApplication {
  id: number;
  user_id: number;
  loan_type: string;
  loan_amount: string;
  preferred_tenure_months: number;
  purpose: string;
  status: ApplicationStatus;
  recommendations: Recommendation[];
}

export interface CreateApplicationPayload {
  loan_type: string;
  loan_amount: number;
  preferred_tenure_months: number;
  purpose: string;
}

export async function createApplication(
  payload: CreateApplicationPayload,
): Promise<LoanApplication> {
  const response = await apiClient.post<LoanApplication>(
    "/applications",
    payload,
  );

  return response.data;
}

export async function getApplications(): Promise<LoanApplication[]> {
  const response = await apiClient.get<LoanApplication[]>(
    "/applications",
  );

  return response.data;
}

export async function getApplication(
  applicationId: number,
): Promise<LoanApplication> {
  const response = await apiClient.get<LoanApplication>(
    `/applications/${applicationId}`,
  );

  return response.data;
}

export async function getRecommendations(
  applicationId: number,
): Promise<Recommendation[]> {
  const response = await apiClient.get<Recommendation[]>(
    `/applications/${applicationId}/recommendations`,
  );

  return response.data;
}
