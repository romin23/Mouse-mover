import pyautogui
import random
import time
import ctypes
import tkinter
import keyboard
import customtkinter as ctki


def rat_move():
    MOVE_SPEED = float(move_speed_txt.get())
    SLEEP_TIME = float(sleep_dur_txt.get())
    user32 = ctypes.windll.user32
    SCREEN_X, SCREEN_Y = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
    try:
        while True:
            if keyboard.is_pressed("q"):
                break
            x = random.randint(0,SCREEN_X)
            y = random.randint(0,SCREEN_Y)
            pyautogui.moveTo(x,y,MOVE_SPEED)
            if checkbox.get():
                pyautogui.click(clicks=2, interval=0.25)
                time.sleep(0.5)
                pyautogui.click(clicks=2, interval=0.25)
            time.sleep(SLEEP_TIME)
            if keyboard.is_pressed("q"):
                break
    except KeyboardInterrupt:
        pass
    

def crash_all():
    root.destroy()

ctki.set_appearance_mode("dark")
ctki.set_default_color_theme("dark-blue")

root = ctki.CTk()
root.title("Rat move ~@romin")
root.iconbitmap("mouse.ico")
root.geometry("350x300")
  
# Setting icon of master window


frame = ctki.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)


move_speed_txt = ctki.CTkEntry(master=frame, width=300, height=30, placeholder_text="Movement Speed(in seconds)")
move_speed_txt.pack(pady=12, padx=10)

sleep_dur_txt = ctki.CTkEntry(master=frame, width=300, height=30, placeholder_text="Delay Duration(in seconds)")
sleep_dur_txt.pack(pady=16, padx=10)

checkbox = ctki.CTkCheckBox(master=frame, text="Random Clicks")
# checkbox.pack(pady=0, padx=0)
checkbox.place(relx=0.23, rely=0.45, anchor=tkinter.CENTER)

start_btn = ctki.CTkButton(master=frame, text="Start",width=300, height=28, hover_color="green", command=rat_move)
start_btn.pack(pady=16, padx=10)

quit_label = ctki.CTkLabel(master=frame, text='Note: Spam "q" or "Q" to stop cursor movement', text_color="red")
# quit_label.pack(pady=0, padx=0)
quit_label.place(relx=0.459, rely=0.68, anchor=tkinter.CENTER)

exit_btn = ctki.CTkButton(master=frame, text="Quit", width=300, height=30, hover_color="red",command=crash_all)
exit_btn.pack(pady=14, padx=10)

root.resizable(False, False)
root.mainloop()



