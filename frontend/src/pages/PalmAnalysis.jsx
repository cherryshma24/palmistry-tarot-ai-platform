import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaHome,
  FaHandSparkles,
  FaStar,
  FaChartLine,
  FaUserCircle,
  FaSignOutAlt,
  FaCloudUploadAlt,
  FaRobot,
  FaCheckCircle,
} from "react-icons/fa";

import api from "../services/api";
import "./PalmAnalysis.css";

function PalmAnalysis() {
  const navigate = useNavigate();

  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);

  // ============================================================
  // IMAGE SELECTION
  // ============================================================

  const handleImage = (e) => {
    const file = e.target.files?.[0];

    if (!file) return;

    if (!file.type.startsWith("image/")) {
      alert("Please select a valid image file.");
      return;
    }

    setImage(file);

    const imageUrl = URL.createObjectURL(file);
    setPreview(imageUrl);
  };

  // ============================================================
  // PALM ANALYSIS
  // ============================================================

  const analyzePalm = async () => {
    if (!image) {
      alert("Please upload your palm image.");
      return;
    }

    const token = localStorage.getItem("access_token");

    const formData = new FormData();
    formData.append("file", image);

    try {
      setLoading(true);

      console.log("=================================");
      console.log("Sending palm image to backend...");
      console.log("File:", image.name);
      console.log("Size:", image.size);
      console.log("=================================");

      const response = await api.post(
        "/palm/analyze",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log("=================================");
      console.log("PALM ANALYSIS SUCCESS");
      console.log(response.data);
      console.log("=================================");

      // Save complete backend response
      localStorage.setItem(
        "analysis_result",
        JSON.stringify(response.data)
      );

      // Save uploaded image for report page
      const reader = new FileReader();

      reader.onloadend = () => {
        localStorage.setItem(
          "palm_image",
          reader.result
        );

        navigate("/report");
      };

      reader.readAsDataURL(image);

    } catch (error) {
      console.error("PALM ANALYSIS ERROR:", error);

      if (error.response) {
        console.error(
          "Backend response:",
          error.response.data
        );

        alert(
          error.response.data?.detail ||
            "Palm analysis failed."
        );

      } else if (error.request) {
        alert(
          "Cannot connect to the backend. Make sure FastAPI is running."
        );

      } else {
        alert("Palm analysis failed.");
      }

    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // LOGOUT
  // ============================================================

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("analysis_result");
    localStorage.removeItem("palm_image");

    navigate("/");
  };

  // ============================================================
  // UI
  // ============================================================

  return (
    <div className="palm-analysis-page">

      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <aside className="sidebar">

        <div className="sidebar-logo">
          🔮 <span>PalmAI</span>
        </div>

        <nav className="sidebar-nav">

          <button
            onClick={() => navigate("/dashboard")}
          >
            <FaHome />
            <span>Dashboard</span>
          </button>

          <button
            className="active"
            onClick={() => navigate("/palm-upload")}
          >
            <FaHandSparkles />
            <span>Palm Analysis</span>
          </button>

          <button
            onClick={() => navigate("/tarot")}
          >
            <FaStar />
            <span>Tarot Reading</span>
          </button>

          <button
            onClick={() => navigate("/report")}
          >
            <FaChartLine />
            <span>Reports</span>
          </button>

          <button
            onClick={() => navigate("/profile")}
          >
            <FaUserCircle />
            <span>Profile</span>
          </button>

        </nav>

        <button
          className="logout-btn"
          onClick={handleLogout}
        >
          <FaSignOutAlt />
          <span>Logout</span>
        </button>

      </aside>


      {/* ======================================================
          MAIN CONTENT
      ====================================================== */}

      <main className="palm-main">

        {/* HEADER */}

        <header className="palm-header">

          <div className="header-icon">
            ✋
          </div>

          <div>

            <h1>
              AI Palm Analysis
            </h1>

            <p>
              Upload your palm image and let our AI analyze
              your hand structure, palm lines and features.
            </p>

          </div>

        </header>


        {/* ====================================================
            AI INFORMATION
        ==================================================== */}

        <section className="ai-info-card">

          <div className="ai-info-icon">
            <FaRobot />
          </div>

          <div className="ai-info-content">

            <h2>
              Artificial Intelligence Vision
            </h2>

            <p>
              Our computer vision pipeline combines
              MediaPipe, OpenCV and YOLOv8 Pose to analyze
              your palm. OpenRouter AI then transforms the
              extracted features into personalized insights.
            </p>

            <div className="technology-list">

              <span>
                <FaCheckCircle />
                MediaPipe
              </span>

              <span>
                <FaCheckCircle />
                OpenCV
              </span>

              <span>
                <FaCheckCircle />
                YOLOv8
              </span>

              <span>
                <FaCheckCircle />
                OpenRouter AI
              </span>

            </div>

          </div>

        </section>


        {/* ====================================================
            UPLOAD CARD
        ==================================================== */}

        <section className="upload-card">

          <div className="upload-card-header">

            <h2>
              Upload Your Palm Image
            </h2>

            <p>
              Use a clear, well-lit image of your dominant palm
              with the complete hand visible.
            </p>

          </div>


          {/* Hidden Input */}

          <input
            id="palm-upload"
            type="file"
            accept="image/*"
            hidden
            onChange={handleImage}
          />


          {/* Upload Area */}

          <label
            htmlFor="palm-upload"
            className={`upload-area ${
              preview ? "has-preview" : ""
            }`}
          >

            {preview ? (

              <div className="preview-container">

                <img
                  src={preview}
                  alt="Palm Preview"
                  className="palm-preview"
                />

                <div className="file-info">

                  <strong>
                    {image?.name}
                  </strong>

                  <span>
                    {(
                      image?.size /
                      1024 /
                      1024
                    ).toFixed(2)} MB
                  </span>

                  <small>
                    Click to choose another image
                  </small>

                </div>

              </div>

            ) : (

              <div className="upload-placeholder">

                <FaCloudUploadAlt
                  className="upload-icon"
                />

                <h3>
                  Click to Upload Palm Image
                </h3>

                <p>
                  JPG / PNG / JPEG
                </p>

                <small>
                  High resolution image recommended
                </small>

              </div>

            )}

          </label>


          {/* Analyze Button */}

          <button
            className="analyze-btn"
            onClick={analyzePalm}
            disabled={loading || !image}
          >

            {loading ? (
              <>
                <span className="spinner"></span>
                AI Analyzing...
              </>
            ) : (
              <>
                <FaRobot />
                Start AI Analysis
              </>
            )}

          </button>


          {/* Loading Status */}

          {loading && (

            <div className="analysis-status">

              <div>
                <FaCheckCircle />
                Detecting hand landmarks...
              </div>

              <div>
                <FaCheckCircle />
                Analyzing palm lines with YOLOv8...
              </div>

              <div>
                <FaCheckCircle />
                Generating AI interpretation...
              </div>

            </div>

          )}

        </section>


        {/* ====================================================
            ANALYSIS PIPELINE
        ==================================================== */}

        <section className="pipeline-card">

          <h2>
            🔬 AI Analysis Pipeline
          </h2>

          <div className="pipeline-grid">

            <div className="pipeline-item">

              <span>01</span>

              <h3>
                Image Processing
              </h3>

              <p>
                OpenCV enhances and preprocesses
                the uploaded palm image.
              </p>

            </div>


            <div className="pipeline-item">

              <span>02</span>

              <h3>
                Hand Detection
              </h3>

              <p>
                MediaPipe detects 21 hand
                landmarks.
              </p>

            </div>


            <div className="pipeline-item">

              <span>03</span>

              <h3>
                Palm Line Detection
              </h3>

              <p>
                YOLOv8 Pose identifies major
                palm lines.
              </p>

            </div>


            <div className="pipeline-item">

              <span>04</span>

              <h3>
                AI Interpretation
              </h3>

              <p>
                OpenRouter generates personalized
                palmistry insights.
              </p>

            </div>

          </div>

        </section>


        {/* FOOTER */}

        <footer className="palm-footer">

          <strong>
            Palmistry & Tarot Intelligence Platform
          </strong>

          <span>
            React • FastAPI • OpenCV • MediaPipe • YOLOv8 • OpenRouter AI
          </span>

        </footer>

      </main>

    </div>
  );
}

export default PalmAnalysis;
