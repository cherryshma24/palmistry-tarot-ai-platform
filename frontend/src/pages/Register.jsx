import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";
import "./Register.css";

function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    password: "",
    role: "user",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    if (!formData.full_name || !formData.email || !formData.password) {
      alert("Please fill in all required fields.");
      return;
    }

    try {
      setLoading(true);

      const response = await api.post("/auth/register", formData);

      alert(response.data.message || "Registration successful!");

      navigate("/");
    } catch (error) {
      console.error(error);

      if (error.response) {
        alert(error.response.data.detail || "Registration failed");
      } else {
        alert("Something went wrong!");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-page">
      <div className="register-glow glow-one"></div>
      <div className="register-glow glow-two"></div>

      <div className="register-container">

        {/* Left visual section */}
        <div className="register-visual">
          <div className="visual-overlay"></div>

          <div className="visual-content">
            <div className="brand-symbol">✦</div>

            <h1>
              Discover Your
              <span> Inner Story</span>
            </h1>

            <p>
              Explore palm insights, tarot symbolism, and AI-powered
              personality intelligence in one place.
            </p>

            <div className="visual-features">
              <div>
                <span>✋</span>
                <p>Palm Intelligence</p>
              </div>

              <div>
                <span>🃏</span>
                <p>Tarot Insights</p>
              </div>

              <div>
                <span>✦</span>
                <p>AI Interpretation</p>
              </div>
            </div>
          </div>
        </div>

        {/* Register section */}
        <div className="register-form-section">
          <div className="register-card">

            <div className="register-header">
              <div className="small-title">WELCOME</div>

              <h2>Create Your Account</h2>

              <p>
                Begin your personal intelligence journey
              </p>
            </div>

            <form onSubmit={handleRegister}>

              <div className="input-group">
                <label htmlFor="full_name">Full Name</label>

                <input
                  id="full_name"
                  type="text"
                  name="full_name"
                  placeholder="Enter your full name"
                  value={formData.full_name}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="input-group">
                <label htmlFor="email">Email Address</label>

                <input
                  id="email"
                  type="email"
                  name="email"
                  placeholder="Enter your email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="input-group">
                <label htmlFor="password">Password</label>

                <input
                  id="password"
                  type="password"
                  name="password"
                  placeholder="Create a password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="input-group">
                <label htmlFor="role">Account Type</label>

                <select
                  id="role"
                  name="role"
                  value={formData.role}
                  onChange={handleChange}
                >
                  <option value="user">User</option>
                  <option value="admin">Admin</option>
                </select>
              </div>

              <button
                type="submit"
                className="register-button"
                disabled={loading}
              >
                {loading ? "Creating Account..." : "Create Account"}
              </button>

            </form>

            <div className="login-link">
              Already have an account?
              <Link to="/"> Sign in</Link>
            </div>

          </div>
        </div>

      </div>
    </div>
  );
}

export default Register;