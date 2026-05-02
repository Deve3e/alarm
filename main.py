import datetime
import threading
import tkinter as tk
from tkinter import messagebox
import winsound

# ---------- THEME CONFIGURATION ----------
current_theme = "light"

themes = {
    "light": {
        "bg": "white",
        "fg": "black",
        "button_bg": "lightgray",
        "button_fg": "black",
        "entry_bg": "white",
        "entry_fg": "black"
    },
    "dark": {
        "bg": "#2b2b2b",
        "fg": "white",
        "button_bg": "#4a4a4a",
        "button_fg": "white",
        "entry_bg": "#3a3a3a",
        "entry_fg": "white"
    }
}

def apply_theme():
    theme = themes[current_theme]
    app.config(bg=theme["bg"])
    top_frame.config(bg=theme["bg"])
    content_frame.config(bg=theme["bg"])
    label_title.config(bg=theme["bg"], fg=theme["fg"])
    entry_time.config(bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["fg"])
    btn_set.config(bg=theme["button_bg"], fg=theme["button_fg"])
    btn_toggle.config(bg=theme["button_bg"], fg=theme["button_fg"])
    label_status.config(bg=theme["bg"], fg="green" if current_theme == "light" else "lightgreen")

def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme()
    btn_toggle.config(text="🌙" if current_theme == "dark" else "☀️")

# ---------- ALARM FUNCTION ----------
def alarm_loop(alarm_time, label_status):
    while True:
        now = datetime.datetime.now()
        if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
            for _ in range(10):  # Beep 5 times
                winsound.Beep(2000, 1000)
                winsound.Beep(100, 1000)  # Beep at 2000 Hz for 1000 ms
            label_status.config(text="⏰ Time's up!")
            break

# ---------- START ALARM ----------
def set_alarm():

    input_time = entry_time.get()
    try:
        alarm_time = datetime.datetime.strptime(input_time, "%H:%M").time()
        label_status.config(text=f"Alarm set for {input_time}")

        # Run alarm in separate thread so UI doesn't freeze
        threading.Thread(target=alarm_loop, args=(alarm_time, label_status), daemon=True).start()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter time in HH:MM format")

# ---------- UI ----------
app = tk.Tk()
app.title("Alarm App")
app.geometry("300x250")

# Top frame for the toggle button
top_frame = tk.Frame(app)
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

btn_toggle = tk.Button(top_frame, text="☀️", command=toggle_theme, font=("Arial", 12))
btn_toggle.pack(side=tk.LEFT)

# Main content frame
content_frame = tk.Frame(app)
content_frame.pack(expand=True)

label_title = tk.Label(content_frame, text="Set Alarm (HH:MM)", font=("Arial", 14))
label_title.pack(pady=10)

entry_time = tk.Entry(content_frame, font=("Arial", 14), justify="center")
entry_time.pack(pady=5)

btn_set = tk.Button(content_frame, text="Set Alarm", command=set_alarm)
btn_set.pack(pady=10)

label_status = tk.Label(content_frame, text="", fg="green")
label_status.pack(pady=10)

apply_theme()  # Apply initial theme

app.mainloop()
