from tkinter import *
import math
import tkinter.messagebox
import winsound
import threading


def show_project_description():
    project_description = "This is a Pomodoro Timer GUI application.\n\n" \
                          "The Pomodoro Technique is a time management method that uses " \
                          "a timer to have 25 minutes work session accompanied by a 5 minute break ," \
                          " after 4 work sessions are completed , a long break of 30 minutes happens. " \
                          "Customize your timer to change timer depending on your activities.\n\n" \
                          "Enjoy using the Pomodoro Timer!"

    tkinter.messagebox.showinfo("Project Description", project_description)


def customize_timer():

    # Create a Toplevel window for customization dialog
    customize_window = Toplevel(window)
    customize_window.title("Customize Timer")
    customize_window.config(padx=20, pady=20)

    # Create and position labels and entry widgets for user input
    work_label = Label(customize_window, text="Work Duration (minutes):")
    work_entry = Entry(customize_window)
    work_label.grid(row=0, column=0, padx=5, pady=5)
    work_entry.grid(row=0, column=1, padx=5, pady=5)

    short_break_label = Label(customize_window, text="Short Break Duration (minutes):")
    short_break_entry = Entry(customize_window)
    short_break_label.grid(row=1, column=0, padx=5, pady=5)
    short_break_entry.grid(row=1, column=1, padx=5, pady=5)

    long_break_label = Label(customize_window, text="Long Break Duration (minutes):")
    long_break_entry = Entry(customize_window)
    long_break_label.grid(row=2, column=0, padx=5, pady=5)
    long_break_entry.grid(row=2, column=1, padx=5, pady=5)

    # Function to apply the custom settings and close the dialog
    def apply_custom_settings():
        global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN
        # if user input is digit , then accept the input or take the  default value
        WORK_MIN = int(work_entry.get()) if work_entry.get().isdigit() else WORK_MIN
        SHORT_BREAK_MIN = int(short_break_entry.get()) if short_break_entry.get().isdigit() else SHORT_BREAK_MIN
        LONG_BREAK_MIN = int(long_break_entry.get()) if long_break_entry.get().isdigit() else LONG_BREAK_MIN
        customize_window.destroy()

    # Create the Apply button to apply custom settings
    apply_button = Button(customize_window, text="Apply", command=apply_custom_settings)
    apply_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)


def play_alarm_sound():
    winsound.Beep(1000, 2000)  # Play alarm sound with frequency 1000 Hz for 1000 ms (1 second)

# ---------------------------- CONSTANTS ------------------------------- #


PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 1
LONG_BREAK_MIN = 1
REPS = 0
TIMER = None

# ---------------------------- TIMER RESET ------------------------------- # 


def reset_timer():
    window.after_cancel(TIMER)
    Timer_label.config(text="Timer")
    canvas.itemconfig(timer_text, text="00:00")
    Correct_Label.config(text="")
    global REPS
    REPS = 0


# ---------------------------- TIMER MECHANISM ------------------------------- # 


def start_timer():
    global REPS
    REPS += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if REPS % 8 == 0:
        count_down(long_break_sec)
        Timer_label.config(text="Break", fg=RED)
    elif REPS % 2 == 0:
        count_down(short_break_sec)
        Timer_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        Timer_label.config(text="Work", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    count_minute = math.floor(count / 60)
    count_second = count % 60

    if count_second < 10:
        count_second = f"0{count_second}"
    canvas.itemconfig(timer_text, text=f"{count_minute}:{count_second}")
    if count > 0:
        global TIMER
        TIMER = window.after(1000, count_down, count-1)
    else:
        start_timer()
        mark = ""
        work_sessions = math.floor(REPS/2)
        for n in range(work_sessions):
            mark += "✔"
        Correct_Label.config(text=mark, font=(FONT_NAME, 20))
        # Show break end notification
        if REPS % 2 != 0 and REPS == 1:
            threading.Thread(target=play_alarm_sound).start()  # Start the alarm sound in a new thread
            tkinter.messagebox.showinfo("Break Ended", "Break time is over. Get back to work!")



# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)

timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

Timer_label = Label(text="Timer", font=(FONT_NAME, 50, "bold"), fg=GREEN, bg=YELLOW)
Timer_label.grid(row=0, column=1)

start_button = Button(text="Start", font=FONT_NAME, fg=RED, highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)

end_button = Button(text="Reset", font=FONT_NAME, fg=RED, highlightthickness=0, command=reset_timer)
end_button.grid(row=2, column=2)

Correct_Label = Label(fg=GREEN, bg=YELLOW)
Correct_Label.grid(row=2, column=1)
Correct_Label.config(pady=50)

customize_button = Button(text="Customize Your Timer", font=FONT_NAME, fg=RED, highlightthickness=0, command=customize_timer)
customize_button.grid(row=3, column=1)

info_icon_img = PhotoImage(file="description.png")
info_icon_img = info_icon_img.subsample(2, 2)
info_icon_label = Label(image=info_icon_img, bg=YELLOW, borderwidth=0, highlightbackground=YELLOW, highlightthickness=0)
info_icon_label.grid(row=0, column=2)
info_icon_label.config(cursor="hand2")
info_icon_label.bind("<Button-1>", lambda event: show_project_description())

window.mainloop() # This is a event driven GUI