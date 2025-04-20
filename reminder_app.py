import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
from datetime import datetime, timedelta
import time

# Show the reminder in a new window
def show_reminder(message):
    popup = tk.Tk()
    popup.title("Reminder")
    popup.geometry("400x200")

    label = tk.Label(popup, text=message, font=("Arial", 16), pady=20)
    label.pack()

    btn = tk.Button(popup, text="OK", command=popup.destroy)
    btn.pack(pady=10)

    popup.mainloop()

# Runs in the background and waits until the set time
def reminder_thread(reminder_time, message):
    while True:
        now = datetime.now()
        if now >= reminder_time:
            show_reminder(message)
            break
        time.sleep(1)

# Set the reminder from user input
def set_reminder():
    task = simpledialog.askstring("What to do?", "What do you want to be reminded about?")
    if not task:
        return

    time_str = simpledialog.askstring("Reminder Time", "Enter time (HH:MM)")
    if not time_str:
        return

    try:
        now = datetime.now()
        reminder_time = datetime.strptime(time_str, "%H:%M")
        reminder_time = reminder_time.replace(year=now.year, month=now.month, day=now.day)

        # If the time has already passed today, move it to tomorrow
        if reminder_time < now:
            reminder_time += timedelta(days=1)

        # Start a new thread that waits and shows reminder
        thread = threading.Thread(target=reminder_thread, args=(reminder_time, task))
        thread.daemon = True
        thread.start()

        messagebox.showinfo("Reminder Set", f"Reminder for '{task}' set at {reminder_time.strftime('%H:%M')}")

    except ValueError:
        messagebox.showerror("Invalid Time", "Please enter time in HH:MM format.")

# Main full-screen window
def create_main_menu():
    window = tk.Tk()
    window.title("Reminder Menu")

    # Full-screen
    window.attributes("-fullscreen", True)
    window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))

    label = tk.Label(window, text="Reminder Menu", font=("Arial", 32))
    label.pack(pady=40)

    btn1 = tk.Button(window, text="Set New Reminder", font=("Arial", 20), command=set_reminder)
    btn1.pack(pady=10)

    btn2 = tk.Button(window, text="Exit", font=("Arial", 20), command=window.quit)
    btn2.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_main_menu()
