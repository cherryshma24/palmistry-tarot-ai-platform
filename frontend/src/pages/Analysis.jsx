import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Analysis.css";

function Analysis() {
  const navigate = useNavigate();

  const [step, setStep] = useState(0);

  const steps = [
    "📤 Uploading Palm Image...",
    "🖐 Detecting 21 Hand Landmarks...",
    "📏 Measuring Palm Features...",
    "🔍 Extracting Major Palm Lines...",
    "🃏 Selecting Tarot Cards...",
    "🧠 Generating AI Interpretation...",
    "📄 Preparing Final Report..."
  ];

  useEffect(() => {
    if (step < steps.length - 1) {
      const timer = setTimeout(() => {
        setStep((prev) => prev + 1);
      }, 1700);

      return () => clearTimeout(timer);
    } else {
      const timer = setTimeout(() => {
        navigate("/report");
      }, 2500);

      return () => clearTimeout(timer);
    }
  }, [step, navigate]);

  const progress = Math.round(((step + 1) / steps.length) * 100);

  return (
    <div className="analysis-page">

      <div className="analysis-card">

        <div className="ai-badge">
          🤖 Artificial Intelligence Engine
        </div>

        <h1>Analyzing Your Palm</h1>

        <p className="analysis-subtitle">
          Please wait while our AI examines your palm,
          detects important features, performs tarot analysis,
          and prepares your personalized life report.
        </p>

        <div className="loader"></div>

        <div className="progress-container">

          <div className="progress-header">
            <span>Processing...</span>
            <span>{progress}%</span>
          </div>

          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${progress}%` }}
            ></div>
          </div>

        </div>

        <div className="current-step">
          {steps[step]}
        </div>

        <div className="status-box">

          <div className="status-item">
            <span>✔ AI Engine</span>
            <span>Running</span>
          </div>

          <div className="status-item">
            <span>✔ Palm Detection</span>
            <span>
              {step >= 1 ? "Completed" : "Pending"}
            </span>
          </div>

          <div className="status-item">
            <span>✔ Feature Extraction</span>
            <span>
              {step >= 3 ? "Completed" : "Processing"}
            </span>
          </div>

          <div className="status-item">
            <span>✔ Tarot Analysis</span>
            <span>
              {step >= 5 ? "Completed" : "Waiting"}
            </span>
          </div>

          <div className="status-item">
            <span>✔ Final Report</span>
            <span>
              {step === steps.length - 1
                ? "Generating..."
                : "Pending"}
            </span>
          </div>

        </div>

      </div>

    </div>
  );
}

export default Analysis;