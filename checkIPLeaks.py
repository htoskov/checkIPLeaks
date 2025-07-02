import requests
import time
import pygame

# Initialize pygame mixer
pygame.mixer.init()

def play_sound():
    pygame.mixer.music.load('alert.mp3')  # Make sure to have an alert sound file named 'alert.mp3'
    pygame.mixer.music.play()

def get_original_ip():
    original_ip = input("Enter your original IP address: ")
    return original_ip.strip()

def check_ip(original_ip):
    while True:
        try:
            # Get the current public IP from an API
            response = requests.get('https://api.ipify.org?format=json')
            current_ip = response.json().get('ip')
            print(f"Current IP: {current_ip}")

            # Check if the current IP matches the original IP
            if current_ip == original_ip:
                print(f"IP leak detected! Original IP equals checked IP: {current_ip}")
                play_sound()  # Play sound when leak is detected
                break

            time.sleep(0.1)  # Wait for 0.1 seconds before the next check
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def main():
    original_ip = get_original_ip()
    proxy_started = input("Is your proxy started? (yes/no): ").strip().lower()

    if proxy_started == 'yes':
        print("Starting IP check...")
        check_ip(original_ip)
    else:
        print("Proxy not started. Exiting.")

if __name__ == "__main__":
    main()
