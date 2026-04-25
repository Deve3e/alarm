import datetime
import winsound
input_time = input("Enter the time for the alarm (HH:MM): ")
alarm_time = datetime.datetime.strptime(input_time, "%H:%M").time()
def main(alarm_time):
    while True:
        x = datetime.datetime.now()
        if x.hour == alarm_time.hour and x.minute == alarm_time.minute:
            print(winsound.Beep(1000, 1000), "⏰ Time's up! Playing alarm sound...")
            break

main(alarm_time)