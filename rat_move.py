import pyautogui
import random
import time
import ctypes
import tkinter
import keyboard
import customtkinter as ctki
import threading

is_moving = False
STOP_HOTKEY = "esc"
click_overlay = None

DEFAULT_MOVE_SPEED = 0.2
DEFAULT_SLEEP_TIME = 1.0


def clamp(val, lower, upper):
    return max(lower, min(val, upper))


def safe_float(value, default, lower, upper):
    try:
        return clamp(float(value), lower, upper)
    except (TypeError, ValueError):
        return default


def ensure_overlay():
    global click_overlay
    if click_overlay is not None:
        return
    overlay = tkinter.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes("-topmost", True)
    try:
        overlay.wm_attributes("-transparentcolor", "#010101")
    except tkinter.TclError:
        pass
    overlay.configure(bg="#010101")
    label = tkinter.Label(overlay, text="●", fg="#00ff88", bg="#010101", font=("Segoe UI", 16, "bold"))
    label.pack()
    overlay.withdraw()
    click_overlay = overlay


def show_click_overlay(x, y):
    if click_overlay is None:
        return
    def _show():
        size = 24
        click_overlay.geometry(f"{size}x{size}+{int(x)}+{int(y)}")
        click_overlay.deiconify()
        click_overlay.lift()
        root.after(180, click_overlay.withdraw)
    root.after(0, _show)


def mouse_movement_loop(move_speed, sleep_time):
    global is_moving
    user32 = ctypes.windll.user32
    SCREEN_X, SCREEN_Y = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
    try:
        while is_moving:
            if keyboard.is_pressed("q"):
                break

            if checkbox.get():
                square_width = float(square_slider.get())
                half = square_width / 2
                cx, cy = pyautogui.position()
                start_cx, start_cy = cx, cy  # keep the starting center to avoid drift to last corner
                points = [
                    (clamp(cx - half, 0, SCREEN_X), clamp(cy - half, 0, SCREEN_Y)),
                    (clamp(cx + half, 0, SCREEN_X), clamp(cy - half, 0, SCREEN_Y)),
                    (clamp(cx + half, 0, SCREEN_X), clamp(cy + half, 0, SCREEN_Y)),
                    (clamp(cx - half, 0, SCREEN_X), clamp(cy + half, 0, SCREEN_Y)),
                ]
                for px, py in points:
                    pyautogui.moveTo(px, py, move_speed)
                    pyautogui.click(clicks=2, interval=0.25)
                    show_click_overlay(px + 10, py + 10)
                    if keyboard.is_pressed("q") or not is_moving:
                        break
                # Return to the starting center instantly so the next cycle does not drift toward the last corner
                pyautogui.moveTo(start_cx, start_cy, duration=0)
                time.sleep(sleep_time)
                continue

            x = random.randint(0, SCREEN_X)
            y = random.randint(0, SCREEN_Y)
            pyautogui.moveTo(x, y, move_speed)
            time.sleep(sleep_time)
            if keyboard.is_pressed("q"):
                break
    except KeyboardInterrupt:
        pass
    finally:
        is_moving = False

def rat_move():
    global is_moving
    if not is_moving:
        is_moving = True
        move_speed = safe_float(move_speed_txt.get(), DEFAULT_MOVE_SPEED, 0.01, 10.0)
        sleep_time = safe_float(sleep_dur_txt.get(), DEFAULT_SLEEP_TIME, 0.0, 60.0)
        # reflect normalized values back to the entries so the user sees what is applied
        move_speed_txt.delete(0, tkinter.END)
        move_speed_txt.insert(0, str(move_speed))
        sleep_dur_txt.delete(0, tkinter.END)
        sleep_dur_txt.insert(0, str(sleep_time))

        thread = threading.Thread(target=mouse_movement_loop, args=(move_speed, sleep_time), daemon=True)
        thread.start()
    

def stop_move():
    global is_moving
    is_moving = False


def crash_all():
    keyboard.unhook_all_hotkeys()
    root.destroy()

ctki.set_appearance_mode("dark")
ctki.set_default_color_theme("dark-blue")

root = ctki.CTk()
root.title("Rat move ~@romin")
root.iconbitmap("mouse.ico")
root.geometry("420x480")
root.minsize(380, 420)

ensure_overlay()

frame = ctki.CTkFrame(master=root)
frame.pack(pady=18, padx=18, fill="both", expand=True)

title_label = ctki.CTkLabel(master=frame, text="Rat Move", font=("Segoe UI", 18, "bold"))
title_label.pack(pady=(8, 4))

subtitle_label = ctki.CTkLabel(master=frame, text="Set speed, delay, and optional square clicking", font=("Segoe UI", 12))
subtitle_label.pack(pady=(0, 10))

move_label = ctki.CTkLabel(master=frame, text="Movement speed (seconds)")
move_label.pack(pady=(6, 2), padx=10, anchor="w")
move_speed_txt = ctki.CTkEntry(master=frame, width=320, height=30, placeholder_text="e.g. 0.2")
move_speed_txt.insert(0, str(DEFAULT_MOVE_SPEED))
move_speed_txt.pack(pady=(0, 10), padx=10, fill="x")

sleep_label = ctki.CTkLabel(master=frame, text="Delay between moves (seconds)")
sleep_label.pack(pady=(4, 2), padx=10, anchor="w")
sleep_dur_txt = ctki.CTkEntry(master=frame, width=320, height=30, placeholder_text="e.g. 1.0")
sleep_dur_txt.insert(0, str(DEFAULT_SLEEP_TIME))
sleep_dur_txt.pack(pady=(0, 12), padx=10, fill="x")

checkbox = ctki.CTkCheckBox(master=frame, text="Enable square double-click pattern")
checkbox.pack(pady=6, padx=10, anchor="w")

square_row = ctki.CTkFrame(master=frame)
square_row.pack(fill="x", padx=10, pady=(4, 10))
square_label = ctki.CTkLabel(master=square_row, text="Square width (px)")
square_label.pack(side="left")
square_slider = ctki.CTkSlider(master=square_row, from_=20, to=200, number_of_steps=18)
square_slider.set(80)
square_slider.pack(side="left", fill="x", expand=True, padx=(10, 0))

start_btn = ctki.CTkButton(master=frame, text="Start", height=32, hover_color="green", command=rat_move)
start_btn.pack(pady=(12, 8), padx=10, fill="x")

exit_btn = ctki.CTkButton(master=frame, text="Quit", height=32, hover_color="red", command=crash_all)
exit_btn.pack(pady=(0, 12), padx=10, fill="x")

quit_label = ctki.CTkLabel(master=frame, text='Press "q" or "Esc" to stop (Esc works in background)', text_color="red")
quit_label.pack(pady=(0, 6), padx=10)

root.resizable(True, True)
keyboard.add_hotkey(STOP_HOTKEY, stop_move)
root.mainloop()



