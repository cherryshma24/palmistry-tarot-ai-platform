import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./TarotReport.css";

function TarotReport() {
    const location = useLocation();
    const navigate = useNavigate();

    const data = location.state || {};

    // ------------------------------------------------------------
    // SUPPORT YOUR EXISTING DATA STRUCTURE
    // ------------------------------------------------------------

    const spread = data.spread || "single";

    const cards =
        data.cards ||
        data.selected_cards ||
        [];

    const card =
        data.card ||
        (cards.length > 0 ? cards[0] : null) ||
        {};

    const reading =
        data.reading ||
        data.ai_reading ||
        data.interpretation ||
        "";

    const cardName =
        card.name ||
        data.card_name ||
        "Tarot Card";

    const number =
        card.number ??
        data.number ??
        "Not Available";

    const arcana =
        card.arcana ||
        data.arcana ||
        "Not Available";

    const suit =
        card.suit ||
        data.suit ||
        "Not Available";

    const archetype =
        card.archetype ||
        data.archetype ||
        "Not Available";

    const element =
        card.element ||
        data.element ||
        "Not Available";

    const keywords =
        card.keywords ||
        data.keywords ||
        [];

    const fortuneTelling =
        card.fortune_telling ||
        data.fortune_telling ||
        [];

    const lightMeaning =
        card.light_meaning ||
        data.light_meaning ||
        [];

    const shadowMeaning =
        card.shadow_meaning ||
        data.shadow_meaning ||
        [];


    // ------------------------------------------------------------
    // HELPERS
    // ------------------------------------------------------------

    const toArray = (value) => {
        if (!value) return [];

        if (Array.isArray(value)) {
            return value;
        }

        return [value];
    };


    const renderList = (value) => {
        const items = toArray(value);

        if (items.length === 0) {
            return <p className="empty-text">Not Available</p>;
        }

        return (
            <ul>
                {items.map((item, index) => (
                    <li key={index}>
                        {String(item)}
                    </li>
                ))}
            </ul>
        );
    };


    // ------------------------------------------------------------
    // AI INTERPRETATION
    // ------------------------------------------------------------

    const renderAIReading = () => {

        if (!reading) {
            return (
                <div className="empty-ai">
                    <div className="empty-ai-icon">✨</div>

                    <h3>No AI Interpretation Available</h3>

                    <p>
                        The tarot interpretation could not be loaded
                        for this reading.
                    </p>
                </div>
            );
        }


        // If AI returned a normal string
        if (typeof reading === "string") {

            return (
                <div className="ai-text">

                    {reading
                        .split("\n")
                        .map((paragraph, index) => {

                            const text = paragraph.trim();

                            if (!text) {
                                return (
                                    <div
                                        key={index}
                                        className="ai-space"
                                    />
                                );
                            }

                            // Markdown headings
                            if (
                                text.startsWith("### ")
                            ) {
                                return (
                                    <h3 key={index}>
                                        {text.replace(
                                            /^###\s*/,
                                            ""
                                        )}
                                    </h3>
                                );
                            }

                            if (
                                text.startsWith("## ")
                            ) {
                                return (
                                    <h3 key={index}>
                                        {text.replace(
                                            /^##\s*/,
                                            ""
                                        )}
                                    </h3>
                                );
                            }

                            return (
                                <p key={index}>
                                    {text}
                                </p>
                            );
                        })}

                </div>
            );
        }


        // If AI returned JSON/object
        return (
            <div className="ai-object">

                {reading.summary && (
                    <div className="ai-section">
                        <h3>🌟 Summary</h3>
                        <p>{reading.summary}</p>
                    </div>
                )}

                {reading.interpretation && (
                    <div className="ai-section">
                        <h3>🔮 Interpretation</h3>
                        <p>{reading.interpretation}</p>
                    </div>
                )}

                {reading.personality && (
                    <div className="ai-section">
                        <h3>🧠 Personality Insights</h3>
                        <p>
                            {typeof reading.personality === "string"
                                ? reading.personality
                                : JSON.stringify(
                                    reading.personality,
                                    null,
                                    2
                                )}
                        </p>
                    </div>
                )}

                {reading.opportunities && (
                    <div className="ai-section">
                        <h3>🌟 Opportunities</h3>

                        {renderList(
                            reading.opportunities
                        )}
                    </div>
                )}

                {reading.challenges && (
                    <div className="ai-section">
                        <h3>⚠️ Challenges</h3>

                        {renderList(
                            reading.challenges
                        )}
                    </div>
                )}

                {reading.advice && (
                    <div className="ai-section">
                        <h3>💫 Guidance</h3>
                        <p>{reading.advice}</p>
                    </div>
                )}

                {reading.love && (
                    <div className="ai-section">
                        <h3>❤️ Love & Relationships</h3>
                        <p>{reading.love}</p>
                    </div>
                )}

                {reading.career && (
                    <div className="ai-section">
                        <h3>💼 Career</h3>
                        <p>{reading.career}</p>
                    </div>
                )}

                {reading.finance && (
                    <div className="ai-section">
                        <h3>💰 Finance</h3>
                        <p>{reading.finance}</p>
                    </div>
                )}

                {reading.health && (
                    <div className="ai-section">
                        <h3>🌿 Health & Wellness</h3>
                        <p>{reading.health}</p>
                    </div>
                )}

                {reading.personal_growth && (
                    <div className="ai-section">
                        <h3>🌱 Personal Growth</h3>
                        <p>{reading.personal_growth}</p>
                    </div>
                )}

                {reading.overall_summary && (
                    <div className="ai-section">
                        <h3>✨ Overall Summary</h3>
                        <p>{reading.overall_summary}</p>
                    </div>
                )}

            </div>
        );
    };


    // ------------------------------------------------------------
    // FULL REPORT
    // ------------------------------------------------------------

    const renderFullReport = () => {

        return (
            <section className="full-report-panel">

                <div className="full-report-title">

                    <span>📜</span>

                    <div>
                        <h2>Full Tarot Report</h2>

                        <p>
                            Complete details of your tarot reading
                        </p>
                    </div>

                </div>


                <div className="full-report-content">

                    <div className="report-heading">
                        TAROT READING REPORT
                    </div>


                    <div className="report-divider" />


                    {/* CARD INFORMATION */}

                    <div className="report-block">

                        <h3>🃏 Card Drawn</h3>

                        <p>
                            <strong>Name:</strong>{" "}
                            {cardName}
                        </p>

                        <p>
                            <strong>Number:</strong>{" "}
                            {number}
                        </p>

                        <p>
                            <strong>Arcana:</strong>{" "}
                            {arcana}
                        </p>

                        <p>
                            <strong>Suit:</strong>{" "}
                            {suit}
                        </p>

                        <p>
                            <strong>Archetype:</strong>{" "}
                            {archetype}
                        </p>

                        <p>
                            <strong>Element:</strong>{" "}
                            {element}
                        </p>

                    </div>


                    {/* KEYWORDS */}

                    <div className="report-block">

                        <h3>⭐ Keywords</h3>

                        {renderList(keywords)}

                    </div>


                    {/* FORTUNE TELLING */}

                    <div className="report-block">

                        <h3>🔮 Fortune Telling</h3>

                        {renderList(
                            fortuneTelling
                        )}

                    </div>


                    {/* POSITIVE MEANING */}

                    <div className="report-block">

                        <h3>🌟 Positive Meanings</h3>

                        {renderList(
                            lightMeaning
                        )}

                    </div>


                    {/* SHADOW MEANING */}

                    <div className="report-block">

                        <h3>🌑 Shadow Meanings</h3>

                        {renderList(
                            shadowMeaning
                        )}

                    </div>


                    {/* AI REPORT */}

                    <div className="report-block ai-full-report">

                        <h3>✨ AI Interpretation</h3>

                        {renderAIReading()}

                    </div>


                    {/* DISCLAIMER */}

                    <div className="report-disclaimer">

                        ✦ Tarot readings are intended for
                        reflection, self-exploration and
                        entertainment. They should not be treated
                        as fixed predictions or professional advice.

                    </div>

                </div>

            </section>
        );
    };


    // ------------------------------------------------------------
    // PAGE
    // ------------------------------------------------------------

    return (

        <div className="tarot-report-page">

            <div className="tarot-report-container">


                {/* =================================================
                    HEADER
                ================================================= */}

                <header className="report-header">

                    <div className="report-symbol">
                        🔮
                    </div>

                    <h1>
                        Tarot Reading Report
                    </h1>

                    <p>
                        {spread === "three"
                            ? "Past • Present • Future"
                            : "Single Card"}
                    </p>

                </header>


                {/* =================================================
                    ACTIONS
                ================================================= */}

                <div className="report-actions">

                    <button
                        className="report-action secondary"
                        onClick={() =>
                            navigate("/tarot")
                        }
                    >
                        ← New Reading
                    </button>

                </div>


                {/* =================================================
                    SIDE BY SIDE
                ================================================= */}

                <div className="report-two-column">


                    {/* =================================================
                        CARD DETAILS
                    ================================================= */}

                    <section className="card-details-panel">

                        <div className="panel-title">

                            <span>🃏</span>

                            <h2>
                                Card Details
                            </h2>

                        </div>


                        <h3 className="card-name">
                            {cardName}
                        </h3>


                        {/* BASIC INFO */}

                        <div className="card-basic-info">

                            <div>
                                <span>Number</span>
                                <strong>
                                    {number}
                                </strong>
                            </div>

                            <div>
                                <span>Arcana</span>
                                <strong>
                                    {arcana}
                                </strong>
                            </div>

                            <div>
                                <span>Suit</span>
                                <strong>
                                    {suit}
                                </strong>
                            </div>

                            <div>
                                <span>Archetype</span>
                                <strong>
                                    {archetype}
                                </strong>
                            </div>

                            <div>
                                <span>Element</span>
                                <strong>
                                    {element}
                                </strong>
                            </div>

                        </div>


                        {/* KEYWORDS */}

                        <div className="detail-section">

                            <h3>
                                ✨ Keywords
                            </h3>

                            <div className="keyword-container">

                                {toArray(keywords).map(
                                    (keyword, index) => (

                                        <span
                                            className="keyword"
                                            key={index}
                                        >
                                            {keyword}
                                        </span>

                                    )
                                )}

                            </div>

                        </div>


                        {/* FORTUNE */}

                        <div className="detail-section">

                            <h3>
                                🔮 Fortune Telling
                            </h3>

                            {renderList(
                                fortuneTelling
                            )}

                        </div>


                        {/* POSITIVE */}

                        <div className="detail-section">

                            <h3>
                                🌟 Positive Meaning
                            </h3>

                            {renderList(
                                lightMeaning
                            )}

                        </div>


                        {/* SHADOW */}

                        <div className="detail-section">

                            <h3>
                                🌑 Shadow Meaning
                            </h3>

                            {renderList(
                                shadowMeaning
                            )}

                        </div>

                    </section>


                    {/* =================================================
                        AI INTERPRETATION
                    ================================================= */}

                    <section className="ai-interpretation-panel">

                        <div className="panel-title">

                            <span>✨</span>

                            <h2>
                                AI Interpretation
                            </h2>

                        </div>

                        <div className="ai-content">

                            {renderAIReading()}

                        </div>


                        <div className="ai-note">

                            ✦ This interpretation is generated
                            using AI and is intended for
                            self-reflection and personal insight.

                        </div>

                    </section>

                </div>


                {/* =================================================
                    FULL REPORT — SAME PAGE
                ================================================= */}

                <div className="full-report-wrapper">

                    {renderFullReport()}

                </div>


                {/* =================================================
                    BOTTOM
                ================================================= */}

                <div className="report-bottom">

                    <button
                        className="report-action secondary"
                        onClick={() =>
                            navigate("/tarot")
                        }
                    >
                        🔮 Start Another Reading
                    </button>

                </div>

            </div>

        </div>
    );
}

export default TarotReport;