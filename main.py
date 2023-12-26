BACKGROUND_COLOR = "#B1DDC6"
MY_FONT = "Ariel"
from tkinter import *
from tkinter import messagebox
from pandas import *
from random import *


card = {}
score = 0

# ---------------------------- FUNCTIONS ------------------------------- #


def get_new_card(dict_to_study):
    global card
    card = choice(deck_to_study)
    return card

def show_front():
    global card
    card = get_new_card(deck_to_study)
    main_canvas.itemconfig(title, text="Kanji")
    main_canvas.itemconfig(pic, image=front_pic)
    main_canvas.itemconfig(target_word, text=f'{card["Kanji"]}')
    check.grid_remove()
    x.grid_remove()

def show_back():
    global card
    main_canvas.itemconfig(pic, image=back_pic)
    main_canvas.itemconfig(title, text="Hiragana and English")
    main_canvas.itemconfig(target_word, text=f"{card['Hiragana']}\n{card['English']}")
    check.grid(column=1, row=1)
    x.grid(column=0, row=1)


def countdown(count):
    main_canvas.itemconfig(timer, text=f"{count}")
    if counting := count > 0:
        timer_seq = window.after(1000, countdown, count - 1)
    else:
        show_back()


def sequence():
    show_front()
    countdown(3)


def card_remembered():
    global card
    scored()
    learned_deck.append(card)
    deck_to_study.remove(card)
    if len(deck_to_study) > 0:
        sequence()
    else:
        messagebox.showinfo(title="Finished", message="Congratulations! You studied all the vocabulary!")
        window.quit()

def not_remembered():
    if len(deck_to_study) > 0:
        sequence()
    else:
        messagebox.showinfo(title="Finished", message="Congratulations! You studied all the vocabulary!")
        window.quit()

def scored():
    global score
    score += 1
    main_canvas.itemconfig(scoreboard, text=f"Score: {score}")


vocab_data = read_csv("data/japanese_vocab.csv")
deck_to_study = vocab_data.to_dict(orient="records")
learned_deck = []

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

front_pic = PhotoImage(file="images/card_front.png")
back_pic = PhotoImage(file="images/card_back.png")
right = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")

main_canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
pic = main_canvas.create_image(400, 263, image=front_pic)
title = main_canvas.create_text(400, 103, text="Kanji", font=(MY_FONT, 30, "italic"))
target_word = main_canvas.create_text(400, 263, text="",
                                      font=(MY_FONT, 40, "bold"), justify="center")
timer = main_canvas.create_text(400, 380, text="3", font=(MY_FONT, 40))
main_canvas.grid(column=0, row=0, columnspan=2)
scoreboard = main_canvas.create_text(400, 450,
                                     text=f"Score: {score}", font=(MY_FONT, 30), justify="center")
check = Button(image=right, bg=BACKGROUND_COLOR, command=card_remembered)
x = Button(image=wrong, bg=BACKGROUND_COLOR, command=not_remembered)

sequence()

window.mainloop()


