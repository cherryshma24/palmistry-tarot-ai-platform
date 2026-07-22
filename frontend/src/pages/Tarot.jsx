import { useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";

import "./Tarot.css";


function Tarot() {

    const navigate = useNavigate();


    const [spread, setSpread] = useState("single");
    const [loading, setLoading] = useState(false);



    const generateReading = async () => {

        try {

            setLoading(true);


            let response;


            if (spread === "single") {

                response = await api.get("/tarot/single");

            } 
            else {

                response = await api.get("/tarot/three");

            }



            console.log("Tarot Response:", response.data);



            navigate("/tarot-result", {

                state: response.data

            });



        } catch(error) {


            console.error(
                "Tarot Error:",
                error
            );


            alert(
                "Failed to generate tarot reading"
            );


        } finally {


            setLoading(false);


        }

    };




    return (

        <div className="tarot-page">


            <div className="tarot-card">


                <h1>
                    🃏 AI Tarot Reading
                </h1>



                <p>
                    Choose your tarot spread
                </p>




                <div className="spread-options">


                    <label>


                        <input

                            type="radio"

                            value="single"

                            checked={
                                spread === "single"
                            }

                            onChange={
                                (e)=>
                                setSpread(e.target.value)
                            }

                        />


                        🃏 Single Card


                    </label>





                    <label>


                        <input

                            type="radio"

                            value="three"

                            checked={
                                spread === "three"
                            }

                            onChange={
                                (e)=>
                                setSpread(e.target.value)
                            }

                        />


                        🃏 Three Card

                        <br />

                        <small>
                            Past • Present • Future
                        </small>


                    </label>



                </div>





                <button

                    onClick={generateReading}

                    disabled={loading}

                >


                    {

                        loading

                        ?

                        "Generating Reading..."

                        :

                        "✨ Generate AI Reading"

                    }


                </button>



            </div>


        </div>

    );

}



export default Tarot;