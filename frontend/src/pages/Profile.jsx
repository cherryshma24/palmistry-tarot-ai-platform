import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Navbar from "../components/Navbar";
import "./Profile.css";

function Profile() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        navigate("/");
        return;
      }

      try {
        const response = await api.get("/auth/profile", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setUser(response.data);
      } catch (error) {
        console.error(error);
        localStorage.removeItem("access_token");
        navigate("/");
      }
    };

    fetchProfile();
  }, [navigate]);

  return (
    <>
      <Navbar />

      <div className="profile-page">

        <div className="profile-card">

          <h2>👤 My Profile</h2>

          {user ? (
            <div className="profile-info">

              <p><strong>🆔 User ID:</strong> {user.id}</p>

              <p><strong>👤 Full Name:</strong> {user.full_name}</p>

              <p><strong>📧 Email:</strong> {user.email}</p>

              <p><strong>🛡 Role:</strong> {user.role}</p>

              <button
                className="back-btn"
                onClick={() => navigate("/dashboard")}
              >
                ⬅ Back to Dashboard
              </button>

            </div>
          ) : (
            <h4>Loading Profile...</h4>
          )}

        </div>

      </div>
    </>
  );
}

export default Profile;