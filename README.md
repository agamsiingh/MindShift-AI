# MindShift-AI




# Emotion Detection and Mental Health Support Assistant

This project is a real-time emotion detection and mental health support system using Python. It utilizes computer vision, emotion recognition, and a chatbot powered by the Google Gemini API to provide comfort and assistance to users experiencing sadness or stress.

---

## 📖 Features

- **Emotion Detection**: Uses a webcam and the FER library to detect emotions in real-time.
- **Mental Health Chatbot**: A chatbot provides empathetic responses and coping strategies.
- **Speech Interaction**: Supports speech recognition and text-to-speech for natural conversations.
- **Prolonged Sadness Detection**: Automatically initiates a conversation when prolonged sadness is detected.
- **Retry Logic**: Handles API errors gracefully with retry mechanisms.

---

## 🛠 Technologies Used

- **Programming Language**: Python
- **Libraries**:  
  - `cv2` for webcam access and video processing  
  - `FER` for emotion recognition  
  - `pyttsx3` for text-to-speech  
  - `speech_recognition` for speech-to-text  
  - `dotenv` for environment variable management  
  - `google.generativeai` for chatbot functionality
- **API**: Google Gemini API for natural language generation  

---

## 📂 Project Structure

- `main.py`: Core script for the application.
- `.env`: Environment variables (e.g., API key for Google Gemini).
- `requirements.txt`: Python dependencies.

---

## 🔧 Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/emotion-detection-assistant.git
   cd emotion-detection-assistant
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Key**:  
   - Create a `.env` file in the root directory.
   - Add your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

4. **Run the Application**:
   ```bash
   python main.py
   ```

---

## 🚀 Usage

- Launch the application and allow webcam access.
- The system will detect emotions in real-time.
- If prolonged sadness is detected, the chatbot initiates a conversation.
- Speak or type your responses to interact with the chatbot.

---

## 📝 Notes

- Ensure a stable internet connection for Google Gemini API usage.
- Use a well-lit environment for better emotion detection accuracy.

---

## 🤝 Contributions

Contributions are welcome!  
- Fork the repository.
- Create a new branch (`feature-branch-name`).
- Submit a pull request for review.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 🌟 Acknowledgments

Special thanks to the creators of the libraries and APIs used in this project for their amazing tools and resources.
```  

Let me know if you'd like any modifications or additional sections!
