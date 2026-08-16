import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";
import "./Tarot.css";


/* ============================================================
   TAROT IMAGE COMPONENT
   Automatically tries multiple possible image locations.
============================================================ */

function TarotImage({ card, alt, className = "" }) {

    const [imageIndex, setImageIndex] = useState(0);
    const [failed, setFailed] = useState(false);

    const imageCandidates = useMemo(() => {

        if (!card?.image) {
            return [];
        }

        const rawImage = String(card.image).trim();

        // Already a complete URL
        if (
            rawImage.startsWith("http://") ||
            rawImage.startsWith("https://") ||
            rawImage.startsWith("data:")
        ) {
            return [rawImage];
        }

        // Remove accidental leading slashes
        const cleanImage = rawImage
            .replace(/^\/+/, "")
            .replace(/\\/g, "/");

        // Only keep the filename/path
        const filename = cleanImage.split("/").pop();

        /*
         * Get API base URL from your existing axios instance.
         *
         * Example:
         * http://localhost:8000/api
         */
        const configuredBase =
            api?.defaults?.baseURL || "";

        const base =
            configuredBase.replace(/\/+$/, "");

        /*
         * Backend root.
         *
         * If base is:
         * http://localhost:8000/api
         *
         * this becomes:
         * http://localhost:8000
         */
        const backendRoot =
            base.replace(/\/api\/?$/i, "");

        const candidates = [

            // 1. If backend already returns a usable path
            rawImage.startsWith("/")
                ? rawImage
                : null,

            // 2. Backend tarot image endpoint
            `${base}/tarot/images/${encodeURIComponent(filename)}`,

            // 3. Backend alternative image endpoint
            `${base}/tarot/image/${encodeURIComponent(filename)}`,

            // 4. Backend static assets
            `${base}/assets/tarot/images/${encodeURIComponent(filename)}`,

            // 5. Backend root static path
            `${backendRoot}/tarot/images/${encodeURIComponent(filename)}`,

            // 6. Frontend public/tarot/images
            `/tarot/images/${encodeURIComponent(filename)}`,

            // 7. Frontend public/tarot
            `/tarot/${encodeURIComponent(filename)}`,

            // 8. Frontend assets
            `/assets/tarot/images/${encodeURIComponent(filename)}`,

            // 9. Original path as final attempt
            `/${cleanImage}`

        ].filter(Boolean);

        // Remove duplicates
        return [...new Set(candidates)];

    }, [card?.image]);


    useEffect(() => {

        setImageIndex(0);
        setFailed(false);

    }, [card?.image]);


    if (!card?.image || failed || imageCandidates.length === 0) {

        return (
            <div
                className={`${className} tarot-image-fallback`}
                aria-label={alt}
            >
                <span>✦</span>
                <small>TAROT</small>
            </div>
        );

    }


    const currentImage =
        imageCandidates[imageIndex];


    return (

        <img
            src={currentImage}
            alt={alt || card.name}
            className={className}

            onError={(event) => {

                console.warn(
                    "Tarot image failed:",
                    currentImage
                );

                if (
                    imageIndex <
                    imageCandidates.length - 1
                ) {

                    setImageIndex(
                        previous =>
                            previous + 1
                    );

                }
                else {

                    setFailed(true);

                }

            }}

            onLoad={() => {

                console.log(
                    "Tarot image loaded:",
                    currentImage
                );

            }}
        />

    );

}


/* ============================================================
   TAROT PAGE
============================================================ */

function Tarot() {

    const navigate = useNavigate();


    /* ========================================================
       STATE
    ======================================================== */

    const [spread, setSpread] =
        useState("single");

    const [cards, setCards] =
        useState([]);

    const [displayCards, setDisplayCards] =
        useState([]);

    const [selectedCards, setSelectedCards] =
        useState([]);

    const [revealedCards, setRevealedCards] =
        useState([]);

    const [loading, setLoading] =
        useState(true);

    const [readingLoading, setReadingLoading] =
        useState(false);

    const [shuffling, setShuffling] =
        useState(false);


    /* ========================================================
       LOAD DECK
    ======================================================== */

    useEffect(() => {

        loadDeck();

    }, []);


    /* ========================================================
       LOAD TAROT DECK
    ======================================================== */

    const loadDeck = async () => {

        try {

            setLoading(true);

            const response =
                await api.get("/tarot/deck");


            console.log(
                "Tarot Deck:",
                response.data
            );


            const loadedCards =
                response.data?.cards || [];


            console.log(
                "Loaded Tarot Cards:",
                loadedCards
            );


            setCards(
                loadedCards
            );


            /*
             * Six cards around the circle.
             */
            setDisplayCards(
                getRandomCards(
                    loadedCards,
                    6
                )
            );

        }
        catch (error) {

            console.error(
                "Tarot Deck Error:",
                error
            );

            alert(
                "Failed to load Tarot deck."
            );

        }
        finally {

            setLoading(false);

        }

    };


    /* ========================================================
       RANDOM CARDS
    ======================================================== */

    const getRandomCards = (
        deck,
        count
    ) => {

        if (
            !deck ||
            deck.length === 0
        ) {

            return [];

        }


        const shuffled =
            [...deck].sort(
                () =>
                    Math.random() - 0.5
            );


        return shuffled.slice(
            0,
            Math.min(
                count,
                deck.length
            )
        );

    };


    /* ========================================================
       SHUFFLE
    ======================================================== */

    const shuffleCards = () => {

        if (
            cards.length === 0 ||
            shuffling
        ) {

            return;

        }


        setShuffling(true);

        setSelectedCards([]);

        setRevealedCards([]);


        setTimeout(() => {

            const newCards =
                getRandomCards(
                    cards,
                    6
                );


            setDisplayCards(
                newCards
            );


            setShuffling(false);

        }, 900);

    };


    /* ========================================================
       CHANGE SPREAD
    ======================================================== */

    const changeSpread = (
        newSpread
    ) => {

        setSpread(
            newSpread
        );

        setSelectedCards([]);

        setRevealedCards([]);


        /*
         * Give the user a fresh six-card
         * arrangement when changing spread.
         */
        if (cards.length > 0) {

            setDisplayCards(
                getRandomCards(
                    cards,
                    6
                )
            );

        }

    };


    /* ========================================================
       SELECT / REVEAL CARD
    ======================================================== */

    const selectCard = (
        card
    ) => {

        if (!card) {
            return;
        }


        const cardName =
            card.name;


        /* ====================================================
           SINGLE CARD
        ==================================================== */

        if (
            spread === "single"
        ) {

            if (
                selectedCards.includes(
                    cardName
                )
            ) {

                return;

            }


            setSelectedCards([
                cardName
            ]);


            /*
             * This triggers the flip.
             */
            setRevealedCards([
                cardName
            ]);


            return;

        }


        /* ====================================================
           THREE CARD
        ==================================================== */

        if (
            selectedCards.includes(
                cardName
            )
        ) {

            setSelectedCards(
                selectedCards.filter(
                    name =>
                        name !== cardName
                )
            );


            setRevealedCards(
                revealedCards.filter(
                    name =>
                        name !== cardName
                )
            );


            return;

        }


        if (
            selectedCards.length >= 3
        ) {

            return;

        }


        setSelectedCards(
            previous => [
                ...previous,
                cardName
            ]
        );


        setRevealedCards(
            previous => [
                ...previous,
                cardName
            ]
        );

    };


    /* ========================================================
       SELECTED CHECK
    ======================================================== */

    const isSelected = (
        cardName
    ) => {

        return selectedCards.includes(
            cardName
        );

    };


    /* ========================================================
       REVEALED CHECK
    ======================================================== */

    const isRevealed = (
        cardName
    ) => {

        return revealedCards.includes(
            cardName
        );

    };


    /* ========================================================
       CARD POSITION
    ======================================================== */

    const getCardPosition = (
        cardName
    ) => {

        const index =
            selectedCards.indexOf(
                cardName
            );


        if (index === -1) {

            return null;

        }


        if (
            spread === "single"
        ) {

            return "YOUR CARD";

        }


        const positions = [
            "PAST",
            "PRESENT",
            "FUTURE"
        ];


        return positions[index];

    };


    /* ========================================================
       GENERATE READING
    ======================================================== */

    const generateReading = async () => {

        if (
            spread === "single" &&
            selectedCards.length !== 1
        ) {

            alert(
                "Please shuffle and choose one Tarot card."
            );

            return;

        }


        if (
            spread === "three" &&
            selectedCards.length !== 3
        ) {

            alert(
                "Please choose three Tarot cards."
            );

            return;

        }


        try {

            setReadingLoading(true);


            const response =
                await api.post(
                    "/tarot/selected",
                    {
                        spread,
                        card_names:
                            selectedCards
                    }
                );


            console.log(
                "Tarot Reading:",
                response.data
            );


            navigate(
                "/tarot-result",
                {
                    state:
                        response.data
                }
            );

        }
        catch (error) {

            console.error(
                "Tarot Reading Error:",
                error
            );


            alert(
                error.response?.data?.detail ||
                "Failed to generate tarot reading."
            );

        }
        finally {

            setReadingLoading(false);

        }

    };


    /* ========================================================
       LOADING
    ======================================================== */

    if (loading) {

        return (

            <div className="tarot-page">

                <div className="tarot-loading">

                    <div className="mystic-symbol">
                        🔮
                    </div>

                    <h2>
                        Preparing the Tarot Deck...
                    </h2>

                    <p>
                        The cards are waiting for you.
                    </p>

                </div>

            </div>

        );

    }


    /* ========================================================
       PAGE
    ======================================================== */

    return (

        <div className="tarot-page">

            <div className="tarot-container">


                {/* =================================================
                    HEADER
                ================================================= */}

                <div className="tarot-header">

                    <div className="tarot-symbol">
                        🔮
                    </div>

                    <h1>
                        Tarot Reading
                    </h1>

                    <p>
                        Let the cards guide your intuition.
                    </p>

                </div>


                {/* =================================================
                    SPREAD SELECTOR
                ================================================= */}

                <div className="spread-selector">

                    <button
                        type="button"

                        className={
                            spread === "single"
                                ? "spread-button active"
                                : "spread-button"
                        }

                        onClick={() =>
                            changeSpread(
                                "single"
                            )
                        }
                    >

                        🃏

                        <span>
                            Single Card
                        </span>

                        <small>
                            One card • One message
                        </small>

                    </button>


                    <button
                        type="button"

                        className={
                            spread === "three"
                                ? "spread-button active"
                                : "spread-button"
                        }

                        onClick={() =>
                            changeSpread(
                                "three"
                            )
                        }
                    >

                        🔮

                        <span>
                            Three Cards
                        </span>

                        <small>
                            Past • Present • Future
                        </small>

                    </button>

                </div>


                {/* =================================================
                    INSTRUCTION
                ================================================= */}

                <div className="selection-info">

                    {spread === "single" ? (

                        <>
                            <strong>
                                ✦ Choose one card
                            </strong>

                            <span>
                                Shuffle the deck, then trust your intuition.
                            </span>
                        </>

                    ) : (

                        <>
                            <strong>
                                ✦ Choose three cards
                            </strong>

                            <span>
                                Shuffle the deck, then choose Past • Present • Future.
                            </span>
                        </>

                    )}

                </div>


                {/* =================================================
                    CIRCULAR DECK
                ================================================= */}

                <div className="circle-deck-section">

                    <div
                        className={
                            shuffling
                                ? "tarot-circle shuffling"
                                : "tarot-circle"
                        }
                    >


                        {displayCards.map(
                            (
                                card,
                                index
                            ) => {

                                const selected =
                                    isSelected(
                                        card.name
                                    );


                                const revealed =
                                    isRevealed(
                                        card.name
                                    );


                                return (

                                    <button
                                        type="button"

                                        key={
                                            `${card.name}-${index}`
                                        }

                                        className={
                                            `circle-card-position position-${index + 1}`
                                        }

                                        onClick={() =>
                                            selectCard(
                                                card
                                            )
                                        }

                                        disabled={
                                            shuffling ||
                                            (
                                                spread === "three" &&
                                                selectedCards.length >= 3 &&
                                                !selected
                                            )
                                        }
                                    >

                                        <div
                                            className={
                                                revealed
                                                    ? "tarot-card-inner revealed"
                                                    : "tarot-card-inner"
                                            }
                                        >


                                            {/* ============================
                                                CARD BACK
                                            ============================ */}

                                            <div className="tarot-card-face tarot-card-back">

                                                <div className="card-back-symbol">
                                                    ✦
                                                </div>

                                                <span>
                                                    TAROT
                                                </span>

                                            </div>


                                            {/* ============================
                                                CARD FRONT
                                            ============================ */}

                                            <div className="tarot-card-face tarot-card-front">

                                                <TarotImage
                                                    card={card}
                                                    alt={card.name}
                                                />

                                            </div>


                                        </div>


                                        {/* ============================
                                            SELECTED BADGE
                                        ============================ */}

                                        {selected && (

                                            <div className="circle-selection-badge">

                                                {spread === "single"

                                                    ? "YOUR CARD"

                                                    : getCardPosition(
                                                        card.name
                                                    )

                                                }

                                            </div>

                                        )}

                                    </button>

                                );

                            }
                        )}


                        {/* =================================================
                            CENTER SYMBOL
                        ================================================= */}

                        <div className="circle-center">

                            <span>
                                ✦
                            </span>

                        </div>

                    </div>


                    {/* =================================================
                        SHUFFLE BUTTON
                    ================================================= */}

                    <button
                        type="button"

                        className="shuffle-button"

                        onClick={
                            shuffleCards
                        }

                        disabled={
                            shuffling
                        }
                    >

                        {shuffling

                            ? "✨ Shuffling..."

                            : "🔀 Shuffle the Cards"

                        }

                    </button>

                </div>


                {/* =================================================
                    SELECTED CARDS
                ================================================= */}

                {selectedCards.length > 0 && (

                    <div className="selected-area">

                        <h3>
                            Your Selection
                        </h3>


                        <div className="selected-cards">

                            {selectedCards.map(
                                (
                                    cardName,
                                    index
                                ) => {

                                    const selectedCard =
                                        cards.find(
                                            card =>
                                                card.name ===
                                                cardName
                                        );


                                    return (

                                        <div
                                            className="selected-card"
                                            key={
                                                cardName
                                            }
                                        >

                                            <div className="selected-position">

                                                {spread === "single"

                                                    ? "YOUR CARD"

                                                    : [
                                                        "PAST",
                                                        "PRESENT",
                                                        "FUTURE"
                                                    ][index]

                                                }

                                            </div>


                                            {selectedCard && (

                                                <TarotImage
                                                    card={
                                                        selectedCard
                                                    }
                                                    alt={
                                                        selectedCard.name
                                                    }
                                                />

                                            )}


                                            <strong>
                                                {cardName}
                                            </strong>

                                        </div>

                                    );

                                }
                            )}

                        </div>

                    </div>

                )}


                {/* =================================================
                    REVEAL READING
                ================================================= */}

                <div className="reveal-area">

                    <button
                        type="button"

                        className="reveal-button"

                        disabled={
                            readingLoading ||
                            (
                                spread === "single"

                                    ? selectedCards.length !== 1

                                    : selectedCards.length !== 3
                            )
                        }

                        onClick={
                            generateReading
                        }
                    >

                        {readingLoading

                            ? "✨ Reading the Cards..."

                            : "🔮 Reveal My Reading"

                        }

                    </button>


                    <p>

                        {spread === "single"

                            ? selectedCards.length === 1

                                ? "Your card has been revealed."

                                : "Shuffle the cards and choose one."

                            : selectedCards.length === 3

                                ? "Your Past • Present • Future spread is ready."

                                : `Choose ${
                                    3 - selectedCards.length
                                } more card${
                                    3 - selectedCards.length === 1
                                        ? ""
                                        : "s"
                                }.`

                        }

                    </p>

                </div>

            </div>

        </div>

    );

}


export default Tarot;