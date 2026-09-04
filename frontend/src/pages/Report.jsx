import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaHome,
  FaHandPaper,
  FaStar,
  FaChartLine,
  FaUserCircle,
  FaSignOutAlt,
  FaCheckCircle,
  FaHeart,
  FaBrain,
  FaCompass,
  FaBriefcase,
  FaMoneyBillWave,
  FaArrowUp,
} from "react-icons/fa";

import "./Report.css";

function Report() {
  const navigate = useNavigate();

  const [analysis, setAnalysis] = useState(null);
  const [profile, setProfile] = useState(null);
  const [palmImage, setPalmImage] = useState(null);

  // ============================================================
  // LOAD DATA
  // ============================================================

  useEffect(() => {
    const result = localStorage.getItem("analysis_result");
    const userProfile = localStorage.getItem("user_profile");
    const storedPalmImage = localStorage.getItem("palm_image");

    console.log("========== PALMAI REPORT DEBUG ==========");
    console.log("RAW analysis_result:", result);

    if (result) {
      try {
        const parsedResult = JSON.parse(result);

        console.log("FULL BACKEND RESULT:", parsedResult);

        console.log(
          "DIRECT LINE DETECTION:",
          parsedResult?.line_detection
        );

        console.log(
          "FEATURE LINE DETECTION:",
          parsedResult?.features?.line_detection
        );

        console.log(
          "HEART:",
          parsedResult?.line_detection?.heart
        );

        console.log(
          "LIFE:",
          parsedResult?.line_detection?.life
        );

        console.log(
          "HEAD:",
          parsedResult?.line_detection?.head
        );

        console.log(
          "FATE:",
          parsedResult?.line_detection?.fate
        );

        console.log("==========================================");

        setAnalysis(parsedResult);
      } catch (error) {
        console.error(
          "Invalid analysis_result:",
          error
        );
      }
    } else {
      console.warn(
        "No analysis_result found in localStorage."
      );
    }

    if (userProfile) {
      try {
        setProfile(JSON.parse(userProfile));
      } catch (error) {
        console.error(
          "Invalid user profile:",
          error
        );
      }
    }

    if (storedPalmImage) {
      setPalmImage(storedPalmImage);
    }
  }, []);

  // ============================================================
  // FIND LINE DETECTION DATA
  // ============================================================

  const lineDetection =
    analysis?.line_detection ||
    analysis?.features?.line_detection ||
    analysis?.palm_analysis?.palm_lines ||
    {};

  // ============================================================
  // CONFIDENCE NORMALIZER
  // ============================================================

  const getConfidence = (line) => {
    if (!line || typeof line !== "object") {
      return 0;
    }

    let value =
      line.confidence_percent ??
      line.confidence_percentage ??
      line.confidence ??
      line.score ??
      line.probability ??
      line.detection_confidence;

    if (value === undefined || value === null) {
      return 0;
    }

    value = Number(value);

    if (Number.isNaN(value)) {
      return 0;
    }

    // Backend decimal format:
    // 0.414 -> 41.4
    if (value >= 0 && value <= 1) {
      value = value * 100;
    }

    return Math.min(
      100,
      Math.max(0, value)
    );
  };

  // ============================================================
  // LENGTH NORMALIZER
  // ============================================================

  const getLength = (line) => {
    if (!line || typeof line !== "object") {
      return 0;
    }

    const value =
      line.length_pixels ??
      line.length ??
      line.line_length ??
      line.distance ??
      0;

    const number = Number(value);

    return Number.isNaN(number)
      ? 0
      : number;
  };

  // ============================================================
  // ANGLE NORMALIZER
  // ============================================================

  const getAngle = (line) => {
    if (!line || typeof line !== "object") {
      return 0;
    }

    const value =
      line.angle_degrees ??
      line.angle ??
      line.degrees ??
      0;

    const number = Number(value);

    return Number.isNaN(number)
      ? 0
      : number;
  };

  // ============================================================
  // GET PALM LINE
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

    // Search every possible backend location
    const detectedLine =
      analysis?.line_detection?.[backendName] ||
      analysis?.features?.line_detection?.[backendName] ||
      analysis?.palm_analysis?.palm_lines?.[backendName] ||
      analysis?.palm_analysis?.line_detection?.[backendName] ||
      {};

    // AI reading information
    const readingLine =
      analysis?.reading?.palm_analysis?.[lineName] ||
      analysis?.reading?.palm_analysis?.[backendName] ||
      analysis?.reading?.lines?.[backendName] ||
      {};

    const confidence =
      getConfidence(detectedLine);

    const length =
      getLength(detectedLine) ||
      getLength(readingLine);

    const angle =
      getAngle(detectedLine) ||
      getAngle(readingLine);

    const interpretation =
      detectedLine?.interpretation ||
      readingLine?.interpretation ||
      readingLine?.prediction ||
      "No interpretation available.";

    const combinedLine = {
      ...readingLine,
      ...detectedLine,

      confidence_percent: confidence,
      length_pixels: length,
      angle_degrees: angle,
      interpretation,
    };

    console.log(
      `REPORT ${lineName}:`,
      combinedLine
    );

    return combinedLine;
  };

  // ============================================================
  // INDIVIDUAL LINE DATA
  // ============================================================

  const heartLine = getLine("heart_line");
  const lifeLine = getLine("life_line");
  const headLine = getLine("head_line");
  const fateLine = getLine("fate_line");

  const heartConfidence =
    heartLine.confidence_percent;

  const lifeConfidence =
    lifeLine.confidence_percent;

  const headConfidence =
    headLine.confidence_percent;

  const fateConfidence =
    fateLine.confidence_percent;

  // ============================================================
  // OVERALL CONFIDENCE
  // ============================================================

  const rawOverallConfidence =
    analysis?.overall_confidence ??
    analysis?.features?.overall_confidence ??
    analysis?.features?.analysis_confidence ??
    analysis?.features?.yolo_line_confidence ??
    analysis?.palm_analysis?.overall_confidence ??
    null;

  let confidence = 0;

  if (
    rawOverallConfidence !== null &&
    rawOverallConfidence !== undefined
  ) {
    let value = Number(
      rawOverallConfidence
    );

    if (!Number.isNaN(value)) {
      if (value >= 0 && value <= 1) {
        value = value * 100;
      }

      confidence = Math.min(
        100,
        Math.max(0, value)
      );
    }
  } else {
    const values = [
      heartConfidence,
      lifeConfidence,
      headConfidence,
      fateConfidence,
    ].filter(
      (value) =>
        typeof value === "number" &&
        value > 0
    );

    if (values.length > 0) {
      confidence =
        values.reduce(
          (sum, value) => sum + value,
          0
        ) / values.length;
    }
  }

  confidence = Number(
    confidence.toFixed(1)
  );

  // ============================================================
  // FORTUNE
  // ============================================================

  const fortuneScore = confidence;

  // ============================================================
  // LOGOUT
  // ============================================================

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/");
  };

  // ============================================================
  // NEW READING
  // ============================================================

  const startNewReading = () => {
    localStorage.removeItem("analysis_result");
    localStorage.removeItem("palm_image");

    navigate("/palm-upload");
  };

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div className="reading-page">

      {/* SIDEBAR */}

      <aside className="reading-sidebar">

        <div className="reading-logo">
          <span>🔮</span>
          <strong>PalmAI</strong>
        </div>

        <nav className="reading-nav">

          <button
            onClick={() =>
              navigate("/dashboard")
            }
          >
            <FaHome />
            <span>Dashboard</span>
          </button>

          <button
            onClick={() =>
              navigate("/palm-upload")
            }
          >
            <FaHandPaper />
            <span>Palm Analysis</span>
          </button>

          <button
            onClick={() =>
              navigate("/tarot")
            }
          >
            <FaStar />
            <span>Tarot Reading</span>
          </button>

          <button
            className="active"
            onClick={() =>
              navigate("/report")
            }
          >
            <FaChartLine />
            <span>Reports</span>
          </button>

          <button
            onClick={() =>
              navigate("/profile")
            }
          >
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

      {/* MAIN */}

      <main className="reading-main">

        {/* HEADER */}

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
              AI-powered interpretation of your palm
              structure, major lines, personality and
              life insights.
            </p>
          </div>

        </header>

        {/* META */}

        <section className="report-meta">

          <div>
            <span>Prepared For</span>

            <strong>
              {profile?.full_name ||
                "Palm Reader"}
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
              {confidence.toFixed(1)}%
            </strong>
          </div>

        </section>

        {/* PALM HERO */}

        <section className="palm-reading-card">

          {/* LEFT */}

          <div className="major-lines left-lines">

            <div className="section-label">
              <span>✦</span>
              MAJOR LINES
            </div>

            <LineCard
              icon="❤️"
              title="Heart Line"
              data={heartLine}
            />

            <LineCard
              icon="🟢"
              title="Life Line"
              data={lifeLine}
            />

            <LineCard
              icon="🧠"
              title="Head Line"
              data={headLine}
            />

            <LineCard
              icon="✨"
              title="Fate Line"
              data={fateLine}
            />

          </div>

          {/* CENTER */}

          <div className="palm-center">

            <div className="palm-title">
              <span>YOUR PALM</span>
              <small>
                AI VISION ANALYSIS
              </small>
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
                  <p>
                    Palm image unavailable
                  </p>
                </div>
              )}

              <div className="scan-line"></div>

            </div>

            <div className="palm-status">

              <FaCheckCircle />

              <span>
                {analysis?.total_landmarks ||
                  21} landmarks detected
              </span>

            </div>

          </div>

          {/* RIGHT */}

          <div className="major-lines right-lines">

            <div className="section-label">
              <span>✦</span>
              PALM INSIGHTS
            </div>

            <InsightBox
              icon="🌟"
              title="Palm Shape"
              value={
                analysis?.palm_shape?.shape ||
                analysis?.features?.palm_shape?.shape ||
                "Unknown"
              }
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
                Array.isArray(
                  analysis?.reading?.personality?.traits
                )
                  ? analysis.reading.personality.traits
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
                analysis?.reading?.career?.career_score != null
                  ? `${analysis.reading.career.career_score}%`
                  : "Analyzed"
              }
              description={
                Array.isArray(
                  analysis?.reading?.career?.suitable_roles
                )
                  ? analysis.reading.career.suitable_roles
                      .slice(0, 2)
                      .join(" • ")
                  : "Career insights generated"
              }
            />

            <InsightBox
              icon="💫"
              title="Fortune"
              value={`${fortuneScore.toFixed(1)}%`}
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

        {/* DETAILED ANALYSIS */}

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
              data={heartLine}
            />

            <DetailedLine
              icon={<FaBrain />}
              title="Head Line"
              color="head"
              data={headLine}
            />

            <DetailedLine
              icon={<FaCompass />}
              title="Life Line"
              color="life"
              data={lifeLine}
            />

            <DetailedLine
              icon={<FaArrowUp />}
              title="Fate Line"
              color="fate"
              data={fateLine}
            />

          </div>

        </section>

        {/* PERSONALITY */}

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

                {Array.isArray(
                  analysis?.reading?.personality?.traits
                ) &&
                analysis.reading.personality.traits.length > 0 ? (

                  analysis.reading.personality.traits.map(
                    (trait, index) => (
                      <span key={index}>
                        {trait}
                      </span>
                    )
                  )

                ) : (
                  <span>
                    Not Available
                  </span>
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
                  analysis?.reading?.personality?.strengths
                ) ? (

                  analysis.reading.personality.strengths.map(
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
                  analysis?.reading?.personality?.growth_areas
                ) ? (

                  analysis.reading.personality.growth_areas.map(
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

        {/* LIFE AREAS */}

        <section className="life-area-grid">

          <LifeArea
            icon={<FaBriefcase />}
            title="Career & Success"
            text={
              analysis?.reading?.career?.prediction ||
              "Career interpretation is not available."
            }
          />

          <LifeArea
            icon={<FaHeart />}
            title="Relationships"
            text={
              analysis?.reading?.relationships?.prediction ||
              "Relationship interpretation is not available."
            }
          />

          <LifeArea
            icon={<FaMoneyBillWave />}
            title="Financial Outlook"
            text={
              analysis?.reading?.finance?.prediction ||
              analysis?.reading?.finance?.money_management ||
              "Financial interpretation is not available."
            }
          />

        </section>

        {/* SUMMARY */}

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
              {analysis?.reading?.overall_summary ||
                "Your personalized palm interpretation is being prepared."}
            </p>

          </div>

        </section>

        {/* FORTUNE */}

        <section className="fortune-section">

          <div className="fortune-header">

            <div>
              <p>FUTURE OUTLOOK</p>
              <h2>Overall Fortune</h2>
            </div>

            <strong>
              {fortuneScore.toFixed(1)}%
            </strong>

          </div>

          <div className="fortune-track">

            <div
              className="fortune-progress"
              style={{
                width: `${Math.min(
                  100,
                  Math.max(0, fortuneScore)
                )}%`,
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

        {/* DISCLAIMER */}

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

        {/* ACTIONS */}

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

        {/* FOOTER */}

        <footer className="reading-footer">

          <strong>
            🔮 Palmistry & Tarot Intelligence Platform
          </strong>

          <span>
            React • FastAPI • MediaPipe • OpenCV •
            YOLOv8 • OpenRouter AI
          </span>

        </footer>

      </main>
    </div>
  );
}

// =============================================================
// LINE CARD
// =============================================================

function LineCard({ icon, title, data }) {
  const confidence = Number(
    data?.confidence_percent ?? 0
  );

  const length = Number(
    data?.length_pixels ??
    data?.length ??
    data?.line_length ??
    0
  );

  return (
    <div className="line-card">

      <div className="line-card-title">
        <span>{icon}</span>
        <strong>{title}</strong>
      </div>

      <p>
        {data?.interpretation ||
          "No interpretation available."}
      </p>

      <div className="line-stats">

        <span>
          Confidence
          <strong>
            {confidence.toFixed(1)}%
          </strong>
        </span>

        <span>
          Length
          <strong>
            {length.toFixed(2)}px
          </strong>
        </span>

      </div>

    </div>
  );
}

// =============================================================
// INSIGHT BOX
// =============================================================

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

        <small>{title}</small>

        <strong>{value}</strong>

        <p>{description}</p>

      </div>

    </div>
  );
}

// =============================================================
// DETAILED LINE
// =============================================================

function DetailedLine({
  icon,
  title,
  color,
  data,
}) {
  const confidence = Number(
    data?.confidence_percent ?? 0
  );

  const length = Number(
    data?.length_pixels ??
    data?.length ??
    data?.line_length ??
    0
  );

  const angle = Number(
    data?.angle_degrees ??
    data?.angle ??
    0
  );

  return (
    <div
      className={`detailed-line ${color}`}
    >

      <div className="detailed-line-header">

        <span>{icon}</span>

        <h3>{title}</h3>

      </div>

      <p>
        {data?.interpretation ||
          "No interpretation available."}
      </p>

      <div className="detail-values">

        <div>
          <span>Detection</span>
          <strong>
            {confidence.toFixed(1)}%
          </strong>
        </div>

        <div>
          <span>Length</span>
          <strong>
            {length.toFixed(2)}px
          </strong>
        </div>

        <div>
          <span>Angle</span>
          <strong>
            {angle.toFixed(2)}°
          </strong>
        </div>

      </div>

    </div>
  );
}

// =============================================================
// LIFE AREA
// =============================================================

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

        <h3>{title}</h3>

        <p>{text}</p>

      </div>

    </div>
  );
}

export default Report;