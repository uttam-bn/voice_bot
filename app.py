import random
from gtts import gTTS
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.playback import play
from fpdf import FPDF
from pydub.utils import which
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

from flask import Flask

app = Flask(__name__)

# Initialize database
from database import init_db, store_complaint, is_duplicate_complaint, get_complaint_id, get_complaint_details, get_total_complaints
init_db()

def generate_complaint_id():
    return f"{random.randint(1000, 9999)}"

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    sound = AudioSegment.from_mp3("response.mp3")
    play(sound)
    os.remove("response.mp3")

def get_voice_input(prompt):
    speak_text(prompt)
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        audio = recognizer.listen(source)
    try:
        response = recognizer.recognize_google(audio)
        print(f"User said: {response}")
        return response
    except sr.UnknownValueError:
        speak_text("Sorry, I did not understand that. Please try again.")
        return get_voice_input(prompt)

def file_complaint():
    try:
        dealer_name = get_voice_input("Please say the dealer name.")
        vehicle_name = get_voice_input("Please say the vehicle name.")
        company = get_voice_input("Please say the vehicle company name.")
        odometer_reading = get_voice_input("Please say the odometer reading.")
        days_since_purchase = get_voice_input("Please say the number of days completed from the date of purchase.")
        dealer_address = get_voice_input("Please say the dealer address.")
        infotainment_serial_no = get_voice_input("Please say the infotainment serial number.")
        city = get_voice_input("Please say the city name.")

        # Validate odometer reading
        if int(odometer_reading) > 40000:
            speak_text('Sorry, your warranty has expired. Warranty claimed if the odometer reading was within 40000 KM, Currently we are not able to register your complaint. Kindly contact our service team')
            return

        # Validate days since purchase
        if int(days_since_purchase) > 730:
            speak_text('Sorry, your warranty has expired. 2 years or 730 days completed from the date of sale of the vehicle, Currently, we are not able to register your complaint. Kindly contact our service team.')
            return

        # Check for duplicate infotainment serial number
        if is_duplicate_complaint(infotainment_serial_no):
            complaint_id = get_complaint_id(infotainment_serial_no)
            response_text = f'Your complaint has already been registered with Complaint ID: {complaint_id}.'
            speak_text(response_text)
            return

        complaint_id = generate_complaint_id()
        store_complaint(complaint_id, dealer_name, company, vehicle_name, odometer_reading, days_since_purchase, dealer_address, infotainment_serial_no, city)
        
        response_text = f'Your complaint has been filed successfully. Complaint ID: {complaint_id}. Dealer Name: {dealer_name}, Vehicle Name: {vehicle_name}, Company: {company}, Dealer Address: {dealer_address}, Infotainment Serial Number: {infotainment_serial_no}, City: {city}'
        speak_text(response_text)
        speak_text(f'Your complaint number is {complaint_id}. Please keep it for future reference.')
        
        # Save the response text as a voice recording for backend
        response_tts = gTTS(text=response_text, lang='en')
        response_tts.save(f"complaint_{complaint_id}.mp3")

        # Save the response text as PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=response_text)
        pdf.output(f"complaint_{complaint_id}.pdf")

    except Exception as e:
        speak_text(f'An error occurred while filing the complaint: {str(e)}')

def provide_complaint_details(complaint_id):
    try:
        complaint = get_complaint_details(complaint_id)
        if complaint:
            response_text = f"Complaint ID: {complaint[0]}, Dealer Name: {complaint[1]}, Vehicle Name: {complaint[3]}, Company: {complaint[2]}, Odometer Reading: {complaint[4]}, Days Since Purchase: {complaint[5]}, Dealer Address: {complaint[6]}, Infotainment Serial Number: {complaint[7]}, City: {complaint[8]}"
            speak_text(response_text)
        else:
            speak_text(f"No complaint found with ID: {complaint_id}")
    except Exception as e:
        speak_text(f'An error occurred while retrieving the complaint details: {str(e)}')

if __name__ == '__main__':
    speak_text("Thank you for calling. I am Laami. How can I help you?")
    while True:
        user_input = get_voice_input("Please say 'register a complaint' to file a complaint, or provide a complaint number to get details.")
        if any(phrase in user_input.lower() for phrase in ["register a complaint", "file a complaint", "complaint", "a complaint"]):
            file_complaint()
        elif any(phrase in user_input.lower() for phrase in ["mail id", "customer mail", "email", "e mail"]):
            speak_text("The customer email is infotainment@gmail.com")
        elif any(phrase in user_input.lower() for phrase in ["warranty period", "warranty claim", "warranty"]):
            speak_text("The warranty period is 730 days from the date of sale and less than 40000 KM.")
        elif user_input.lower().isdigit():
            provide_complaint_details(user_input.lower())
        else:
            speak_text("Okay, let me know if you need anything else.")
