import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaHome,
  FaHandPaper,
  FaStar,
  FaChartLine,
  FaUserCircle,
  FaSignOutAlt,
  FaRobot,
  FaUser,
  FaCheckCircle,
} from "react-icons/fa";

import "./Report.css";

function Report() {
  const navigate = useNavigate();

  const [analysis, setAnalysis] = useState(null);
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const result = localStorage.getItem("analysis_result");
    const userProfile = localStorage.getItem("user_profile");

    if (result) setAnalysis(JSON.parse(result));
    if (userProfile) setProfile(JSON.parse(userProfile));
  }, []);

  return (
    <div className="report-layout">

      {/* ================= SIDEBAR ================= */}

      <aside className="sidebar">

        <div className="logo">🔮 PalmAI</div>

        <div className="menu">

          <div
            className="menu-item"
            onClick={() => navigate("/dashboard")}
          >
            <FaHome />
            Dashboard
          </div>

          <div
            className="menu-item"
            onClick={() => navigate("/palm-upload")}
          >
            <FaHandPaper />
            Palm Analysis
          </div>

          <div
            className="menu-item"
            onClick={() => navigate("/tarot")}
          >
            <FaStar />
            Tarot Reading
          </div>

          <div
            className="menu-item active"
            onClick={() => navigate("/report")}
          >
            <FaChartLine />
            Reports
          </div>

          <div
            className="menu-item"
            onClick={() => navigate("/profile")}
          >
            <FaUserCircle />
            Profile
          </div>

        </div>

        <div
          className="logout"
          onClick={() => {
            localStorage.removeItem("access_token");
            navigate("/");
          }}
        >
          <FaSignOutAlt />
          Logout
        </div>

      </aside>

      {/* ================= MAIN ================= */}

      <main className="report-main">

        <header className="report-header">

          <h1>🔮 AI Palmistry Intelligence Report</h1>

          <p>
            Generated using MediaPipe, OpenCV and the AI Interpretation Engine.
            This report combines computer vision, feature extraction and AI-generated insights.
          </p>

        </header>

        {/* ================= AI SUMMARY ================= */}

        <section className="glass-card">

          <h2>
            <FaRobot /> AI Summary
          </h2>

          <p>
            Palm successfully analyzed using computer vision and AI.
            The extracted palm characteristics have been interpreted to generate
            a personalized personality profile and life insights.
          </p>

          <div className="analysis-grid">

            <div className="analysis-item">
              <FaCheckCircle />
              <h3>{analysis?.total_landmarks || 0}</h3>
              <p>Landmarks</p>
            </div>

            <div className="analysis-item">
              <FaCheckCircle />
              <h3>Palm Features</h3>
              <p>Extracted</p>
            </div>

            <div className="analysis-item">
              <FaCheckCircle />
              <h3>AI Report</h3>
              <p>Generated</p>
            </div>

            <div className="analysis-item">
              <FaCheckCircle />
              <h3>
                {analysis?.reading?.confidence ??
                  Math.round(
                    (analysis?.features?.analysis_confidence ?? 0) * 100
                  )}
                %
              </h3>

              <p>AI Confidence</p>

            </div>

          </div>

        </section>

        {/* ================= USER + AI ================= */}

        <section className="report-grid">

          <section className="glass-card">

            <h2>
              <FaUser />
              User Information
            </h2>

            <div className="info-row">
              <span>Name</span>
              <strong>{profile?.full_name || "Not Provided"}</strong>
            </div>

            <div className="info-row">
              <span>Email</span>
              <strong>{profile?.email || "Not Provided"}</strong>
            </div>

            <div className="info-row">
              <span>Age</span>
              <strong>{profile?.age || "-"}</strong>
            </div>

            <div className="info-row">
              <span>Gender</span>
              <strong>{profile?.gender || "-"}</strong>
            </div>

            <div className="info-row">
              <span>Occupation</span>
              <strong>{profile?.occupation || "-"}</strong>
            </div>

          </section>

          <section className="glass-card">

            <h2>
              <FaRobot />
              AI Confidence
            </h2>

            <div className="score-circle">

              <h1>

                {analysis?.reading?.confidence ??
                  Math.round(
                    (analysis?.features?.analysis_confidence ?? 0) * 100
                  )}
                %

              </h1>

              <p>Confidence</p>

            </div>

          </section>

        </section>

        {/* ================= PALM SHAPE ================= */}

        <section className="glass-card">

          <h2>✋ Palm Shape</h2>

          <div className="info-row">
            <span>Shape</span>
            <strong>{analysis?.palm_shape?.shape || "Unknown"}</strong>
          </div>

          <div className="info-row">
            <span>Aspect Ratio</span>
            <strong>{analysis?.palm_shape?.ratio || "-"}</strong>
          </div>

          <div className="info-row">
            <span>Confidence</span>
            <strong>
              {Math.round((analysis?.palm_shape?.confidence || 0) * 100)}%
            </strong>
          </div>

        </section>

        

        

        {/* ================= PALM ANALYSIS ================= */}

<section className="glass-card">

  <h2>🖐 Palm Analysis</h2>

  <div className="analysis-grid">

    {/* LIFE LINE */}
    <div className="analysis-item">

      <h3>❤️ Life Line</h3>

      <p>
        {analysis?.reading?.palm_analysis?.life_line?.interpretation ||
          "No interpretation available."}
      </p>

      <div className="info-row">
        <span>Detection Confidence</span>
        <strong>
          {analysis?.reading?.palm_analysis?.life_line?.confidence_percent ?? 0}%
        </strong>
      </div>

      <div className="info-row">
        <span>Length</span>
        <strong>
          {analysis?.reading?.palm_analysis?.life_line?.length_pixels ?? 0} px
        </strong>
      </div>

      <div className="info-row">
        <span>Angle</span>
        <strong>
          {analysis?.reading?.palm_analysis?.life_line?.angle_degrees ?? 0}°
        </strong>
      </div>

    </div>


    {/* HEART LINE */}
    <div className="analysis-item">

      <h3>💕 Heart Line</h3>

      <p>
        {analysis?.reading?.palm_analysis?.heart_line?.interpretation ||
          "No interpretation available."}
      </p>

      <div className="info-row">
        <span>Detection Confidence</span>
        <strong>
          {analysis?.reading?.palm_analysis?.heart_line?.confidence_percent ?? 0}%
        </strong>
      </div>

      <div className="info-row">
        <span>Length</span>
        <strong>
          {analysis?.reading?.palm_analysis?.heart_line?.length_pixels ?? 0} px
        </strong>
      </div>

      <div className="info-row">
        <span>Angle</span>
        <strong>
          {analysis?.reading?.palm_analysis?.heart_line?.angle_degrees ?? 0}°
        </strong>
      </div>

    </div>


    {/* HEAD LINE */}
    <div className="analysis-item">

      <h3>🧠 Head Line</h3>

      <p>
        {analysis?.reading?.palm_analysis?.head_line?.interpretation ||
          "No interpretation available."}
      </p>

      <div className="info-row">
        <span>Detection Confidence</span>
        <strong>
          {analysis?.reading?.palm_analysis?.head_line?.confidence_percent ?? 0}%
        </strong>
      </div>

      <div className="info-row">
        <span>Length</span>
        <strong>
          {analysis?.reading?.palm_analysis?.head_line?.length_pixels ?? 0} px
        </strong>
      </div>

      <div className="info-row">
        <span>Angle</span>
        <strong>
          {analysis?.reading?.palm_analysis?.head_line?.angle_degrees ?? 0}°
        </strong>
      </div>

    </div>


    {/* FATE LINE */}
    <div className="analysis-item">

      <h3>✨ Fate Line</h3>

      <p>
        {analysis?.reading?.palm_analysis?.fate_line?.interpretation ||
          "No interpretation available."}
      </p>

      <div className="info-row">
        <span>Detection Confidence</span>
        <strong>
          {analysis?.reading?.palm_analysis?.fate_line?.confidence_percent ?? 0}%
        </strong>
      </div>

      <div className="info-row">
        <span>Length</span>
        <strong>
          {analysis?.reading?.palm_analysis?.fate_line?.length_pixels ?? 0} px
        </strong>
      </div>

      <div className="info-row">
        <span>Angle</span>
        <strong>
          {analysis?.reading?.palm_analysis?.fate_line?.angle_degrees ?? 0}°
        </strong>
      </div>

    </div>

  </div>

</section>


        {/* ================= PERSONALITY ================= */}

        <section className="glass-card">

          <h2>🧠 Personality Profile</h2>

          <div className="info-row">
            <span>Traits</span>
            <strong>
              {Array.isArray(analysis?.reading?.personality?.traits)
  ? analysis.reading.personality.traits.join(", ")
  : "-"}
            </strong>
          </div>

          <div className="info-row">
            <span>Strengths</span>
            <strong>
              {Array.isArray(analysis?.reading?.personality?.strengths)
  ? analysis.reading.personality.strengths.join(", ")
  : "-"}
            </strong>
          </div>

          <div className="info-row">
            <span>Growth Areas</span>
            <strong>
              {Array.isArray(analysis?.reading?.personality?.growth_areas)
  ? analysis.reading.personality.growth_areas.join(", ")
  : "-"}
            </strong>
          </div>

        </section>
                {/* ================= AI PREDICTIONS ================= */}

        <section className="glass-card">

          <h2>✨ AI Predictions</h2>

          <div className="prediction">

            <h3>💕 Relationships</h3>

            <p>
              {analysis?.reading?.relationships?.prediction}
            </p>

            <h3>💼 Career</h3>

            <p>
              {analysis?.reading?.career?.prediction}
            </p>

            <h3>💰 Finance</h3>

            <p>
              {analysis?.reading?.finance?.prediction}
            </p>

            <h3>❤️ Health</h3>

            <p>
              {analysis?.reading?.health?.prediction}
            </p>

          </div>

        </section>

        {/* ================= CAREER ANALYSIS ================= */}

        <section className="glass-card">

          <h2>💼 Career Intelligence</h2>

          <div className="info-row">

            <span>Career Score</span>

            <strong>

              {analysis?.reading?.career?.career_score ?? "--"}%

            </strong>

          </div>

          <div className="info-row">

            <span>Suggested Roles</span>

            <strong>

             {Array.isArray(analysis?.reading?.career?.suitable_roles)
  ? analysis.reading.career.suitable_roles.join(", ")
  : "Not Available"}

            </strong>

          </div>

        </section>

        {/* ================= FINANCE ================= */}

        <section className="glass-card">

          <h2>💰 Financial Outlook</h2>

          <p>

            {analysis?.reading?.finance?.money_management}

          </p>

        </section>

        {/* ================= HEALTH ================= */}

        <section className="glass-card">

          <h2>❤️ Wellness Recommendation</h2>

          <p>

            {analysis?.reading?.health?.wellness_tip}

          </p>

        </section>

        {/* ================= AI RECOMMENDATIONS ================= */}

        <section className="glass-card">

          <h2>🎯 AI Recommendations</h2>

          <ul>

            {Array.isArray(analysis?.reading?.recommendations) &&
  analysis.reading.recommendations.map((item,index)=>(

              <li key={index}>{item}</li>

            ))}

          </ul>

        </section>

        {/* ================= FORTUNE ================= */}

        <section className="glass-card fortune">

          <h2>🌟 Overall Fortune Score</h2>

          <div className="fortune-bar">

            <div
              className="fortune-fill"
              style={{
                width: `${analysis?.reading?.fortune_score ?? 0}%`,
              }}
            />

          </div>

          <h1>

            {analysis?.reading?.fortune_score ?? 0}%

          </h1>

          <p>

            {analysis?.reading?.fortune_score >= 90
              ? "Excellent Future Outlook"
              : analysis?.reading?.fortune_score >= 80
              ? "Very Positive Future"
              : analysis?.reading?.fortune_score >= 70
              ? "Good Opportunities Ahead"
              : "Keep Growing"}

          </p>

        </section>

        {/* ================= SUMMARY ================= */}

        <section className="glass-card">

          <h2>📝 AI Overall Summary</h2>

          <p>

            {analysis?.reading?.overall_summary}

          </p>

        </section>

        {/* ================= BUTTONS ================= */}

        <div className="button-group">

          <button
            className="download-btn"
            onClick={() => window.print()}
          >
            Download PDF Report
          </button>

          <button
            className="new-btn"
            onClick={() => {

              localStorage.removeItem("analysis_result");

              navigate("/palm-upload");

            }}
          >
            Start New Reading
          </button>

        </div>

        {/* ================= FOOTER ================= */}

        <footer className="report-footer">

          <p>

            Generated by

            <strong>

              {" "}Palmistry & Tarot Intelligence Platform

            </strong>

          </p>

          <span>

            React • FastAPI • OpenCV • MediaPipe • OpenRouter AI • Computer Vision

          </span>

        </footer>

      </main>

    </div>

  );

}

export default Report;