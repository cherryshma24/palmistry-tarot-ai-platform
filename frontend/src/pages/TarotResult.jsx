import { useLocation, useNavigate } from "react-router-dom";
import "./TarotResult.css";


function TarotResult(){

    const location = useLocation();
    const navigate = useNavigate();

    const reading = location.state;


    if(!reading){
        return <h2>No Card Selected</h2>;
    }


    const card = reading.card || reading.cards?.present;



    return(

        <div className="tarot-result-page">


            <div className="result-card">


                <h1>
                    🃏 Tarot Card Drawn
                </h1>


                <h2>
                    {card.name}
                </h2>


                <p>
                    <b>Arcana:</b> {card.arcana}
                </p>


                <p>
                    <b>Suit:</b> {card.suit}
                </p>


                <h3>
                    Keywords
                </h3>


                <ul>

                {
                    card.keywords?.map((item,index)=>(

                        <li key={index}>
                            {item}
                        </li>

                    ))
                }

                </ul>



                <button
                onClick={()=>
                    navigate("/tarot-report",
                    {
                        state:reading
                    })
                }
                >

                ✨ Generate Report

                </button>



                <br/>


                <button
                onClick={()=>
                    navigate("/dashboard")
                }
                >

                🏠 Dashboard

                </button>


            </div>


        </div>

    );

}


export default TarotResult;