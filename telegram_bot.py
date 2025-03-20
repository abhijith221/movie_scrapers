import os
import requests
from bs4 import BeautifulSoup
import time
import simpleaudio as sa

# Get credentials from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# URL of the movie booking page
URL = "https://paytm.com/movies/trivandrum/ariesplex-sl-cinemas-cinionic-dolby-atmos-vanchiyoor-thiruvananthapuram-c/1018571"

# Theatre name to check
THEATRE_NAME = "27"

def send_telegram_message(message):
    """Send a message via Telegram bot"""
    telegram_api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
    try:
        response = requests.post(telegram_api_url, data=payload)
        print(f"Telegram notification sent: {response.status_code}")
        return response.json()
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
        return None

def check_booking():
    """Check if booking is available for the specified movie"""
    try:
        response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        if THEATRE_NAME in soup.get_text():
            message = f"🎉 BOOKING STARTED! 🎉\n\nMovie: {THEATRE_NAME}\nLink: {URL}"
            print(message)
            send_telegram_message(message)
            return True
        else:
            print(f"❌ No booking available yet for {THEATRE_NAME} at {time.strftime('%H:%M:%S')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking booking: {e}")
        return False

def main():
    """Main function to run the booking checker"""
    print(f"Starting to check for {THEATRE_NAME} booking availability...")
    send_telegram_message(f"🎬 Bot started! Checking for {THEATRE_NAME} booking availability...")
    
    if check_booking():
        print("✅ Booking found!")
    else:
        print("⏳ No booking found.")

if __name__ == "__main__":
    main()
