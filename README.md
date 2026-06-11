# Voice Bot — Voice-Activated Complaint Filing

A voice-based complaint management system. A user files a complaint by speaking;
the bot captures the speech, runs an interactive dialogue to collect the
details, stores the complaint, generates a PDF report, and replies with
synthesized voice.

## What it does
- **Speech in** — captures the caller's voice and transcribes it (speech-to-text)
- **Interactive dialogue** — asks for the details it needs (dealer, vehicle, issue)
- **Stores the complaint** — saves structured records in SQLite
- **PDF report** — generates a complaint document automatically
- **Speech out** — responds back with synthesized voice (text-to-speech)
- Also handles complaint-number lookup, warranty queries, and contact info

## Tech
Python · Flask · SpeechRecognition · gTTS (text-to-speech) · SQLite · pydub · ReportLab/PDF

## Run it
```bash
pip install -r requirements.txt
python app.py
```
You'll need `ffmpeg` installed for audio processing.

## How it works
```
caller speech ──▶ speech-to-text ──▶ dialogue manager ──▶ SQLite
                                            │
                          PDF report ◀──────┘
                                            │
                  spoken reply ◀── text-to-speech
```

## Notes
This is a working proof of concept. The natural next step is to swap the speech
layer for Indian-language models (e.g. Sarvam Saarika for STT and Bulbul for
TTS) and connect a phone number for live calls.

## License
MIT
