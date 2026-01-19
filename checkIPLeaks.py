import time
import subprocess
import sys
from dataclasses import dataclass

import requests


@dataclass
class Config:
    wifi_interface_name: str = "Wi-Fi"

    # Default (will be overridden by user input)
    allowed_leaks_before_kill: int = 2

    # Public IP endpoint(s)
    ip_endpoints = (
        "https://api.ipify.org?format=json",
        "https://ifconfig.me/all.json",
        "https://ipinfo.io/json",
    )

    request_timeout: int = 8


def get_public_ip() -> str:
    last_err = None
    for url in Config.ip_endpoints:
        try:
            r = requests.get(
                url,
                timeout=Config.request_timeout,
                headers={"User-Agent": "checkIPLeaks/1.0"},
            )
            r.raise_for_status()
            data = r.json()

            if "ip" in data and isinstance(data["ip"], str):
                return data["ip"].strip()
            if "IP" in data and isinstance(data["IP"], str):
                return data["IP"].strip()
            if "ip_address" in data and isinstance(data["ip_address"], str):
                return data["ip_address"].strip()

        except Exception as e:
            last_err = e
            continue

    raise RuntimeError(f"Failed to fetch public IP. Last error: {last_err}")


def disable_wifi(interface_name: str) -> None:
    cmd = f'netsh interface set interface name="{interface_name}" admin=disabled'
    subprocess.run(cmd, shell=True, check=True)
    print(f"[OK] Automatically disabled interface '{interface_name}'.")


def show_interfaces() -> None:
    print("\n[INFO] netsh interface show interface:\n")
    out = subprocess.run(
        ["netsh", "interface", "show", "interface"],
        capture_output=True,
        text=True,
        shell=False,
    )
    print(out.stdout.strip() if out.stdout else "(no output)")
    if out.stderr:
        print("\n[STDERR]\n" + out.stderr.strip())


def main() -> None:
    print(
        "\nNOTE: You can find your public IP here before continuing:\n"
        "https://www.whatismyip.com/\n"
    )

    original_ip = input("Enter your ORIGINAL (non-proxy/VPN) public IP address: ").strip()
    if not original_ip:
        print("[ERROR] Original IP cannot be empty.")
        sys.exit(1)

    try:
        interval = float(input("Check interval seconds (recommended 3-10): ").strip())
    except ValueError:
        print("[ERROR] Invalid interval.")
        sys.exit(1)

    if interval <= 0:
        print("[ERROR] Interval must be > 0.")
        sys.exit(1)

    # ---- NEW: ask user how many leaks are allowed ----
    try:
        allowed = int(
            input("How many leaks are allowed before auto-kill? (e.g. 1, 2, 5): ").strip()
        )
        if allowed <= 0:
            raise ValueError
        Config.allowed_leaks_before_kill = allowed
    except ValueError:
        print("[ERROR] Please enter a positive whole number.")
        sys.exit(1)

    vpn_started = input("Is your proxy/VPN started? (yes/no): ").strip().lower()
    if vpn_started != "yes":
        print(
            "[WARN] You said VPN is not started. "
            "This tool is meant to detect leaks while VPN is ON."
        )

    print("[INFO] Monitoring public IP...")
    leak_count = 0

    while True:
        try:
            current_ip = get_public_ip()
            print(f"[INFO] Current IP: {current_ip}")

            if current_ip == original_ip:
                leak_count += 1
                print(
                    f"[WARN] Leak {leak_count}/"
                    f"{Config.allowed_leaks_before_kill}"
                )
            else:
                if leak_count:
                    print("[INFO] VPN restored — resetting leak counter.")
                leak_count = 0

            if leak_count >= Config.allowed_leaks_before_kill:
                print("\n" + "!" * 72)
                print("[LEAK DETECTED] Public IP matches ORIGINAL IP too many times.")
                print(f"IP: {current_ip}")
                print("[AUTO ACTION] Disabling Wi-Fi NOW.")
                print("!" * 72 + "\n")

                try:
                    disable_wifi(Config.wifi_interface_name)
                except Exception as e:
                    print(f"[ERROR] Could not disable Wi-Fi: {e}")
                    show_interfaces()
                    print(
                        "\n[HINT] Update Config.wifi_interface_name at the top of the file."
                    )

                print("\nTo turn on your Wi-Fi again, run this command:")
                print(
                    'netsh interface set interface name="Wi-Fi" admin=enabled'
                )

                break

        except KeyboardInterrupt:
            print("\n[INFO] Stopped by user.")
            break
        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(interval)


if __name__ == "__main__":
    main()
