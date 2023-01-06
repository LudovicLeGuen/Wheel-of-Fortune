"""
The Wheel or fortune game.
"""

import sys
import time
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

PLAYER = ["", ""]
PLAYER_BANK = [0, 0]
ROUND_BANK = [0, 0]
CASH = 0
ROUND = 1
TURN = 0
guessed_letters = []
GUESS = ""
MYSTERY_SENTENCE = ""
HIDE_SENTENCE = ""
VOWELS = ["a", "e", "i", "o", "u"]
CONSONANT = ["b", "c", "d", "f", "g", "h", "j", "k", "l",
             "m", "n", "p", "q", "r", "s", "t", "v", "w",
             "x", "y", "z"]

WHEEL = ["Bankrupt", 600, 400, 300, "Pass your turn",
         800, 350, 450, 700, 300, 600, "Bankrupt", 600, 500, 300, 500,
         800, 550, 400, 300, 900, 500, 300, 900]

title = SHEET.worksheet('title')
data = title.get_all_values()


def print(s):
    """
    Used to add a typing effect when printing on the terminal
    """
    for letters in s + '\n':
        sys.stdout.write(letters)
        sys.stdout.flush()
        time.sleep(1./25)


def player_turn():
    """
    This function defines the player who will play
    the turn by populating the PLAYER variable index with
    a 0 or a 1 thanks to the modulo.
    PLAYER[0]= player 1, PLAYER[1] = player 2
    """
    return PLAYER[TURN % 2]


def play_game():
    """
    The Funtion starts the game and registers the 2 players names.
    """
    print("Hello and welcome to the Wheel ... of ...  Fortuuuuuune!")
    print("\nMy Name is Mr Boty and I will be your host!")
    print("I am really glad to have you with us today.")
    print("Lets start by introducing our 2 contestants shall we?\n")
    print("Contestant 1. What is your name please?")
    while True:
        PLAYER[0] = (input("-> \n"))
        if len(PLAYER[0]) == 0:
            print("Don't be shy. I know I am intimidating but please")
            print("name yourself so the audience can recognize you.")

        elif len(PLAYER[0]) > 10:
            print("WOW, I will never remember such a long name.\n")
            print("Do you have a nickname I would rather use?")

        else:
            print(f"Welcome and good luck {PLAYER[0]} \n")
            break

    print("Contestant 2. What is your name please?")
    while True:
        PLAYER[1] = (input("-> \n"))
        if len(PLAYER[1]) == 0:
            print("Don't be shy. I know I am intimidating but please")
            print("name yourself so the audience can recognize you.")

        elif len(PLAYER[1]) > 10:
            print("WOW, I will never remember such a long name.\n")
            print("Do you have a nickname I would rather use?")

        else:
            print(f"Welcome and good luck {PLAYER[1]} \n")
            break

    print("I hope you will both have fun.\n")
    print("But before we start the game\n")
    print("would you like to consult the rules?\n")


def rules():
    """
    The function shows the game rules and ask whether the players
    have understood them and are ready to proceed.
    """

    while True:
        user_input = input("yes or no? -> \n")
        if user_input == "no":
            print("Excellent. I see that we have 2 experts today.")
            print("It is going to be reaaaaaally fun!!\n")
            print("Ladies and Gentlemen. Without further ado.\n")
            break

        elif (user_input != "no" and user_input != "yes"):
            print("Sorry, I did not understand your answer")
            print("Insert yes or no please")
            continue

        else:
            print("The rules are simple:\n")
            print("You have to discover a mystery sentence per round")
            print("by guessing a consonant or a vowel each turn.\n")
            print("For your firt guess you will need to:")
            print("- Turn the wheel to get a cash value")
            print("- And then guess a consonant.\n")
            print("- The cash value will be multiplied by the")
            print("  number of consonant found in the mystery")
            print("  sentence and will be added to your bank.\n")
            print("- After guessing a correct letter, you can:")
            print("  a - buy a Vowel for 250$")
            print("  b - turn the wheel and find a new consonant")
            print("  c - guess the mystery sentence\n")
            print("- You will pass your turn if:")
            print("  a - your letter is not in the mystery sentence")
            print("  b - you guess incorrecty the mystery sentence")
            print("  c - your letter has already been guessed")
            print("  c - you spin the wheel on 'Pass your turn'")
            print("  e - you spin the wheel on 'Bankrupt' in which case")
            print("  you also lose all your earnings. OUCH!!\n")
            print("The player who guessed correctly the mystery sentence")
            print("earns her/his money accumulated during the round")
            print("The loser loses the round money")
            print("Note that the winners will win 1000$ minimum even if")
            print("they have less at the end of the round")
            print("The winner is the player with the most money")
            print("at the end of the 10th round\n")
            print('Have you understood the rules? (type yes when ready)')
            player_input()
            break


def player_input():
    """
    Functions registers the player answer to continue playing or not
    """
    user_input = ''
    while True:
        user_input = input("-> \n")

        if user_input.lower() != 'yes':
            print("It's ok. We have all the time in the world")
            print("Enter yes when you are ready")
            continue

        else:
            print('Very well. Here we go!')
            break


def select_row():
    """
    The function selects randomly a row in the google
    worksheet called "title" and creates a quote
    said by Mr Boty and the sentence to guess in the turn.
    """
    global MYSTERY_SENTENCE, TURN
    TURN = int(ROUND) - 1
    row = random.choice(list(data))
    MYSTERY_SENTENCE = row[0].lower()
    print(f"Let's reveal the mystery sentence for round {ROUND}!!\n")
    print(f"{PLAYER[0]}, {PLAYER[1]}, the mystery sentence is")
    print(f"in the '{row[4]}' category,\n")
    print(f"and it contains {row[1]} words and {row[2]} letters.\n")
    print("Take it away!")
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
    turn_wheel()


def turn_wheel():
    """
    The function gets the cash value from the wheel list.
    """
    global CASH, TURN

    print(f'\n{player_turn()}, you have spun the wheel.')
    print("Aaaaanndd ... it ... lands.... on...\n")

    CASH = random.choice(WHEEL)

    if CASH == "Bankrupt":
        print("\n")
        print("OH NOOOOO! It FELL ON BANKRUPT.")
        print("You lose ALL your earnings and pass your turn!!!")
        print("That is really unlucky and painful. GOSH!!")
        PLAYER_BANK[TURN % 2] = 0
        TURN += 1
        turn_wheel()

    elif CASH == "Pass your turn":
        print("\n")
        print(f"PASS YOUR TURN!! Too bad {player_turn()}")
        print("It is now your opponent turn.")
        print("Sorry")
        TURN += 1
        turn_wheel()

    else:
        print(f"{CASH}$")
        player_guess()


def check_consonant():
    """
    The function checks if there are still some remaning 
    consonants to be found in the mystery sentence. If no 
    consonants remains to be found, the no_consonant function
    is called, otherwise, the function is passed.
    """
    with_vowel = ""
    for char in MYSTERY_SENTENCE:
        # ord(chr) returns the ascii value
        # CHECKING FOR UPPER CASE
        if ord(char) >= 65 and ord(char) <= 90:
            with_vowel += char

            # checking for lower case
        elif ord(char) >= 97 and ord(char) <= 122:
            with_vowel += char

    no_vowel = with_vowel.translate({ord(i): None for i in 'aeiou'})
    # found on
    # https://www.digitalocean.com/community/tutorials/python-remove-character-from-string

    mystery_list = list(no_vowel)
 
    if len(guessed_letters) == 0:
        pass

    elif all(elem in guessed_letters for elem in mystery_list):
        no_consonant()

    else:
        pass


def no_consonant():
    """
    The function is called when all consonants in the sentence are found.
    It gives only two choices to play since the user cannot spin the wheel 
    anymore. 
    """
    print(f"{player_turn()} NO MORE CONSONANT IN THE MYSTERY SENTENCE!")
    print("You can only")
    print("  a - buy a vowel for 250$ or")
    print("  b - guess the mystery sentence")
    while True:
        user_input = input("a or b? -> \n")
        if user_input == "a":
            buy_vowel()
            break

        elif user_input == "b":
            guess_sentence()
            break

        else:
            print("wrong answer. a or b?")


def player_guess():
    """
    This function check if the player guess is a consonant or not,
    if the guess has been guessed before and if the user guessed
    a single letter.
    """
    print(f"\n{player_turn()}, what consonant do you choose for {CASH}$?")
    global GUESS, TURN
    while True:
        GUESS = input("-> \n")

        if len(GUESS) != 1:
            print(f"Sorry {player_turn()} we need only one letter.")
            print("Please guess a single consonant.\n")
            continue

        elif GUESS not in CONSONANT:
            print(f"Sorry {GUESS.upper()} is not a consonant.")
            print("Please enter a consonant.\n")
            continue

        elif GUESS in guessed_letters:
            print(f"Sorry, {GUESS.upper()} has already been guessed.")
            print(f"You unfortunately lose you turn {player_turn()}.\n")
            TURN += 1
            turn_wheel()
            break

        else:
            print(f"Thank you {player_turn()}")
            print(f"Let's see if the letter '{GUESS.upper()}' ")
            print("is in the mystery sentence.\n")
            guessed_letters.append(GUESS)
            compare_print()
            break


def compare_print():
    """ The function compares the users guess with the mystery
    sentence and print the letters that are correct.
    The function then gives a choice to the player who can either
    guess the sentence, buy a vowel or turn the wheel again"""
    global HIDE_SENTENCE, TURN
    print("* "*20)
    print(f"{PLAYER[0]} = {ROUND_BANK[0]}$ --- {PLAYER[1]} = {ROUND_BANK[1]}$")

    hidden_list = list(HIDE_SENTENCE)
    indices = [
        i for i, letter in enumerate(MYSTERY_SENTENCE) if letter == GUESS
        ]
    for index in indices:
        hidden_list[index] = GUESS
        HIDE_SENTENCE = "".join(hidden_list)
    
    print(f"\n{HIDE_SENTENCE}\n")
    print("* "*20)

    letter_count = MYSTERY_SENTENCE.count(GUESS)

    if letter_count == 1:
        print("\nCongratulations")
        print(f"{GUESS.upper()} is found once in the mystery sentence.")

    elif letter_count == 0:
        print(f"\n{GUESS.upper()} is not in the mystery sentence.")
        print(f"{player_turn()}, you pass your turn.\n")
        TURN += 1
        turn_wheel()

    else:
        print("\nCongratulations")
        print(f"{GUESS.upper()} is found {letter_count} times")
        print("in the sentence!")

    price = int(letter_count)*CASH
    ROUND_BANK[TURN % 2] = int(price) + int(ROUND_BANK[TURN % 2])
    print(f"\nYou earned {price}$!!!")
    print(f"{player_turn()}, you now have")
    print(f"{ROUND_BANK[TURN % 2]}$ in the bank.\n")
    check_consonant()
    print(f"{player_turn()} you guessed a correct consonant.")
    print("what is your next move please?")
    print("  a - buy a vowel for 250$")
    print("  b - turn the wheel and guess another consonant")
    print("  c - guess the mystery sentence")

    while True:
        user_input = input("a, b or c? -> \n")
        if user_input == "a":
            buy_vowel()
            break

        elif user_input == "b":
            turn_wheel()
            break

        elif user_input == "c":
            guess_sentence()
            break

        else:
            print("wrong answer. a, b or c?")


def guess_sentence():
    """
    The function allows the player to guess directly
    the sentence for a chance to win the round.
    If the answer is wrong the second player can play.
    if the answer is correct the winning_guess function is called
    """
    global TURN
    print("\n")
    print(f"Very well {player_turn()}.")
    print("Be sure to insert all your letters in lowercase")
    print("For example -> i love jamaica")
    print("Good Luck")
    user_input = input("-> \n")

    if user_input == MYSTERY_SENTENCE:
        winning_round()

    else:
        print("\n")
        print(f"I am really sorry {player_turn()}")
        print("The answer is incorrect,")
        print("you pass your turn")
        TURN += 1
        check_consonant()
        turn_wheel()


def winning_round():
    """
    The function gives the money to the winning player,
    reset the round bank accounts,
    empty the guessed letters,
    goes 1 round up and calls the convert_letter function
    to start a new mystery sentence.
    """
    global ROUND, ROUND_BANK

    print(f"\nCONGRATULATIONS {player_turn()}!!!")
    print(f"The answer was indeed {MYSTERY_SENTENCE}!!!")

    if int(ROUND_BANK[TURN % 2]) > 1000:
        print(f"You have totalized {ROUND_BANK[TURN % 2]}$ during")
        print(" this round. Congratulations!!!\n")
        PLAYER_BANK[TURN % 2] = int(PLAYER_BANK[TURN % 2]) \
            + int(ROUND_BANK[TURN % 2])

    else:
        print("You have won a 1000$ in this round\n")
        PLAYER_BANK[TURN % 2] = int(PLAYER_BANK[TURN % 2]) + 1000

    print("Let's recapitulate the score:")
    print(f"{PLAYER[0]} you own {PLAYER_BANK[0]}$")
    print(f"{PLAYER[1]} you own {PLAYER_BANK[1]}$")

    if int(PLAYER_BANK[0]) == int(PLAYER_BANK[1]):
        print("Ladies and gentlemen, the game is tied.")
        print("Now that's what I call entertainment!")

    elif int(PLAYER_BANK[0]) > int(PLAYER_BANK[1]):
        print(f"{PLAYER[1]}, I count on you to fight back")

    else:
        print(f"{PLAYER[0]}, do not give up!!!")

    ROUND += 1
    print("\n")
    print(f"\nIt is now time to move onto Round {ROUND}!!!\n")
    print("Dear contestants your earnings for the round")
    print("are obviously reset to 0.\n")
    ROUND_BANK = [0, 0]
    guessed_letters.clear()
    convert_letter(select_row())


def buy_vowel():
    """
    The function removes 250$ from the player bank
    and checks if the input is a vowel.
    Then the function calls compare_print()
    to checks if the vowel is in the mystery sentence"""

    global GUESS, HIDE_SENTENCE, TURN

    if int(ROUND_BANK[TURN % 2]) < 250:
        print(f"I apologize {player_turn()} but you do not")
        print("have enough money to buy a vowel.")
        print("You have no other choice than guessing the sentence")
        guess_sentence()

    ROUND_BANK[TURN % 2] = int(ROUND_BANK[TURN % 2]) - 250
    print(f"\n{player_turn()}, you chose to buy a vowel.")
    print(f"You have now have {ROUND_BANK[TURN % 2]}$ in the bank.\n")
    print("What is you vowel?")

    while True:
        GUESS = input("-> \n")
        if len(GUESS) != 1:
            print(f"Sorry {player_turn()} we need a single letter.")
            print("Please insert a single vowel\n")
            continue

        elif GUESS not in VOWELS:
            print(f"Sorry {GUESS.upper()} is not a vowel.")
            print("Please enter a vowel\n")
            continue

        elif GUESS in guessed_letters:
            print(f"Sorry, {GUESS.upper()} has already been guessed.")
            print(f"You unfortunately lose you turn {player_turn()}.\n")
            TURN += 1
            check_consonant()
            turn_wheel()
            break

        else:
            print(f'Thank you {player_turn()}')
            print(f"Let's see if '{GUESS.upper()}'")
            print("is in the mystery sentence.\n")
            guessed_letters.append(GUESS)
            break

    hidden_list = list(HIDE_SENTENCE)
    indices = [
        i for i, letter in enumerate(MYSTERY_SENTENCE) if letter == GUESS
        ]
    for index in indices:
        hidden_list[index] = GUESS
        HIDE_SENTENCE = "".join(hidden_list)
    print(HIDE_SENTENCE)

    letter_count = MYSTERY_SENTENCE.count(GUESS)
    print("\nCongratulations")
    if letter_count == 1:
        print(f"{GUESS.upper()} is found once in the mystery sentence")

    elif letter_count == 0:
        print(f"{GUESS.upper()} is not in the mystery sentence.")
        print(f"{player_turn()}, you pass your turn\n")
        TURN += 1
        check_consonant()
        turn_wheel()

    else:
        print(f"{GUESS.upper()} is found {letter_count} times")
        print("in the sentence!\n")

    check_consonant()

    print(f"{player_turn()} you guessed a correct vowel.")
    print("what is your next move please?")
    print("  a - buy another vowel for 250$")
    print("  b - turn the wheel and find a new consonant")
    print("  c - guess the mystery sentence")
    while True:
        user_input = input("-> \n")
        if user_input == "a":
            buy_vowel()
            break

        elif user_input == "b":
            turn_wheel()
            break

        elif user_input == "c":
            guess_sentence()
            break

        else:
            print("wrong answer. a, b or c?")


def main():
    """
    The function that runs other functions
    """
    play_game()
    rules()
    convert_letter(select_row())


main()
