import requests
from bs4 import BeautifulSoup
import time
import simpleaudio as sa

# Telegram Bot Configuration
BOT_TOKEN = '7843814570:AAGnmnYKb2Ixj_Z70hw39256hbkLDKnxn38'  # Replace with your Telegram bot token
CHAT_ID = '634580559'      # Replace with your Telegram chat ID

# Load the alert sound once
wave_obj = sa.WaveObject.from_wave_file("empuraan.wav")
play_obj = None  # To track the playing sound

# URL of the movie booking page
URL = "https://paytm.com/movies/trivandrum/ariesplex-sl-cinemas-cinionic-dolby-atmos-vanchiyoor-thiruvananthapuram-c/1018571"

# Theatre name to check
THEATRE_NAME = "27"

def send_telegram_message(message):
    """Send a message via Telegram bot"""
    telegram_api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(telegram_api_url, data=payload)
        print(f"Telegram notification sent: {response.status_code}")
        return response.json()
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
        return None

def play_alert():
    """Play local alert sound"""
    global play_obj
    if play_obj is not None:
        play_obj.stop()  # Stop the previous sound if still playing
    play_obj = wave_obj.play()  # Play the new sound

def check_booking():
    """Check if booking is available for the specified movie"""
    try:
        response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()  # Raise an error if request fails
        soup = BeautifulSoup(response.text, "html.parser")
        
        if THEATRE_NAME in soup.get_text():
            message = f"🎉 BOOKING STARTED! 🎉\n\nMovie: {THEATRE_NAME}\nLink: {URL}"
            print(message)
            
            # Send Telegram notification
            send_telegram_message(message)
            
            # Play local alert sound
            play_alert()
            
            return True  # Stop loop if booking is found
        else:
            current_time = time.strftime("%H:%M:%S", time.localtime())
            print(f"❌ No booking available yet for {THEATRE_NAME} at {current_time}")
            return False
    except requests.exceptions.RequestException as e:
        error_message = f"Error checking booking: {e}"
        print(error_message)
        # Optionally notify about errors too
        # send_telegram_message(error_message)
        return False

def main():
    """Main function to run the booking checker"""
    print(f"Starting to check for {THEATRE_NAME} booking availability...")
    print(f"Will send Telegram alerts to chat ID: {CHAT_ID}")
    
    # Send initial message to confirm bot is working
    send_telegram_message(f"🎬 Bot started! Checking for {THEATRE_NAME} booking availability...")
    
    check_interval = 10  # Seconds between checks (increased to avoid rate limiting)
    
    # Run the check at regular intervals
    while True:
        if check_booking():
            break  # Stop checking once booking is available
        time.sleep(check_interval)  # Wait before checking again

if __name__ == "__main__":
    main()