import cv2
import time
from fer import FER
import pyttsx3
import os
import google.generativeai as genai
import speech_recognition as sr
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

# Load environment variables for Gemini API
load_dotenv()

# Initialize the emotion detector and TTS engine
detector = FER()
engine = pyttsx3.init()

# Set to a natural-sounding female voice
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', 145)  # Adjust speech rate for more natural flow
        engine.setProperty('volume', 1.0)  # Max volume for clarity
        break

# Set up the Google Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Text-to-speech and speech recognition
def text_to_speech(text):
    print(f"Bot (speaking): {text}")
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            text_to_speech("Sorry, I didn't catch that. Could you repeat?")
            return None
        except sr.RequestError:
            text_to_speech("There seems to be an issue with the speech service.")
            return None

# Create the Gemini API mental health support model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Configure the mental health support chatbot
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="You are a mental health support assistant. You provide empathy, comfort, and coping strategies for emotional well-being."
)

chat_session = model.start_chat(history=[])

# Retry logic for ResourceExhausted errors
def send_message_with_retry(chat_session, user_input, max_retries=5, retry_delay=10):
    for attempt in range(max_retries):
        try:
            response = chat_session.send_message(user_input)
            return response.text
        except ResourceExhausted as e:
            print(f"Resource exhausted (Attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying after {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                return "Sorry, I'm unable to respond right now due to system limitations."

# Video capture for emotion detection
video_capture = cv2.VideoCapture(0)

# Track time spent in sadness
emotion_timer = {'sad': 0}
emotion_threshold = 1  # Seconds to trigger chatbot for prolonged sadness

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Detect emotions in the frame
    emotions = detector.detect_emotions(frame)

    if emotions:
        dominant_emotion, emotion_score = detector.top_emotion(frame)

        # Display the detected emotion on the video
        cv2.putText(frame, f'{dominant_emotion}: {emotion_score:.2f}', (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        if dominant_emotion == 'sad':
            emotion_timer['sad'] += 0.5
            if emotion_timer['sad'] >= emotion_threshold:
                cv2.putText(frame, "I noticed you're feeling sad. Let's talk.", (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                
                text_to_speech("I noticed you're feeling sad. Let's talk. Why are you feeling down?")

                # Stop webcam for conversation
                video_capture.release()
                cv2.destroyAllWindows()

                # Continuous conversation
                while True:
                    user_input = recognize_speech()

                    if user_input and "stop" in user_input.lower():
                        text_to_speech("Okay, I'm here if you need to talk again.")
                        break

                    if user_input:
                        # Send input to chatbot with retry logic
                        model_response = send_message_with_retry(chat_session, user_input)
                        text_to_speech(model_response)

                # Restart webcam after conversation
                video_capture = cv2.VideoCapture(0)
                emotion_timer['sad'] = 0  # Reset sadness timer

        else:
            # Reset timer if sadness is not detected
            emotion_timer['sad'] = 0

    # Display the video with detected emotions
    if video_capture.isOpened():
        cv2.imshow('Emotion Detection', frame)

    # Break loop on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Control emotion check rate
    time.sleep(0.5)

# Release video capture resources
video_capture.release()
cv2.destroyAllWindows()
