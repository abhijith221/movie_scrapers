import requests
from bs4 import BeautifulSoup
import time
import simpleaudio as sa

# Load the alert sound once
wave_obj = sa.WaveObject.from_wave_file("empuraan.wav")
play_obj = None  # To track the playing sound

# URL of the movie booking page
URL = "https://paytm.com/movies/trivandrum/ariesplex-sl-cinemas-cinionic-dolby-atmos-vanchiyoor-thiruvananthapuram-c/1018571"

# Theatre name to check
THEATRE_NAME = "L2: Empuraan"
#THEATRE_NAME = "L2: Empuraan"

def play_alert():
    global play_obj
    if play_obj is not None and play_obj.is_playing():  
        play_obj.stop()  # Only stop if a sound is playing
    play_obj = wave_obj.play()  # Play the new sound

def check_booking():
    try:
        response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()  # Raise an error if request fails

        soup = BeautifulSoup(response.text, "html.parser")

        if THEATRE_NAME in soup.get_text():
            print(f"🎉 Booking started for {THEATRE_NAME}!")
            play_alert() 
            return True  # Stop loop if booking is found
        else:
            print(f"❌ No booking available yet... {THEATRE_NAME}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False

# Run the check every 9 seconds
while True:
    if check_booking():
        break  # Stop checking once booking is available
    time.sleep(9)  # Wait before checking again
