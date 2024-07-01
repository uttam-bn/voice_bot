# Voice-Activated Complaint Filing System

## Overview
This project is a voice-activated complaint filing system built using Python, Flask, and various libraries for speech recognition and text-to-speech conversion. The system allows users to file complaints verbally, validates input, stores data in a SQLite database, and provides responses both through voice and text.

## Features
- Voice recognition for user input using SpeechRecognition library.
- Text-to-speech conversion for system responses using gTTS (Google Text-to-Speech) library.
- Flask web framework for handling HTTP requests and rendering HTML templates.
- SQLite database for storing complaint data with basic CRUD operations.

## Prerequisites
- Python 3.x installed on your system.
- Required Python packages can be installed using pip:
pip install flask, gTTS, SpeechRecognition, pydub, playsound
- Ensure ffmpeg and ffprobe are installed and accessible in your system path for audio processing (required by pydub).

## Setting Up
1. **Clone the repository:**
 git clone https://github.com/uttam-bn/voice_bot.git
 cd voice_bot

- pip install -r requirements.txt
- python app.py


## Usage

- Upon running the application, you will hear "Thank you for calling. I am Laami. How can I help you?".
- Speak "register a complaint" or "file a complaint" to begin filing a complaint. Follow the voice prompts to provide details such as dealer name, vehicle name, etc.
- If asked for a complaint number, provide the complaint number to retrieve details.
- To inquire about the warranty period, ask about warranty or warranty claim.
- Emails related queries will be answered with "infotainment@gmail.com".
- Complaint data and details will be saved in a SQLite database named complaints.db.
- A text file complaints.txt will be generated containing the number of complaints filed in pdf format.
- Voice recordings of each interaction will be saved as response.mp3 for reference.


