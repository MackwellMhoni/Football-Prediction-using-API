import requests
import pytz
import os
from datetime import *
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk

# ___________________________________________UI___________________________________
window = tk.Tk()
window.title("Football Prediction")
window.geometry("500x600")

try:
    # Use Pillow to open the file first, which handles more PNG variants
    pil_image = Image.open("image/download.png")
    img = ImageTk.PhotoImage(pil_image)

    image_label = tk.Label(window, image=img)
    image_label.image = img  # Keep a reference
    image_label.pack(pady=10)
except Exception as e:
    # to catch and print the specific reason if the image still fails
    print(f"Pillow Error: {e}")

display_area = scrolledtext.ScrolledText(window, width=55, height=15, font=("Segoe UI", 10))
display_area.pack(pady=10)

status_label = tk.Label(window, text="Ready", fg="blue")
status_label.pack()

# ___________________________________________BACKEND___________________________________
#timezones for location and local location
api_timezone = pytz.timezone("Europe/Madrid")
local_timezone = pytz.timezone("Africa/Johannesburg")


def get_current_datetime(start_date):
    # API typically returns ISO format: 2024-01-30T15:00:00
    local_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
    return api_timezone.localize(local_date).astimezone(local_timezone)


def fetch_data():
    status_label.config(text="Fetching predictions...", fg="orange")
    display_area.delete('1.0', tk.END)
    window.update_idletasks()  # Ensure UI updates before network call

    current_server_time = datetime.now(tz=timezone.utc).astimezone(api_timezone)
    tomorrow = current_server_time.date() + timedelta(days=1)

    headers = {
        'User-Agent': 'python_requests',
        "X-RapidAPI-Key": "ed42443d22mshc07e63312bfe71bp1684f9jsn5fc616bc8ca9",
        "X-RapidAPI-Host": "football-prediction-api.p.rapidapi.com"
    }

    #The dictionary values will be used as query parameters automatically
    params = {
        "iso_date": tomorrow.strftime("%Y-%m-%d"),
        "federation": "UEFA",
        "market": "classic"
    }

    prediction_endpoint = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"

    try:
        # requests.get combines the endpoint and params correctly
        response = requests.get(prediction_endpoint, headers=headers, params=params, timeout=10)

        if response.ok:
            json_data = response.json()
            matches = json_data.get("data", [])

            if not matches:
                display_area.insert(tk.END, f"No matches found for {params['iso_date']}.")
            else:
                matches.sort(key=lambda p: p["start_date"])
                for match in matches:
                    local_start_time = get_current_datetime(match["start_date"])
                    prediction_odds = match.get("odds", {}).get(match["prediction"], "N/A")

                    output = f"{local_start_time.strftime('%H:%M')} | {match['home_team']} vs {match['away_team']}\n"
                    output += f"Pred: {match['prediction']} @ {prediction_odds}\n"
                    output += "-" * 50 + "\n"
                    display_area.insert(tk.END, output)

            status_label.config(text="Update Successful", fg="green")
        else:
            # If still 400, print the server's reason to the console or UI
            error_reason = response.text
            status_label.config(text=f"Error: {response.status_code}", fg="red")
            display_area.insert(tk.END, f"Server message: {error_reason}")

    except Exception as e:
        status_label.config(text="Connection Error", fg="red")
        display_area.insert(tk.END, f"Error: {str(e)}")


# Refresh Button
refresh_btn = tk.Button(window, text="Refresh Predictions", command=fetch_data, bg="#f0f0f0")
refresh_btn.pack(pady=5)

# Trigger initial fetch
window.after(100, fetch_data)
window.mainloop()