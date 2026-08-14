import { create } from "zustand";
import type { UserResponse } from "../api/auth";

interface AuthState {
  user: UserResponse | null;
  token: string | null;
  setAuth: (token: string, user: UserResponse) => void;
  setUser: (user: UserResponse) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: localStorage.getItem("loanwise_access_token"),

  setAuth: (token, user) => {
    localStorage.setItem("loanwise_access_token", token);

    set({
      token,
      user,
    });
  },

  setUser: (user) => {
    set({ user });
  },

  logout: () => {
    localStorage.removeItem("loanwise_access_token");

    set({
      token: null,
      user: null,
    });
  },
}));
