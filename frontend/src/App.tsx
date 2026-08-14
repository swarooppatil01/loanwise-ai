import { useEffect } from "react";
import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import { getMe } from "./api/auth";
import { useAuthStore } from "./stores/authStore";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import ApplyLoan from "./pages/ApplyLoan";
import Recommendations from "./pages/Recommendations";
import AIAssistant from "./pages/AIAssistant";

import ProtectedRoute from "./routes/ProtectedRoute";

function AppRoutes() {
  const setUser = useAuthStore((state) => state.setUser);
  const token = useAuthStore((state) => state.token);

  useEffect(() => {
    if (!token) return;

    getMe()
      .then(setUser)
      .catch(() => {
        localStorage.removeItem("loanwise_access_token");
      });
  }, [token, setUser]);

  return (
    <Routes>
      <Route
        path="/"
        element={<Navigate to="/dashboard" replace />}
      />

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/register"
        element={<Register />}
      />

      <Route element={<ProtectedRoute />}>
        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/profile"
          element={<Profile />}
        />

        <Route
          path="/apply"
          element={<ApplyLoan />}
        />

        <Route
          path="/recommendations/:applicationId"
          element={<Recommendations />}
        />

        <Route
          path="/ai"
          element={<AIAssistant />}
        />
      </Route>

      <Route
        path="*"
        element={<Navigate to="/dashboard" replace />}
      />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}
