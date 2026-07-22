import { useLocation, useNavigate } from "react-router-dom";
import "./TarotReport.css";


function TarotReport() {

    const location = useLocation();
    const navigate = useNavigate();


    const reading = location.state;


    if (!reading) {

        return (
            <div className="tarot-report-page">

                <div className="report-card">

                    <h2>
                        No Reading Found
                    </h2>

                    <button onClick={() => navigate("/tarot")}>
                        Back to Tarot
                    </button>

                </div>

            </div>
        );
    }



    // Supports both single and three card readings
    const cards = reading.cards || {};



    const renderCard = (title, card) => {


        if (!card) return null;


        return (

            <div className="card-section">


                <h3>
                    {title}
                </h3>



                <h4>
                    {card.name}
                </h4>



                <p>
                    <b>Number:</b> {card.number}
                </p>



                <p>
                    <b>Arcana:</b> {card.arcana}
                </p>



                <p>
                    <b>Suit:</b> {card.suit}
                </p>



                {
                    card.archetype &&

                    <p>
                        <b>Archetype:</b> {card.archetype}
                    </p>

                }



                {
                    card.element &&

                    <p>
                        <b>Element:</b> {card.element}
                    </p>

                }



                <p>
                    <b>Keywords:</b>
                </p>


                <ul>

                    {
                        card.keywords?.map((word,index)=>(

                            <li key={index}>
                                {word}
                            </li>

                        ))
                    }

                </ul>





                {
                    card.fortune_telling &&

                    <>

                    <p>
                        <b>Fortune Telling:</b>
                    </p>


                    <ul>

                    {
                        card.fortune_telling.map((item,index)=>(

                            <li key={index}>
                                {item}
                            </li>

                        ))
                    }

                    </ul>

                    </>

                }





                <p>
                    <b>Light Meaning:</b>
                </p>


                <ul>

                {
                    card.light_meaning?.map((item,index)=>(

                        <li key={index}>
                            {item}
                        </li>

                    ))
                }

                </ul>





                <p>
                    <b>Shadow Meaning:</b>
                </p>


                <ul>

                {
                    card.shadow_meaning?.map((item,index)=>(

                        <li key={index}>
                            {item}
                        </li>

                    ))
                }

                </ul>



            </div>

        );

    };




    return (

        <div className="tarot-report-page">


            <div className="report-card">



                <h1>
                    🔮 Tarot Reading Report
                </h1>



                <h2>
                    {reading.spread}
                </h2>




                {/* SINGLE CARD */}

                {
                    reading.card &&

                    renderCard(
                        "🃏 Drawn Card",
                        reading.card
                    )

                }




                {/* THREE CARD */}

                {
                    cards.past &&

                    renderCard(
                        "🌙 Past",
                        cards.past
                    )

                }



                {
                    cards.present &&

                    renderCard(
                        "☀️ Present",
                        cards.present
                    )

                }



                {
                    cards.future &&

                    renderCard(
                        "🌟 Future",
                        cards.future
                    )

                }






                {/* AI GENERATED READING */}

                {
                    (reading.ai_reading || reading.interpretation) &&


                    <div className="ai-section">


                        <h2>
                            ✨ AI Interpretation
                        </h2>



                        <p>
                            {
                                reading.ai_reading ||
                                reading.interpretation
                            }
                        </p>



                    </div>

                }






                {/* TEXT REPORT */}

                {
                    reading.report &&

                    <div className="report-text">


                        <h2>
                            📜 Full Report
                        </h2>


                        <pre>
                            {reading.report}
                        </pre>


                    </div>

                }





                <div className="report-buttons">


    <button
        onClick={() => navigate("/tarot")}
    >
        🔮 New Reading
    </button>



    <button
        onClick={() => navigate("/dashboard")}
    >
        🏠 Back to Dashboard
    </button>


</div>


            </div>


        </div>

    );

}


export default TarotReport;