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
MYSTERY_SENTENCE = ""
PLAYER1 = ""
PLAYER2 = ""
ROUND = "1"
VOWELS = ["a", "e", "i", "o", "u"]
CONSONANT = ["b", "c", "d", "f", "g", "h", "j", "k", "l",
             "m", "n", "p", "q", "r", "s", "t", "v", "w",
             "x", "y", "z"]
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
    MYSTERY_SENTENCE = row[0]
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
    guess = MYSTERY_SENTENCE
    for i in range(0, len(MYSTERY_SENTENCE)):
        if ord(MYSTERY_SENTENCE[i]) != 32:
            guess = guess.replace(MYSTERY_SENTENCE[i], '_ ')
    print(guess)


def turn_wheel():
    """
    The function gets the cash value from the wheel list.
    """
    print("\n")
    print(f'{PLAYER1}, are you ready to turn the wheel? (type yes when ready)')

    player_input()

    cash_value = random.choice(WHEEL)

    if cash_value == "Bankrupt":
        print("\n")
        print("OH GOSH! You fell on BANKRUPT.")
        print("You lose ALL your earnings and pass your turn")
        print("That is really unlucky")

    elif cash_value == "Pass your turn":
        print("\n")
        print("Too bad, You fell on PASS YOUR TURN.")
        print("It is now your opponent turn.")
        print("Sorry")

    else:
        print("Well none!")
        print(f"Excellent you play for {cash_value}$")
        return cash_value


def player_guess():
    """
    This function check if the player guess is a consonant or not, 
    if the guess has been guessed before and if the user guessed 
    a single letter.
    """
    print("\n")
    print(PLAYER1 + ". What will be your consonant?")
    player_guess = ''
    while True:
        player_guess = input("Type a consonant -> ")

        if len(player_guess) != 1:
            print(f"Sorry {PLAYER1} you have inserted more than one letter.")
            print("Please guess a single consonant")
            print("\n")
            continue

        elif player_guess not in CONSONANT:
            print(f"Sorry {player_guess.upper()} is not a consonant.")
            print("Please enter a consonant")
            print("\n")
            continue

        elif player_guess in guessed_letters:
            print(f"Sorry, {player_guess.upper()} has already been guessed.")
            print("Please enter another consonant")
            print("\n")
            continue

        else:
            print('Thank you ' + str(PLAYER1))
            print(f"Let's see if the letter '{player_guess.upper()}' ")
            print("is in the mystery sentence.")
            print("\n")
            guessed_letters.append(player_guess)
            print("this is guessed letters " + str(guessed_letters))                      
            break


def main():
    """
    The function that runs other functions
    """
    play_game()
    rules()
    player_input()
    convert_letter(select_row())
    turn_wheel()
    player_guess()


main()
