import { useNavigate, useLocation } from "react-router-dom";
import {
  FaHome,
  FaHandPaper,
  FaStar,
  FaChartLine,
  FaUserCircle,
  FaSignOutAlt,
} from "react-icons/fa";

import "./Sidebar.css";

function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  const logout = () => {
    localStorage.removeItem("access_token");
    navigate("/");
  };

  const isActive = (path) => location.pathname === path;

  return (
    <aside className="sidebar">

      <div className="logo">
        🔮 PalmAI
      </div>

      <div className="menu">

        <div
          className={`menu-item ${isActive("/dashboard") ? "active" : ""}`}
          onClick={() => navigate("/dashboard")}
        >
          <FaHome />
          Dashboard
        </div>

        <div
          className={`menu-item ${isActive("/palm-upload") ? "active" : ""}`}
          onClick={() => navigate("/palm-upload")}
        >
          <FaHandPaper />
          Palm Analysis
        </div>

        <div
          className="menu-item"
          onClick={() =>
            alert("Tarot Reading will be available in a future update.")
          }
        >
          <FaStar />
          Tarot Reading
        </div>

        <div
          className={`menu-item ${isActive("/report") ? "active" : ""}`}
          onClick={() => navigate("/report")}
        >
          <FaChartLine />
          Reports
        </div>

        <div
          className={`menu-item ${isActive("/profile") ? "active" : ""}`}
          onClick={() => navigate("/profile")}
        >
          <FaUserCircle />
          Profile
        </div>

      </div>

      <div className="logout" onClick={logout}>
        <FaSignOutAlt />
        Logout
      </div>

    </aside>
  );
}

export default Sidebar;