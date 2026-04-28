import datetime
import threading
import tkinter as tk
from tkinter import messagebox
import winsound

# ---------- ALARM FUNCTION ----------
def alarm_loop(alarm_time, label_status):
    while True:
        now = datetime.datetime.now()
        if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
            winsound.Beep(1000, 1000)
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
app.geometry("300x200")

label_title = tk.Label(app, text="Set Alarm (HH:MM)", font=("Arial", 14))
label_title.pack(pady=10)

entry_time = tk.Entry(app, font=("Arial", 14), justify="center")
entry_time.pack(pady=5)

btn_set = tk.Button(app, text="Set Alarm", command=set_alarm)
btn_set.pack(pady=10)

label_status = tk.Label(app, text="", fg="green")
label_status.pack(pady=10)

app.mainloop()
