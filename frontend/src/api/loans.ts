import apiClient from "./client";

export type LoanType =
  | "personal"
  | "home"
  | "education"
  | "vehicle";

export interface LoanProduct {
  id: number;
  name: string;
  lender: string;
  loan_type: LoanType;
  min_amount: string;
  max_amount: string;
  min_income: string;
  min_credit_score: number;
  max_dti: string;
  min_interest_rate: string;
  max_interest_rate: string;
  min_tenure_months: number;
  max_tenure_months: number;
  processing_fee_percent: string;
  employment_types: string;
  special_conditions: string | null;
  is_active: boolean;
}

export async function getLoans(
  loanType?: LoanType,
): Promise<LoanProduct[]> {
  const response = await apiClient.get<LoanProduct[]>(
    "/loans",
    {
      params: loanType
        ? { loan_type: loanType }
        : undefined,
    },
  );

  return response.data;
}

export async function getLoan(
  loanId: number,
): Promise<LoanProduct> {
  const response = await apiClient.get<LoanProduct>(
    `/loans/${loanId}`,
  );

  return response.data;
}
