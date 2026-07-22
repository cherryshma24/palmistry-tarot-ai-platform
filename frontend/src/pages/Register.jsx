import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";

function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    password: "",
    role: "user",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleRegister = async () => {
    try {
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
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">

          <div className="card shadow p-4">

            <h2 className="text-center mb-4">
              Register
            </h2>

            <div className="mb-3">
              <label>Full Name</label>
              <input
                type="text"
                name="full_name"
                className="form-control"
                placeholder="Enter Full Name"
                value={formData.full_name}
                onChange={handleChange}
              />
            </div>

            <div className="mb-3">
              <label>Email</label>
              <input
                type="email"
                name="email"
                className="form-control"
                placeholder="Enter Email"
                value={formData.email}
                onChange={handleChange}
              />
            </div>

            <div className="mb-3">
              <label>Password</label>
              <input
                type="password"
                name="password"
                className="form-control"
                placeholder="Enter Password"
                value={formData.password}
                onChange={handleChange}
              />
            </div>

            <div className="mb-3">
              <label>Role</label>

              <select
                className="form-select"
                name="role"
                value={formData.role}
                onChange={handleChange}
              >
                <option value="user">User</option>
                <option value="admin">Admin</option>
              </select>
            </div>

            <button
              className="btn btn-success w-100"
              onClick={handleRegister}
            >
              Register
            </button>

            <p className="text-center mt-3">
              Already have an account?{" "}
              <Link to="/">Login</Link>
            </p>

          </div>

        </div>
      </div>
    </div>
  );
}

export default Register;