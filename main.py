import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
words_to_learn = {}
current_card = {}

try:
    data = pandas.read_csv("data/words_to_learn")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    words_to_learn = original_data.to_dict(orient="records")
else:
    words_to_learn = data.to_dict(orient="records")


def new_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_to_learn)
    word = current_card["French"]
    canvas.itemconfig(english_french_word, text=word, fill="black")
    canvas.itemconfig(canvas_image, image=card_front_image)
    canvas.itemconfig(language_text, text="French", fill="black")
    window.after(3000, func=flip_card)
    flip_timer = window.after(3000, flip_card)


def flip_card():

    word = current_card["English"]
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(english_french_word, text=word, fill="white")


def is_known():
    words_to_learn.remove(current_card)
    to_learn = pandas.DataFrame(words_to_learn)
    to_learn.to_csv("data/words_to_learn.csv", index=False)
    new_card()


window = Tk()
window.title("Flashcard")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_front_image = PhotoImage(file="images/card_front.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 270, image=card_front_image)
canvas.grid(column=0, row=0, columnspan=2)
language_text = canvas.create_text(400, 150, text="French", fill="black", font=("Arial", 40, "italic"))
english_french_word = canvas.create_text(400, 263, text="word", fill="black", font=("Arial", 60, "bold"))

right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)
right_button.config(padx=50, pady=50)

wrong_button = Button(image=wrong_image, highlightthickness=0, command=new_card)
wrong_button.grid(column=0, row=1)
wrong_button.config(pady=50, padx=50)


new_card()

window.mainloop()
