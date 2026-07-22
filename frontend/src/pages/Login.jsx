import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";
import "./Login.css";

function Login() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);

    try {
      const response = await api.post("/auth/login", formData);

      localStorage.setItem(
        "access_token",
        response.data.access_token
      );

      navigate("/dashboard");
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Invalid email or password."
      );
    }

    setLoading(false);
  };

  return (
    <div className="login-page">

      <div className="login-card">

        <h2>🔮 Palmistry & Tarot AI</h2>

        <h5>Intelligence Platform</h5>

        <form onSubmit={handleSubmit}>

          <div className="mb-3">

            <label>Email Address</label>

            <input
              type="email"
              name="email"
              className="form-control"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              required
            />

          </div>

          <div className="mb-4">

            <label>Password</label>

            <input
              type="password"
              name="password"
              className="form-control"
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleChange}
              required
            />

          </div>

          <button
            type="submit"
            className="login-btn"
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </button>

        </form>

        <div className="register-link">
          Don't have an account?{" "}
          <Link to="/register">
            Register
          </Link>
        </div>

      </div>

    </div>
  );
}

export default Login;