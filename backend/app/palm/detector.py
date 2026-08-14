import mediapipe as mp


# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands


hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
)


def detect_hand_landmarks(rgb_image):
    """
    Detect hand landmarks using MediaPipe.
    """

    # Ensure image is RGB
    if rgb_image is None:
        return None


    results = hands.process(rgb_image)


    if not results.multi_hand_landmarks:
        print("❌ MediaPipe: No hand detected")
        return None


    landmarks = []


    for hand_landmarks in results.multi_hand_landmarks:

        for landmark in hand_landmarks.landmark:

            landmarks.append({

                "x": landmark.x,

                "y": landmark.y,

                "z": landmark.z

            })


    print("✅ MediaPipe: Hand detected")

    return landmarks