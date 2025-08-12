import requests
import time
import pygame

pygame.mixer.init()

def play_sound():
    pygame.mixer.music.load('alert.mp3')
    pygame.mixer.music.play()

def get_original_ip():
    original_ip = input("Enter your original IP address: ")
    return original_ip.strip()

def check_ip(original_ip):
    while True:
        try:
            response = requests.get('https://api.ipify.org?format=json')
            current_ip = response.json().get('ip')
            print(f"[INFO]Current IP: {current_ip}")

            if current_ip == original_ip:
                print(f"[WARNING]IP leak detected! Original IP equals checked IP: {current_ip}")
                play_sound()
                time.sleep(2)
                break

            time.sleep(5)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def main():
    original_ip = get_original_ip()
    proxy_started = input("Is your proxy started? (yes/no): ").strip().lower()

    if proxy_started == 'yes':
        print("[INFO]Starting IP check...")
        check_ip(original_ip)
    else:
        print("[INFO]Proxy not started. Exiting.")
        time.sleep(3)
        quit

if __name__ == "__main__":
    main()
