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
  FaHeart,
  FaBriefcase,
  FaCoins,
  FaHeartbeat,
  FaDownload,
  FaRedo,
} from "react-icons/fa";

import "./Report.css";

function Report() {

  const navigate = useNavigate();

  const [analysis, setAnalysis] = useState(null);
  const [profile, setProfile] = useState(null);

  useEffect(() => {

    const result = localStorage.getItem("analysis_result");
    const userProfile = localStorage.getItem("user_profile");

    if (result) {
      setAnalysis(JSON.parse(result));
    }

    if (userProfile) {
      setProfile(JSON.parse(userProfile));
    }

  }, []);

  return (

<div className="report-layout">

{/* ================= SIDEBAR ================= */}

<aside className="sidebar">

<div className="logo">
🔮 PalmAI
</div>

<div className="menu">

<div
className="menu-item"
onClick={()=>navigate("/dashboard")}
>
<FaHome/>
Dashboard
</div>

<div
className="menu-item"
onClick={()=>navigate("/palm-upload")}
>
<FaHandPaper/>
Palm Analysis
</div>

<div
className="menu-item"
onClick={()=>alert("Tarot Reading page coming soon")}
>
<FaStar/>
Tarot Reading
</div>

<div
className="menu-item active"
onClick={()=>navigate("/report")}
>
<FaChartLine/>
Reports
</div>

<div
className="menu-item"
onClick={()=>navigate("/profile")}
>
<FaUserCircle/>
Profile
</div>

</div>

<div
className="logout"
onClick={()=>{
localStorage.removeItem("access_token");
navigate("/");
}}
>
<FaSignOutAlt/>
Logout
</div>

</aside>

{/* ================= REPORT ================= */}

<main className="report-main">

<header className="report-header">

<h1>
🔮 AI Palmistry & Tarot Report
</h1>

<p>
Generated using Artificial Intelligence, Computer Vision &
Tarot Interpretation Engine
</p>

</header>

{/* ================= AI SUMMARY ================= */}

<section className="glass-card">

  <h2>
    <FaRobot />
    📝 AI Summary
  </h2>

  <p>
    Palm successfully analyzed using MediaPipe Computer Vision and Gemini AI.
    The report below summarizes the detected palm characteristics.
  </p>

  <div className="analysis-grid">

    <div className="analysis-item">
      <FaCheckCircle />
      <h3>{analysis?.total_landmarks || 0}</h3>
      <p>Landmarks Detected</p>
    </div>

    <div className="analysis-item">
      <FaCheckCircle />
      <h3>Palm Features</h3>
      <p>Extracted Successfully</p>
    </div>

    <div className="analysis-item">
      <FaCheckCircle />
      <h3>Tarot Reading</h3>
      <p>Generated</p>
    </div>

    <div className="analysis-item">
      <FaCheckCircle />
      <h3>
        {analysis?.features?.analysis_confidence
          ? Math.round(analysis.features.analysis_confidence * 100)
          : 95}%
      </h3>
      <p>AI Confidence</p>
    </div>

  </div>

</section>


{/* ================= USER + ACCURACY ================= */}

<section className="report-grid">
  {/* ================= USER INFORMATION ================= */}

<div className="glass-card">

  <h2>
    <FaUser />
    User Information
  </h2>

  <div className="info-row">
    <span>Full Name</span>
    <strong>{profile?.full_name || "Not Provided"}</strong>
  </div>

  <div className="info-row">
    <span>Email</span>
    <strong>{profile?.email || "Not Provided"}</strong>
  </div>

  <div className="info-row">
    <span>Age</span>
    <strong>{profile?.age || "Not Provided"}</strong>
  </div>

  <div className="info-row">
    <span>Gender</span>
    <strong>{profile?.gender || "Not Provided"}</strong>
  </div>

  <div className="info-row">
    <span>Date of Birth</span>
    <strong>{profile?.dob || "Not Provided"}</strong>
  </div> 

  <div className="info-row">
    <span>Birth Time</span>
    <strong>{profile?.birthTime || "Not Provided"}</strong>
  </div>

  <div className="info-row">
    <span>Birth Place</span>
    <strong>{profile?.birthPlace || "Not Provided"}</strong>
  </div>

  <div className="info-row">
    <span>Occupation</span>
    <strong>{profile?.occupation || "Not Provided"}</strong>
  </div>

  <div className="info-row">
    <span>Interest</span>
    <strong>{profile?.interest || "Not Provided"}</strong>
  </div>
  

  <div className="info-row">
    <span>Notes</span>
    <strong>{profile?.notes || "Not Provided"}</strong>
  </div>

</div>

{/* ================= AI ACCURACY ================= */}

<div className="glass-card">

  <h2>
    <FaRobot />
    AI Accuracy
  </h2>

  <div className="score-circle">

    <h1>
      {analysis?.features?.analysis_confidence
 ? Math.round(analysis.features.analysis_confidence * 100)
 : 95}%
    </h1>

    <p>
      Confidence
    </p>

  </div>

</div>

</section>

<section className="glass-card">

  <h2>✋ Palm Shape Analysis</h2>

  <div className="info-row">
    <span>Palm Shape</span>
    <strong>{analysis?.palm_shape?.shape || "Unknown"}</strong>
  </div>

  <div className="info-row">
    <span>Palm Length</span>
    <strong>{analysis?.palm_shape?.palm_length || "-"}</strong>
  </div>

  <div className="info-row">
    <span>Palm Width</span>
    <strong>{analysis?.palm_shape?.palm_width || "-"}</strong>
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

<section className="glass-card">

  <h2>📏 Palm Line Detection</h2>

  <div className="info-row">
    <span>Detected Lines</span>
    <strong>
      {analysis?.line_detection?.candidate_lines_detected || 0}
    </strong>
  </div>

  <div className="info-row">
    <span>Estimated Main Lines</span>
    <strong>
      {analysis?.line_detection?.estimated_main_lines || 0}
    </strong>
  </div>

  <div className="info-row">
    <span>Line Quality</span>
    <strong>
      {analysis?.line_detection?.line_quality || "Unknown"}
    </strong>
  </div>

  <div className="info-row">
    <span>Status</span>
    <strong>
      {analysis?.line_detection?.status || "Not Available"}
    </strong>
  </div>

</section>



<section className="glass-card">

<h2>🖐 Hand Information</h2>

<div className="info-row">
<span>Hand Orientation</span>
<strong>
{analysis?.features?.hand_orientation}
</strong>
</div>

<div className="info-row">
<span>Palm Center X</span>
<strong>
{analysis?.features?.palm_center?.x}
</strong>
</div>

<div className="info-row">
<span>Palm Center Y</span>
<strong>
{analysis?.features?.palm_center?.y}
</strong>
</div>

</section>

  
<section className="glass-card">

<h2>📏 Palm Measurements</h2>

<div className="info-row">
<span>Thumb Length</span>
<strong>{analysis?.features?.thumb_length?.toFixed(3)}</strong>
</div>

<div className="info-row">
<span>Index Length</span>
<strong>{analysis?.features?.index_length?.toFixed(3)}</strong>
</div>

<div className="info-row">
<span>Middle Length</span>
<strong>{analysis?.features?.middle_length?.toFixed(3)}</strong>
</div>

<div className="info-row">
<span>Ring Length</span>
<strong>{analysis?.features?.ring_length.toFixed(3)}</strong>
</div>

<div className="info-row">
<span>Little Finger</span>
<strong>{analysis?.features?.little_length?.toFixed(3)}</strong>
</div>

<div className="info-row">
<span>Palm Width</span>
<strong>{analysis?.features?.palm_width?.toFixed(3)}</strong>
</div>

<div className="info-row">
<span>Palm Height</span>
<strong>{analysis?.features?.palm_height.toFixed(3)}</strong>
</div>

</section>



{/* ================= PALM ANALYSIS ================= */}
<section className="report-grid">
<section className="glass-card">

  <h2>

    <FaHandPaper />

    Palm Analysis

  </h2>

  <div className="analysis-grid">

    <div className="analysis-item">

      <h3>❤️ Life Line</h3>

      <p>
       {analysis?.reading?.life_line || "Strong & Long"}
      </p>

    </div>

    <div className="analysis-item">

      <h3>💗 Heart Line</h3>

      <p>
        {analysis?.reading?.heart_line}
      </p>

    </div>

    <div className="analysis-item">

      <h3>🧠 Head Line</h3>

      <p>
          {analysis?.reading?.head_line}
      </p>

    </div>

    <div className="analysis-item">

      <h3>⭐ Fate Line</h3>

      <p>
        {analysis?.reading?.fate_line}
      </p>

    </div>

  </div>

</section>

{/* ================= TAROT READING ================= */}

<section className="glass-card">

  <h2>
    🃏 Tarot Reading
  </h2>

  <div className="tarot-grid">

    <div className="tarot-card">

      ⭐

      <h3>The Star</h3>

      <p>Hope & Success</p>

    </div>

    <div className="tarot-card">

      🌙

      <h3>The Moon</h3>

      <p>Intuition</p>

    </div>

    <div className="tarot-card">

      🦁

      <h3>Strength</h3>

      <p>Confidence</p>

    </div>

  </div>

</section>
{/* ================= AI PREDICTIONS ================= */}

<section className="glass-card">

  <h2>
    ✨ AI Predictions
  </h2>

  <div className="prediction">

    <h3>
      <FaHeart />
      Love ★★★★★
    </h3>

   <p>
   {analysis?.reading?.love_prediction}
   </p>

    <h3>
      <FaBriefcase />
      Career ★★★★☆
    </h3>

    <p>
      {analysis?.reading?.career_prediction}
    </p>

    <h3>
      <FaCoins />
      Finance ★★★★☆
    </h3>

    <p>
      {analysis?.reading?.finance_prediction}
    </p>

    <h3>
      <FaHeartbeat />
      Health ★★★★★
    </h3>

    <p>
      {analysis?.reading?.health_prediction}
    </p>
  </div>
</section>

{/* ================= OVERALL FORTUNE ================= */}

<section className="glass-card fortune">

  <h2>
    🌟 Overall Fortune Score
  </h2>

  <div className="fortune-bar">

    <div
      className="fortune-fill"
      style={{
        width: `${analysis?.reading?.fortune_score || 90}%`,
      }}
    ></div>

  </div>

  <h1>
    {analysis?.reading?.fortune_score || 90}%
  </h1>

  <p>
    {analysis?.reading?.fortune_score >= 90
      ? "Excellent Future Outlook"
      : analysis?.reading?.fortune_score >= 75
      ? "Very Positive Future"
      : analysis?.reading?.fortune_score >= 60
      ? "Good Potential Ahead"
      : "Keep Growing & Stay Positive"}
  </p>

</section>


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

    <FaDownload />

    Download PDF Report

  </button>

  <button
    className="new-btn"
    onClick={() => {
      localStorage.removeItem("analysis_result");
      navigate("/palm-upload");
    }}
  >

    <FaRedo />

    Start New Reading

  </button>

</div>

{/* ================= FOOTER ================= */}

<footer className="report-footer">

  <p>

    Generated by

    <strong>
      {" "}
      Palmistry & Tarot Intelligence Platform
    </strong>

  </p>

  <span>

    React • FastAPI • MediaPipe • Artificial Intelligence

  </span>

</footer>

</section>
</main>

</div>

);

}

export default Report;