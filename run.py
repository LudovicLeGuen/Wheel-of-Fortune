"""
The Wheel or fortune game.
"""

import random
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('wheel-of-fortune')

guessed_letters = []
GUESS = ""
MYSTERY_SENTENCE = ""
HIDE_SENTENCE = ""
PLAYER1 = ""
PLAYER2 = ""
round = "1"
VOWELS = ["a", "e", "i", "o", "u"]
CONSONANT = ["b", "c", "d", "f", "g", "h", "j", "k", "l",
             "m", "n", "p", "q", "r", "s", "t", "v", "w",
             "x", "y", "z"]
CASH = 0
PLAYER1CASH = 0
PLAYER2CASH = 0
WHEEL = ["Bankrupt", 600, 400, 300, "Pass your turn",
         800, 350, 450, 700, 300, 600, "Bankrupt", 600, 500, 300, 500,
         800, 550, 400, 300, 900, 500, 300, 900]

title = SHEET.worksheet('title')
data = title.get_all_values()


def play_game():
    """
    The Funtion starts the game and registers the 2 players names.
    """
    global PLAYER1, PLAYER2
    print("Hello and welcome to the Wheel ... of ...  Fortuuuuuune!")
    print("\n")
    print("My Name is Mr Boty and I will be your host!")
    print("\n")
    print("Lets introduce our 2 contestants. ")
    print("\n")
    PLAYER1 = str(input("Contestant 1. What is you name please? "))
    print("Welcome and good luck " + str(PLAYER1))
    print("\n")

    PLAYER2 = str(input("Contestant 2. How should we call you? "))
    print("Thank you and good luck to you too " + str(PLAYER2))
    print("\n")
    print("And now that we know our 2 contestants,")
    print("\n")
    print("Let's have a look at the rules!")
    print("\n")


def rules():
    """
    The function shows the game rules and ask whether the players
    have understood them and are ready to proceed.
    """
    print("The rules are simple:")
    print("\n")
    print("- Turn the wheel to get a cash value and guess a consonant.")
    print("\n")
    print("- The cash value will be multiplied by the number of consonant")
    print("  in the mystery sentence and will be added to your jackpot.")
    print("\n")
    print("- After guessing a correct consonant, you can:")
    print("  a - buy a Vowel for 250$")
    print("  b - turn the wheel and find a new consonant")
    print("  c - guess the mystery sentence")
    print("\n")
    print("- You will pass your turn if:")
    print("  a - your consonant is not in the mystery sentence")
    print("  b - you guess incorrecty the mystery sentence")
    print("  c - you fall on the 'Pass your turn' case in the wheel")
    print("  d - you fall on the 'Bankrupt' case. You will")
    print("  also lose all your earnings. OUCH!! THOUGH LUCK!")
    print("\n")
    print('Have you understood the rules? (type yes when ready)')


def player_input():
    """
    Functions registers the player answer to continue playing or not
    """
    user_input = ''
    while True:
        user_input = input("->")

        if user_input.lower() != 'yes':
            print("It's ok. We have all the time in the world")
            print("Enter yes when you are ready")
            continue

        else:
            print('Very well. Here we go!')

            break
        return user_input.lower()


def select_row():
    """
    The function selects randomly a row in the google
    worksheet called "title" and creates a quote
    said by Mr Boty and the sentence to guess in the turn.
    """
    global MYSTERY_SENTENCE
    row = random.choice(list(data))
    MYSTERY_SENTENCE = row[0].lower()
    print("Dear contestants,")
    print(f"in the '{row[4]}' category.\n")
    print(f"The guess contains {row[1]} words and {row[2]} letters.\n")
    print("Take it away!")
    print(MYSTERY_SENTENCE)
    return MYSTERY_SENTENCE


def convert_letter(MYSTERY_SENTENCE):
    """
    The function turns each letter of the sentence
    created in the function in an underscore and therefore
    creates the guess users will try to solve.
    The function is inspired by Hayley Guillou on stack overflow
    https://stackoverflow.com/questions/32960141/how-can-i-replace-the-letters-of-a-string-with-underscores
    """
    global HIDE_SENTENCE
    HIDE_SENTENCE = MYSTERY_SENTENCE
    for i in range(0, len(MYSTERY_SENTENCE)):
        if ord(MYSTERY_SENTENCE[i]) != 32:
            HIDE_SENTENCE = HIDE_SENTENCE.replace(MYSTERY_SENTENCE[i], '_')
    print(HIDE_SENTENCE)


def turn_wheel():
    """
    The function gets the cash value from the wheel list.
    """
    global CASH, PLAYER1CASH
    print("\n")
    print(f'{PLAYER1}, are you ready to turn the wheel? (type yes when ready)')

    player_input()

    CASH = random.choice(WHEEL)

    if CASH == "Bankrupt":
        print("\n")
        print("OH GOSH! You fell on BANKRUPT.")
        print("You lose ALL your earnings and pass your turn")
        print("That is really unlucky")
        PLAYER1CASH = 0

    elif CASH == "Pass your turn":
        print("\n")
        print("Too bad, You fell on PASS YOUR TURN.")
        print("It is now your opponent turn.")
        print("Sorry")

    else:
        print(f"Well done!{PLAYER1}!")
        print(f"You play for {CASH}$")
        player_guess()


def player_guess():
    """
    This function check if the player guess is a consonant or not,
    if the guess has been guessed before and if the user guessed
    a single letter.
    """
    print("\n")
    print(PLAYER1 + ". What will be your consonant?")
    global GUESS
    while True:
        GUESS = input("Type a consonant -> ")

        if len(GUESS) != 1:
            print(f"Sorry {PLAYER1} you have inserted more than one letter.")
            print("Please guess a single consonant")
            print("\n")
            continue

        elif GUESS not in CONSONANT:
            print(f"Sorry {GUESS.upper()} is not a consonant.")
            print("Please enter a consonant")
            print("\n")
            continue

        elif GUESS in guessed_letters:
            print(f"Sorry, {GUESS.upper()} has already been guessed.")
            print("Please enter another consonant")
            print("\n")
            continue

        else:
            print('Thank you ' + str(PLAYER1))
            print(f"Let's see if the letter '{GUESS.upper()}' ")
            print("is in the mystery sentence.")
            print("\n")
            guessed_letters.append(GUESS)
            compare_print()
            break


def compare_print():
    """ The function compares the users guess with the mystery 
    sentence and print the letters that are correct.
    The function then gives a choice to the player who can either 
    guess the sentence, buy a vowel or turn the wheel again"""
    global HIDE_SENTENCE, PLAYER1CASH
    hidden_list = list(HIDE_SENTENCE)
    indices = [
        i for i, letter in enumerate(MYSTERY_SENTENCE) if letter == GUESS
        ]
    for index in indices:
        hidden_list[index] = GUESS
        HIDE_SENTENCE = "".join(hidden_list)
    print(HIDE_SENTENCE)

    letter_count = MYSTERY_SENTENCE.count(GUESS)
    print("\n")
    print(f"Congratulations {PLAYER1}")
    if letter_count == 1:
        print(f"{GUESS.upper()} is found once in the mystery sentence")
    else:
        print(f"{GUESS.upper()} is found {letter_count} times")
        print("in the sentence!")

    earnings = int(letter_count)*CASH
    PLAYER1CASH = int(earnings) + int(PLAYER1CASH)
    print(f"You earned {earnings}$!!!")
    print(f"{PLAYER1} your have now have {PLAYER1CASH}$ in the bank.")
    print("\n")
    print(f"Dear {PLAYER1}")
    print("Now that you have found a correct consonant in ")
    print("the mystery sentence, you are allowed to either: ")
    print("  a - buy a Vowel for 250$")
    print("  b - turn the wheel and find a new consonant")
    print("  c - guess the mystery sentence")
    print("\n")
    print(f"{PLAYER1}, what is your choice please? a, b or c?")
    user_input = input("->")
    if user_input == "a":
        turn_wheel()
    elif user_input == "b":
        turn_wheel()
    elif user_input == "c":
        turn_wheel()
    else:
        print("wrong answer")


def main():
    """
    The function that runs other functions
    """
    play_game()
    rules()
    player_input()
    convert_letter(select_row())
    turn_wheel()


main()
