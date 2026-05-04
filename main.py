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

def format_time(*args):
    value = entry_var.get()
    # Remove non-digits
    digits = ''.join(c for c in value if c.isdigit())
    # Limit to 4 digits
    digits = digits[:4]
    
    if len(digits) == 4:
        hours = int(digits[:2])
        minutes = int(digits[2:])
        # Clamp values
        hours = min(max(hours, 0), 23)
        minutes = min(max(minutes, 0), 59)
        formatted = f"{hours:02d}:{minutes:02d}"
    elif len(digits) >= 3:
        # If 3 digits, assume first 2 are hours, last is first digit of minutes
        hours = int(digits[:2])
        hours = min(max(hours, 0), 23)
        formatted = f"{hours:02d}:{digits[2]}"
    elif len(digits) >= 1:
        formatted = digits[:2]  # Up to 2 digits for hours
    else:
        formatted = ''
    
    # Update if changed
    if formatted != value:
        entry_var.set(formatted)

# ---------- INPUT FORMATTING ----------
def alarm_loop(alarm_time, label_status):
    while True:
        now = datetime.datetime.now()
        if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
            for _ in range(10):  # Beep 5 times
                winsound.Beep(2000, 1000)
                winsound.Beep(100, 1000)  # Beep at 2000 Hz for 1000 ms
            label_status.config(text="⏰ Alarm Time's up!")
            break

# ---------- START ALARM ----------
def set_alarm():
    input_time = entry_time.get()
    try:
        # Parse HH:MM format
        if ':' in input_time:
            hours, minutes = input_time.split(':')
            hours = int(hours)
            minutes = int(minutes)
            if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                raise ValueError
        else:
            raise ValueError
        alarm_time = datetime.time(hours, minutes)
        label_status.config(text=f"Alarm set for {input_time}")

        # Run alarm in separate thread so UI doesn't freeze
        threading.Thread(target=alarm_loop, args=(alarm_time, label_status), daemon=True).start()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter time in HH:MM format (00:00 to 23:59)")

# ---------- UI ----------
app = tk.Tk()
app.title("Alarm App")
app.geometry("300x250")

entry_var = tk.StringVar()
entry_var.trace('w', format_time)

# Top frame for the toggle button
top_frame = tk.Frame(app)
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

btn_toggle = tk.Button(top_frame, text="☀️", command=toggle_theme, font=("Segoe UI Emoji", 12))
btn_toggle.pack(side=tk.LEFT)

# Main content frame
content_frame = tk.Frame(app)
content_frame.pack(expand=True)

label_title = tk.Label(content_frame, text="Set Alarm (HH:MM)", font=("Arial", 14))
label_title.pack(pady=10)

entry_time = tk.Entry(content_frame, font=("Arial", 14), justify="center", textvariable=entry_var)
entry_time.pack(pady=5)

btn_set = tk.Button(content_frame, text="Set Alarm", command=set_alarm)
btn_set.pack(pady=10)

label_status = tk.Label(content_frame, text="", fg="green")
label_status.pack(pady=10)

apply_theme()  # Apply initial theme

app.mainloop()
