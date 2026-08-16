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
  FaHeart,
  FaBrain,
  FaCompass,
  FaBriefcase,
  FaMoneyBillWave,
  FaArrowUp,
  FaCheckCircle,
} from "react-icons/fa";

import "./Report.css";

function Report() {
  const navigate = useNavigate();

  const [analysis, setAnalysis] = useState(null);
  const [profile, setProfile] = useState(null);
  const [palmImage, setPalmImage] = useState(null);

  useEffect(() => {
    const result = localStorage.getItem("analysis_result");
    const userProfile = localStorage.getItem("user_profile");
    const storedPalmImage = localStorage.getItem("palm_image");

    if (result) {
      try {
        setAnalysis(JSON.parse(result));
      } catch (error) {
        console.error("Invalid analysis result:", error);
      }
    }

    if (userProfile) {
      try {
        setProfile(JSON.parse(userProfile));
      } catch (error) {
        console.error("Invalid profile:", error);
      }
    }

    if (storedPalmImage) {
      setPalmImage(storedPalmImage);
    }
  }, []);

 

const reading = analysis?.reading;

// Use actual CV/YOLO line detection first.
// reading.palm_analysis currently contains fallback AI values (0),
// while analysis.line_detection contains the real detected values.
const lineDetection = analysis?.line_detection || {};

const palmAnalysis = {
  heart_line: {
    ...(reading?.palm_analysis?.heart_line || {}),
    ...(lineDetection?.heart || {}),
  },

  life_line: {
    ...(reading?.palm_analysis?.life_line || {}),
    ...(lineDetection?.life || {}),
  },

  head_line: {
    ...(reading?.palm_analysis?.head_line || {}),
    ...(lineDetection?.head || {}),
  },

  fate_line: {
    ...(reading?.palm_analysis?.fate_line || {}),
    ...(lineDetection?.fate || {}),
  },
};

// Calculate confidence from actual detected palm lines
const lineConfidences = [
  lineDetection?.heart?.confidence_percent,
  lineDetection?.life?.confidence_percent,
  lineDetection?.head?.confidence_percent,
  lineDetection?.fate?.confidence_percent,
].filter(
  (value) => typeof value === "number"
);

const calculatedConfidence =
  lineConfidences.length > 0
    ? Math.round(
        lineConfidences.reduce(
          (sum, value) => sum + value,
          0
        ) / lineConfidences.length
      )
    : 0;

const confidence =
  reading?.confidence > 0
    ? reading.confidence
    : calculatedConfidence;

const fortuneScore =
  reading?.fortune_score > 0
    ? reading.fortune_score
    : calculatedConfidence;


// ============================================================
// PALM LINE DATA
// ============================================================

const getLine = (lineName) => {

  const backendNameMap = {
    heart_line: "heart",
    life_line: "life",
    head_line: "head",
    fate_line: "fate",
  };

  const backendName =
    backendNameMap[lineName] || lineName;

  const detectedLine =
    analysis?.line_detection?.[backendName] || {};

  const readingLine =
    reading?.palm_analysis?.[lineName] || {};

  // Combine BOTH:
  // - interpretation comes from AI reading
  // - confidence/length/angle come from CV
  return {
    ...readingLine,
    ...detectedLine,

    interpretation:
      readingLine?.interpretation ||
      detectedLine?.interpretation ||
      "Interpretation not available.",
  };
};


  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/");
  };

  const startNewReading = () => {
    localStorage.removeItem("analysis_result");
    localStorage.removeItem("palm_image");
    navigate("/palm-upload");
  };

  return (
    <div className="reading-page">

      {/* =====================================================
          SIDEBAR
      ===================================================== */}

      <aside className="reading-sidebar">

        <div className="reading-logo">
          <span>🔮</span>
          <strong>PalmAI</strong>
        </div>

        <nav className="reading-nav">

          <button onClick={() => navigate("/dashboard")}>
            <FaHome />
            <span>Dashboard</span>
          </button>

          <button onClick={() => navigate("/palm-upload")}>
            <FaHandPaper />
            <span>Palm Analysis</span>
          </button>

          <button onClick={() => navigate("/tarot")}>
            <FaStar />
            <span>Tarot Reading</span>
          </button>

          <button
            className="active"
            onClick={() => navigate("/report")}
          >
            <FaChartLine />
            <span>Reports</span>
          </button>

          <button onClick={() => navigate("/profile")}>
            <FaUserCircle />
            <span>Profile</span>
          </button>

        </nav>

        <button
          className="reading-logout"
          onClick={handleLogout}
        >
          <FaSignOutAlt />
          <span>Logout</span>
        </button>

      </aside>

      {/* =====================================================
          MAIN REPORT
      ===================================================== */}

      <main className="reading-main">

        {/* ===================================================
            HEADER
        =================================================== */}

        <header className="reading-header">

          <div className="header-icon">
            🔮
          </div>

          <div>
            <p className="eyebrow">
              VEDIC & AI PALMISTRY ANALYSIS
            </p>

            <h1>
              Your Palm Reading
            </h1>

            <p className="header-description">
              AI-powered interpretation of your palm structure,
              major lines, personality and life insights.
            </p>
          </div>

        </header>


        {/* ===================================================
            REPORT META
        =================================================== */}

        <section className="report-meta">

          <div>
            <span>Prepared For</span>
            <strong>
              {profile?.full_name || "Palm Reader"}
            </strong>
          </div>

          <div>
            <span>Analysis Engine</span>
            <strong>
              MediaPipe + YOLOv8 + OpenRouter
            </strong>
          </div>

          <div>
            <span>AI Confidence</span>
            <strong className="gold-text">
              {confidence}%
            </strong>
          </div>

        </section>


        {/* ===================================================
            PALM READING HERO
        =================================================== */}

        <section className="palm-reading-card">

          {/* LEFT INFORMATION */}

          <div className="major-lines left-lines">

            <div className="section-label">
              <span>✦</span>
              MAJOR LINES
            </div>

            <LineCard
              icon="❤️"
              title="Heart Line"
              data={getLine("heart_line")}
            />

            <LineCard
              icon="🟢"
              title="Life Line"
              data={getLine("life_line")}
            />

            <LineCard
              icon="🧠"
              title="Head Line"
              data={getLine("head_line")}
            />

            <LineCard
              icon="✨"
              title="Fate Line"
              data={getLine("fate_line")}
            />

          </div>


          {/* CENTER PALM */}

          <div className="palm-center">

            <div className="palm-title">
              <span>YOUR PALM</span>
              <small>AI VISION ANALYSIS</small>
            </div>

            <div className="palm-image-frame">

              {palmImage ? (
                <img
                  src={palmImage}
                  alt="Analyzed Palm"
                />
              ) : (
                <div className="no-palm-image">
                  <span>✋</span>
                  <p>Palm image unavailable</p>
                </div>
              )}

              <div className="scan-line"></div>

            </div>

            <div className="palm-status">
              <FaCheckCircle />
              <span>
                {analysis?.total_landmarks || 21} landmarks detected
              </span>
            </div>

          </div>


          {/* RIGHT INFORMATION */}

          <div className="major-lines right-lines">

            <div className="section-label">
              <span>✦</span>
              PALM INSIGHTS
            </div>

            <InsightBox
              icon="🌟"
              title="Palm Shape"
              value={analysis?.palm_shape?.shape || "Unknown"}
              description={
                analysis?.palm_shape?.ratio
                  ? `Aspect ratio: ${analysis.palm_shape.ratio}`
                  : "Shape analysis available"
              }
            />

            <InsightBox
              icon="🧠"
              title="Personality"
              value={
                Array.isArray(reading?.personality?.traits)
                  ? reading.personality.traits
                      .slice(0, 2)
                      .join(" • ")
                  : "AI Profile"
              }
              description="Based on extracted palm characteristics."
            />

            <InsightBox
              icon="💼"
              title="Career"
              value={
                reading?.career?.career_score != null
                  ? `${reading.career.career_score}%`
                  : "Analyzed"
              }
              description={
                Array.isArray(reading?.career?.suitable_roles)
                  ? reading.career.suitable_roles
                      .slice(0, 2)
                      .join(" • ")
                  : "Career insights generated"
              }
            />

            <InsightBox
              icon="💫"
              title="Fortune"
              value={`${fortuneScore}%`}
              description={
                fortuneScore >= 90
                  ? "Excellent future outlook"
                  : fortuneScore >= 80
                  ? "Very positive future"
                  : fortuneScore >= 70
                  ? "Good opportunities ahead"
                  : "Keep growing"
              }
            />

          </div>

        </section>


        {/* ===================================================
            PALM LINE DETAILS
        =================================================== */}

        <section className="report-section">

          <div className="section-heading">

            <span>✦</span>

            <div>
              <p>DETAILED ANALYSIS</p>
              <h2>Major Palm Lines</h2>
            </div>

          </div>

          <div className="line-grid">

            <DetailedLine
              icon={<FaHeart />}
              title="Heart Line"
              color="heart"
              data={getLine("heart_line")}
            />

            <DetailedLine
              icon={<FaBrain />}
              title="Head Line"
              color="head"
              data={getLine("head_line")}
            />

            <DetailedLine
              icon={<FaCompass />}
              title="Life Line"
              color="life"
              data={getLine("life_line")}
            />

            <DetailedLine
              icon={<FaArrowUp />}
              title="Fate Line"
              color="fate"
              data={getLine("fate_line")}
            />

          </div>

        </section>


        {/* ===================================================
            PERSONALITY
        =================================================== */}

        <section className="report-section">

          <div className="section-heading">
            <span>✦</span>

            <div>
              <p>PERSONALITY INSIGHT</p>
              <h2>Your Character Profile</h2>
            </div>
          </div>

          <div className="personality-grid">

            <div className="personality-card">

              <span className="card-symbol">
                🧠
              </span>

              <h3>Core Traits</h3>

              <div className="tag-container">

                {Array.isArray(reading?.personality?.traits) &&
                reading.personality.traits.length > 0 ? (
                  reading.personality.traits.map(
                    (trait, index) => (
                      <span key={index}>
                        {trait}
                      </span>
                    )
                  )
                ) : (
                  <span>Not Available</span>
                )}

              </div>

            </div>


            <div className="personality-card">

              <span className="card-symbol">
                💪
              </span>

              <h3>Strengths</h3>

              <ul>

                {Array.isArray(
                  reading?.personality?.strengths
                ) ? (
                  reading.personality.strengths.map(
                    (item, index) => (
                      <li key={index}>
                        <FaCheckCircle />
                        {item}
                      </li>
                    )
                  )
                ) : (
                  <li>
                    <FaCheckCircle />
                    Not Available
                  </li>
                )}

              </ul>

            </div>


            <div className="personality-card">

              <span className="card-symbol">
                🌱
              </span>

              <h3>Growth Areas</h3>

              <ul>

                {Array.isArray(
                  reading?.personality?.growth_areas
                ) ? (
                  reading.personality.growth_areas.map(
                    (item, index) => (
                      <li key={index}>
                        <FaArrowUp />
                        {item}
                      </li>
                    )
                  )
                ) : (
                  <li>
                    <FaArrowUp />
                    Not Available
                  </li>
                )}

              </ul>

            </div>

          </div>

        </section>


        {/* ===================================================
            LIFE AREAS
        =================================================== */}

        <section className="life-area-grid">

          <LifeArea
            icon={<FaBriefcase />}
            title="Career & Success"
            text={
              reading?.career?.prediction ||
              "Career interpretation is not available."
            }
          />

          <LifeArea
            icon={<FaHeart />}
            title="Relationships"
            text={
              reading?.relationships?.prediction ||
              "Relationship interpretation is not available."
            }
          />

          <LifeArea
            icon={<FaMoneyBillWave />}
            title="Financial Outlook"
            text={
              reading?.finance?.prediction ||
              reading?.finance?.money_management ||
              "Financial interpretation is not available."
            }
          />

        </section>


        {/* ===================================================
            OVERALL SUMMARY
        =================================================== */}

        <section className="summary-card">

          <div className="summary-icon">
            🔮
          </div>

          <div>

            <p className="summary-label">
              YOUR OVERALL READING
            </p>

            <h2>
              AI Interpretation
            </h2>

            <p className="summary-text">
              {reading?.overall_summary ||
                "Your personalized palm interpretation is being prepared."}
            </p>

          </div>

        </section>


        {/* ===================================================
            FORTUNE
        =================================================== */}

        <section className="fortune-section">

          <div className="fortune-header">

            <div>
              <p>FUTURE OUTLOOK</p>
              <h2>Overall Fortune</h2>
            </div>

            <strong>
              {fortuneScore}%
            </strong>

          </div>

          <div className="fortune-track">

            <div
              className="fortune-progress"
              style={{
                width: `${fortuneScore}%`,
              }}
            />

          </div>

          <p className="fortune-message">

            {fortuneScore >= 90
              ? "Excellent Future Outlook"
              : fortuneScore >= 80
              ? "Very Positive Future"
              : fortuneScore >= 70
              ? "Good Opportunities Ahead"
              : "Keep Growing"}

          </p>

        </section>


        {/* ===================================================
            DISCLAIMER
        =================================================== */}

        <div className="reading-disclaimer">

          <strong>
            ✦ AI-assisted palmistry
          </strong>

          <span>
            This reading is intended for entertainment,
            reflection and personal insight. It should not
            be considered scientific, medical, financial
            or professional advice.
          </span>

        </div>


        {/* ===================================================
            ACTIONS
        =================================================== */}

        <div className="report-actions">

          <button
            className="print-btn"
            onClick={() => window.print()}
          >
            🖨️ Download / Print Report
          </button>

          <button
            className="new-reading-btn"
            onClick={startNewReading}
          >
            ✨ Start New Reading
          </button>

        </div>


        {/* ===================================================
            FOOTER
        =================================================== */}

        <footer className="reading-footer">

          <strong>
            🔮 Palmistry & Tarot Intelligence Platform
          </strong>

          <span>
            React • FastAPI • MediaPipe • OpenCV • YOLOv8 • OpenRouter AI
          </span>

        </footer>

      </main>

    </div>
  );
}


/* =============================================================
   LINE CARD
============================================================= */

function LineCard({ icon, title, data }) {

  const confidence =
    data?.confidence_percent ??
    (data?.confidence != null
      ? Math.round(data.confidence * 100)
      : 0);

  const length =
    data?.length_pixels ??
    data?.length ??
    data?.line_length ??
    0;

  return (
    <div className="line-card">

      <div className="line-card-title">

        <span>
          {icon}
        </span>

        <strong>
          {title}
        </strong>

      </div>

      <p>
        {data?.interpretation ||
          "No interpretation available."}
      </p>

      <div className="line-stats">

        <span>
          Confidence

          <strong>
            {confidence}%
          </strong>
        </span>

        <span>
          Length

          <strong>
            {length}px
          </strong>
        </span>

      </div>

    </div>
  );
}

/* =============================================================
   INSIGHT BOX
============================================================= */

function InsightBox({
  icon,
  title,
  value,
  description,
}) {
  return (
    <div className="insight-box">

      <span className="insight-icon">
        {icon}
      </span>

      <div>

        <small>
          {title}
        </small>

        <strong>
          {value}
        </strong>

        <p>
          {description}
        </p>

      </div>

    </div>
  );
}


/* =============================================================
   DETAILED LINE
============================================================= */

function DetailedLine({
  icon,
  title,
  color,
  data,
}) {

  const confidence =
    data?.confidence_percent ??
    (data?.confidence != null
      ? Math.round(data.confidence * 100)
      : 0);

  const length =
    data?.length_pixels ??
    data?.length ??
    data?.line_length ??
    0;

  const angle =
    data?.angle_degrees ??
    data?.angle ??
    0;


  return (
    <div className={`detailed-line ${color}`}>

      <div className="detailed-line-header">

        <span>
          {icon}
        </span>

        <h3>
          {title}
        </h3>

      </div>

      <p>
        {data?.interpretation ||
          "No interpretation available."}
      </p>

      <div className="detail-values">

        <div>
          <span>Detection</span>

          <strong>
            {confidence}%
          </strong>
        </div>

        <div>
          <span>Length</span>

          <strong>
            {length}px
          </strong>
        </div>

        <div>
          <span>Angle</span>

          <strong>
            {angle}°
          </strong>
        </div>

      </div>

    </div>
  );
}


/* =============================================================
   LIFE AREA
============================================================= */

function LifeArea({
  icon,
  title,
  text,
}) {
  return (
    <div className="life-area">

      <div className="life-icon">
        {icon}
      </div>

      <div>

        <h3>
          {title}
        </h3>

        <p>
          {text}
        </p>

      </div>

    </div>
  );
}


export default Report;