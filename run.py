"""
The Wheel or fortune game.
"""
import sys
import time
from time import sleep
from os import system, name
import random
import termcolor
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

PLAYER = ["", ""]  # stores the 2 players name.
PLAYER_BANK = [0, 0]  # stores the money won by each player
ROUND_BANK = [0, 0]  # stores the money earned during the round
CASH = 0  # stores the value given randomly byt the wheel
ROUND = 1  # determines the round played
NUM_ROUND = 0  # stores the number of rounds chosen by players
TURN = 0  # goes up +1 each time a player passes its turn
guessed_letters = []  # stores all letters guessed during the round
GUESS = ""  # the player consonnant or vowel guess.
MYSTERY_SENTENCE = ""  # Stores the mystery sentence of each round
HIDE_SENTENCE = ""  # stores the mystery sentence with underscores.
VOWELS = ["a", "e", "i", "o", "u"]
CONSONANT = ["b", "c", "d", "f", "g", "h", "j", "k", "l",
             "m", "n", "p", "q", "r", "s", "t", "v", "w",
             "x", "y", "z"]

WHEEL = ["Bankrupt", 600, 400, 300, "Pass your turn",
         800, 350, 450, 700, 300, 600, "Bankrupt", 600, 500, 300, 500,
         800, 550, 400, 300, 900, 500, 300, 900]
# just like the actual game, the wheel has 24 values.

title = SHEET.worksheet('title')
data = title.get_all_values()
# gets the mystery sentences stored in a google sheet.


def print(script):
    """
    Used to add a typing effect when printing on the terminal
    """
    for letters in script + '\n':
        sys.stdout.write(letters)
        sys.stdout.flush()
        time.sleep(1./30)


def clear():
    """
    The function clears the screen.

    """
    # The function was copied from
    # https://www.geeksforgeeks.org/clear-screen-python/

    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def player_turn():
    """
    This function defines the player who will play
    the turn by populating the PLAYER global variable index
    with a 0 or a 1 thanks to the modulo.
    PLAYER[0]= player 1, PLAYER[1] = player 2
    """
    return PLAYER[TURN % 2]


def score_sentence_print():
    """
    Function clears the screen after 2 seconds and display the overall
    game score, the round score and the mystery sentence.
    """
    sleep(2)
    clear()
    termcolor.cprint("- "*25, "cyan", attrs=['bold'])
    termcolor.cprint(f"Game score  {PLAYER[0]} = {PLAYER_BANK[0]}$ --- "
                     f"{PLAYER[1]} = {PLAYER_BANK[1]}$", "cyan",
                     attrs=['bold'])
    termcolor.cprint(f"Round score {PLAYER[0]} = {ROUND_BANK[0]}$ --- "
                     f"{PLAYER[1]} = {ROUND_BANK[1]}$", "cyan", attrs=['bold'])
    termcolor.cprint("- "*25, "cyan", attrs=['bold'])
    termcolor.cprint("* "*25, "yellow", attrs=['bold'])
    termcolor.cprint(f"\n{HIDE_SENTENCE}\n", "yellow", attrs=['bold'])
    termcolor.cprint("* "*25, "yellow", attrs=['bold'])


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
        # obligation to insert at least 1\ character.
        if PLAYER[0].strip() == '':
            print("Don't be shy. I know I am intimidating but please")
            print("name yourself so the audience can recognize you.")

        elif len(PLAYER[0]) > 15:  # 15 characters max.
            print("WOW, I will never remember such a long name.\n")
            print("Do you have a nickname I would rather use?")

        else:  # Players can put any type of character they want.
            print(f"Welcome and good luck {PLAYER[0]} \n")
            break

    print("Contestant 2. What is your name please?")
    while True:
        PLAYER[1] = (input("-> \n"))  # Copies player 1 process
        if PLAYER[1].strip() == '':
            print("Don't be shy. I know I am intimidating but please")
            print("name yourself so the audience can recognize you.")

        elif len(PLAYER[1]) > 15:
            print("WOW, I will never remember such a long name.\n")
            print("Do you have a nickname I would rather use?")

        else:
            print(f"Welcome and good luck {PLAYER[1]}\n")

            break

    sleep(2)
    clear()
    num_round()


def num_round():
    """
    Function determines how many rounds should be played.
    """
    global NUM_ROUND
    print("How many rounds would you like play today?")
    while True:
        try:
            NUM_ROUND = int(input("between 2 and 10: "))
        except ValueError:
            print("Please enter a valid integer 2-10")
            continue
        if NUM_ROUND >= 2 and NUM_ROUND <= 10:
            print(f"\nExcellent. Today we will play {NUM_ROUND} Rounds.\n")
            break
        else:
            print('The integer must be in the range 2-10')

    print("But before we start the game,\n")
    print("would you like to consult the rules?\n")
    rules()


def rules():
    """
    The function shows the game rules and ask whether the players
    have understood them and are ready to proceed.
    """

    while True:
        user_input = input("yes or no? -> \n").lower()
        if user_input == "no":
            print("Fantastic. I see that we have 2 experts today.")
            print("It is going to be reaaaaaally fun!!\n")
            print("Ladies and Gentlemen. Without further ado.\n")
            print("LET'S PLAY THE WHEEL ... OF ...  FORTUUUUUNNE!\n")
            sleep(3)
            clear()
            break

        elif (user_input != "no" and user_input != "yes"):
            print("Sorry, I did not understand your answer")
            print("Insert yes or no please")
            continue

        else:
            clear()
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
            print("- The player who guessed correctly the mystery sentence")
            print("  earns her/his money accumulated during the round.")
            print("- The loser loses the round money.")
            print("- Note that the winners will win 1000$ minimum even if")
            print("  they have less at the end of the round.")
            print("- The last round money prize will be mulptiplied by 3.")
            print("- The winner is the player with the most money")
            print("  at the end of all rounds.\n")
            print('All good? Are you ready to continue? (type yes when ready)')
            player_input()
            break


def player_input():
    """
    Functions registers the player answer to continue playing or not
    """
    while True:
        user_input = input("-> \n").lower()

        if user_input.lower() != 'yes':
            print("It's ok. We have all the time in the world")
            print("Enter yes when you are ready")
            continue

        else:
            clear()
            if ROUND == 1:
                print("Ladies and Gentlemen... Without further ado.\n")
                print("LET'S PLAY THE WHEEL ... OF ...  FORTUUUUUNNE!\n")
            break


def select_row():
    """
    The function selects randomly a row in the google
    worksheet called "title" and creates the sentence
    to guess in the turn.
    """
    global MYSTERY_SENTENCE, TURN
    # Switches players who start the round. Player1 starts round 1
    TURN = int(ROUND) - 1
    row = random.choice(list(data))
    MYSTERY_SENTENCE = row[0].lower()

    # Each round starts here so the scenario switches if we play the last
    # round with the x3 gain multiplicator.
    if int(ROUND) == int(NUM_ROUND):
        print("Ladies and gentlemen, this is the final Round.")
        print("As you probably already know, this round winner")
        print("will see its earnings muliplied by 3.\n")

        if int(PLAYER_BANK[0]) > int(PLAYER_BANK[1]):
            print(f"{PLAYER[1]}, this is your chance.")
            print(f"{PLAYER[0]}, be cautious. Everything is possible\n")

        else:
            print(f"{PLAYER[0]}, this is your chance.")
            print(f"{PLAYER[1]}, be cautious. Everything is possible\n")
    else:
        print(f"Let's reveal the mystery sentence for Round {ROUND}!!\n")

    termcolor.cprint(f"The mystery sentence is in the '{row[4]}' category\n",
                     "yellow", attrs=['bold'])
    termcolor.cprint(f"and it contains {row[1]} words and {row[2]} letters.\n",
                     "yellow", attrs=['bold'])

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

    termcolor.cprint("* "*25, "yellow", attrs=['bold'])
    termcolor.cprint(f"\n{HIDE_SENTENCE}\n", "yellow", attrs=['bold'])
    termcolor.cprint("* "*25, "yellow", attrs=['bold'])

    print("\nGOOD LUCK!")
    turn_wheel()


def turn_wheel():
    """
    The function gets a random value from the wheel list and stores
    it in the CASH global variabe.
    """
    global CASH, TURN

    print(f'\n{player_turn()}, you have spun the wheel.')
    print("Aaaaanndd ... it ... lands.... on...\n")

    CASH = random.choice(WHEEL)

    if CASH == "Bankrupt":
        # the modulo defines the index of the ROUND_BANK variable and therefore
        # defines the player earnings
        if ROUND_BANK[TURN % 2] == 0:
            termcolor.cprint("It fell on Bankrupt.", "red", attrs=['bold'])
            print(f"Well, it is not really a loss {player_turn()}.")
            print("You did not have any money in the bank.")
            print("Nevertheless you lose your turn.")

        elif ROUND_BANK[TURN % 2] < 2000:
            termcolor.cprint("It fell on Bankrupt.", "red", attrs=['bold'])
            print(f"You lose {ROUND_BANK[TURN % 2]}$ {player_turn()}.")
            print("It's tough but I believe in you.")
            print("It's your oppopent's turn now.")

        elif ROUND_BANK[TURN % 2] < 4000:
            termcolor.cprint("OH NOOOOO! it is Bankrupt...", "red",
                             attrs=['bold'])
            print(f"{ROUND_BANK[TURN % 2]}$.... gone.")
            print("I feel for you, really I do. It is not the end yet but...")
            print("your oppopent has the hand now.")

        else:
            termcolor.cprint("NOOOOOOO, BANKRUPT!!!!", "red", attrs=['bold'])
            print("OOOOOH lordy lord... I am speechless.")
            print(f"You had {ROUND_BANK[TURN % 2]}$ {player_turn()}")
            print(f"{ROUND_BANK[TURN % 2]}$ !!!!!!!!!!!!")
            print("That is really unlucky ... reaaaally unlucky")
            print("Do not forget that you pass your turn too.")

        ROUND_BANK[TURN % 2] = 0  # The player loses the round earnings.
        TURN += 1
        turn_wheel()

    elif CASH == "Pass your turn":
        termcolor.cprint(f"\nPASS YOUR TURN!! Too bad {player_turn()}.", "red",
                         attrs=['bold'])
        print("It is now your opponent turn.")
        print("Sorry")
        TURN += 1
        turn_wheel()

    else:
        termcolor.cprint(f"{CASH}$", "blue", attrs=['bold'])
        player_guess()


def check_consonant():
    """
    The function checks if there are still some remaining
    consonants to be found in the mystery sentence. If all
    consonants were already found, the no_consonant function
    is called, otherwise the games continues with the function
    player_guess.
    """
    with_vowel = ""
    for char in MYSTERY_SENTENCE:
        if ord(char) >= 65 and ord(char) <= 90:
            with_vowel += char

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
    termcolor.cprint("\nNO MORE CONSONANT IN THE MYSTERY SENTENCE!", "magenta",
                     attrs=['bold'])

    if int(ROUND_BANK[TURN % 2]) < 250:
        termcolor.cprint(f"\n{player_turn()} you do not have enough money in\
                         the bank", "red", attrs=['bold'])
        termcolor.cprint("to buy a vowel.", "red", attrs=['bold'])
        print("You have no other choice than guessing the sentence.")
        guess_sentence()

    print(f"{player_turn()} You can only:")
    print("  a - buy a vowel for 250$ or")
    print("  b - guess the mystery sentence")
    while True:
        user_input = input("a or b? -> \n").lower()
        if user_input == "a":
            buy_vowel()
            break

        elif user_input == "b":
            guess_sentence()
            break

        else:
            termcolor.cprint("wrong answer. a or b?", "magenta",
                             attrs=['bold'])


def player_guess():
    """
    This function check if the player guess is a consonant or not,
    if the guess has been guessed before and if the user guessed
    a single letter.
    """
    print(f"\n{player_turn()}, what consonant do you choose for {CASH}$?")
    global GUESS, TURN
    while True:
        GUESS = input("-> \n").lower()

        if len(GUESS) != 1:  # 1 letter only
            termcolor.cprint(f"Sorry, {player_turn()} we need only one "
                             "letter.", "magenta", attrs=['bold'])
            print("Please guess a single consonant.\n")
            continue

        elif GUESS not in CONSONANT:
            termcolor.cprint(f"Sorry, {GUESS.upper()} is not a "
                             "consonant.", "magenta", attrs=['bold'])
            print("Please enter a consonant.\n")
            continue

        elif GUESS in guessed_letters:
            termcolor.cprint(f"Sorry, {GUESS.upper()} has already been "
                             "guessed.", "red", attrs=['bold'])
            print(f"You unfortunately lose you turn {player_turn()}.\n")
            TURN += 1
            score_sentence_print()
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

    hidden_list = list(HIDE_SENTENCE)
    indices = [
        i for i, letter in enumerate(MYSTERY_SENTENCE) if letter == GUESS
        ]
    for index in indices:
        hidden_list[index] = GUESS
        HIDE_SENTENCE = "".join(hidden_list)

    score_sentence_print()

    # gives the number of letter on the mystery sentence
    letter_count = MYSTERY_SENTENCE.count(GUESS)

    if letter_count == 1:
        termcolor.cprint("\nGood", "green", attrs=['bold'])
        print(f"{GUESS.upper()} is found once in the mystery sentence.")

    elif letter_count == 0:
        termcolor.cprint(f"\n{GUESS.upper()} is not in the mystery sentence.",
                         "red", attrs=['bold'])
        print(f"{player_turn()}, you pass your turn.\n")
        TURN += 1
        score_sentence_print()
        turn_wheel()

    else:
        termcolor.cprint("\nCongratulations", "green", attrs=['bold'])
        print(f"{GUESS.upper()} is found {letter_count} times")
        print("in the sentence!")

    # calculates the number of letter found x the wheel value
    price = int(letter_count)*CASH
    # updates the player earnings
    ROUND_BANK[TURN % 2] = int(price) + int(ROUND_BANK[TURN % 2])

    termcolor.cprint(f"\n{player_turn()}, you earn {price}$!!!\n", "blue",
                     attrs=['bold'])

    check_consonant()

    print(f"\n{player_turn()} you guessed a correct consonant.")
    print("what is your next move please?")
    print("  a - buy a vowel for 250$")
    print("  b - turn the wheel and guess another consonant")
    print("  c - guess the mystery sentence")

    while True:
        user_input = input("a, b or c? -> \n").lower()
        if user_input == "a":
            score_sentence_print()
            buy_vowel()
            break

        elif user_input == "b":
            score_sentence_print()
            turn_wheel()
            break

        elif user_input == "c":
            score_sentence_print()
            guess_sentence()
            break

        else:
            termcolor.cprint("wrong answer. a, b or c?", "magenta",
                             attrs=['bold'])


def guess_sentence():
    """
    The function allows the player to guess directly
    the sentence for a chance to win the round.
    If the answer is wrong the second player takes the trun.
    If the answer is correct the winning_guess function is called
    """
    global TURN
    print(f"\nVery well {player_turn()}.")
    print("What do you think the sentence is?")
    user_input = input("-> \n").lower()

    if user_input == MYSTERY_SENTENCE:
        winning_round()

    else:
        termcolor.cprint(f"\nI am really sorry {player_turn()}", "red",
                         attrs=['bold'])
        termcolor.cprint("The answer is incorrect,", "red", attrs=['bold'])
        termcolor.cprint("you pass your turn", "red", attrs=['bold'])
        TURN += 1
        check_consonant()
        score_sentence_print()
        turn_wheel()


def winning_round():
    """
    The function gives the money to the winning player,
    reset the player earnings to 0,
    empties the guessed letters variable,
    goes 1 round up and calls the convert_letter function
    to start a new mystery sentence.
    """
    global ROUND, ROUND_BANK
    clear()
    termcolor.cprint(f"\nCONGRATULATIONS {player_turn()}!!!", "green",
                     attrs=['bold'])
    print("The answer was indeed")
    termcolor.cprint(f"{MYSTERY_SENTENCE.upper()}!!!", "green", attrs=['bold'])

    if int(ROUND_BANK[TURN % 2]) > 1000:
        print(f"You have totalized {ROUND_BANK[TURN % 2]}$ in")
        print("this round.\n")

        if int(ROUND) == int(NUM_ROUND):
            print("And since this was the last one")
            print("it is multiplied by 3!\n")
            print(f"You earned {int(ROUND_BANK[TURN % 2]) * 3}$!")
            PLAYER_BANK[TURN % 2] = int(PLAYER_BANK[TURN % 2])\
                + int(ROUND_BANK[TURN % 2])*3

        else:
            PLAYER_BANK[TURN % 2] = int(PLAYER_BANK[TURN % 2])\
                + int(ROUND_BANK[TURN % 2])

    else:
        print("You have won 1000$ in this round\n")

        if int(ROUND) == int(NUM_ROUND):
            print("And since this was the last one")
            print("it is multiplied by 3!\n")
            print("You earned 3000$!")
            PLAYER_BANK[TURN % 2] = int(PLAYER_BANK[TURN % 2]) + 3000

        else:
            PLAYER_BANK[TURN % 2] = int(PLAYER_BANK[TURN % 2]) + 1000

    print("This money is now yours and it cannot be taken away.\n")
    print("You deserve it!\n")

    if int(ROUND) == int(NUM_ROUND):  # If this is the last round
        game_over()

    print("Let's recapitulate the gains:")
    termcolor.cprint(f"{PLAYER[0]} you own {PLAYER_BANK[0]}$", "blue",
                     attrs=['bold'])
    termcolor.cprint(f"{PLAYER[1]} you own {PLAYER_BANK[1]}$", "blue",
                     attrs=['bold'])

    if int(PLAYER_BANK[0]) == int(PLAYER_BANK[1]):
        print("Ladies and gentlemen, the game is tied.")
        print("What a duel!")
        print("Now that's what I call entertainment!")

    elif int(PLAYER_BANK[0]) > int(PLAYER_BANK[1]):
        print(f"Don't worry {PLAYER[1]}, I am sure the")
        print("next round will be yours.\n")

    else:
        print(f"{PLAYER[0]}, do not give up!!!")
        print("The next round has your name written all over it!\n")

    ROUND += 1
    print("Dear contestants, are you ready to play the next round?!\n")
    player_input()
    print(f"It is now time to move onto Round {ROUND}!!!\n")
    print("Dear contestants your earnings for the round")
    print("are obviously reset to 0.\n")

    ROUND_BANK = [0, 0]  # players earnings reset
    guessed_letters.clear()  # guessels letters reset
    convert_letter(select_row())  # starts the new round


def buy_vowel():
    """
    The function removes 250$ from the player bank
    and checks if the input is a vowel.
    Then the function calls compare_print()
    to checks if the vowel is in the mystery sentence"""

    global GUESS, HIDE_SENTENCE, TURN

    ROUND_BANK[TURN % 2] = int(ROUND_BANK[TURN % 2]) - 250

    print(f"\n{player_turn()}, you chose to buy a vowel.")
    termcolor.cprint(f"You have now have {ROUND_BANK[TURN % 2]}$.\n" "blue",
                     attrs=['bold'])
    print("What is your vowel?")

    while True:
        GUESS = input("-> \n").lower()
        if len(GUESS) != 1:
            termcolor.cprint(f"Sorry {player_turn()} we need a single "
                             "letter.", "magenta", attrs=['bold'])
            print("Please insert a single vowel\n")
            continue

        elif GUESS not in VOWELS:
            termcolor.cprint(f"Sorry {GUESS.upper()} is not a "
                             "vowel.", "magenta", attrs=['bold'])
            print("Please enter a vowel\n")
            continue

        elif GUESS in guessed_letters:
            termcolor.cprint(f"Sorry, {GUESS.upper()} has already been "
                             "guessed.", "red", attrs=['bold'])
            print(f"You unfortunately lose you turn {player_turn()}.\n")
            TURN += 1
            check_consonant()
            score_sentence_print()
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

    score_sentence_print()

    letter_count = MYSTERY_SENTENCE.count(GUESS)
    if letter_count == 1:
        print("\nNot bad!")
        print(f"{GUESS.upper()} is found once in the mystery sentence")

    elif letter_count == 0:
        print(f"\n{GUESS.upper()} is not in the mystery sentence.")
        termcolor.cprint(f"{player_turn()}, you pass your turn\n", "magenta",
                         attrs=['bold'])
        TURN += 1
        check_consonant()
        turn_wheel()

    else:
        print("\nNice.")
        print(f"{GUESS.upper()} is found {letter_count} times")
        print("in the sentence!\n")

    check_consonant()

    if int(ROUND_BANK[TURN % 2]) < 250:
        print(f"I apologize {player_turn()} but you do not")
        print("have enough money to buy a vowel.")
        print("  a - turn the wheel and find a new consonant")
        print("  b - guess the mystery sentence")
        while True:
            user_input = input("-> \n").lower()
            if user_input == "a":
                turn_wheel()
                break

            elif user_input == "b":
                guess_sentence()
                break

            else:
                termcolor.cprint("wrong answer. a or b?", "magenta",
                                 attrs=['bold'])

    print(f"{player_turn()} you guessed a correct vowel.")
    print("what is your next move please?")
    print("  a - buy another vowel for 250$")
    print("  b - turn the wheel and find a new consonant")
    print("  c - guess the mystery sentence")
    while True:
        user_input = input("-> \n").lower()
        if user_input == "a":
            score_sentence_print()
            buy_vowel()
            break

        elif user_input == "b":
            score_sentence_print()
            turn_wheel()
            break

        elif user_input == "c":
            score_sentence_print()
            guess_sentence()
            break

        else:
            termcolor.cprint("wrong answer. a, b or c?", "magenta",
                             attrs=['bold'])


def game_over():
    """
    The function will close the game. It will tell who
    the winner is and will conclude the game like a
    host would do.
    """
    print("LADIES AND GENTLEMEN THIS IS IT!!!!")
    print(f"We went through {num_round()} rounds")
    print(" and after ups and downs the winner is...")
    if int(PLAYER_BANK[0]) > int(PLAYER_BANK[1]):  # If player1 wins
        termcolor.cprint(f"{PLAYER[0]} with {PLAYER_BANK[0]}$", "green",
                         attrs=['bold'])
        print("What a victory!")
        print(f"Let's not forget {PLAYER[1]}. You were sensational too.")

    else:  # If player2 wins
        termcolor.cprint(f"{PLAYER[1]} with {PLAYER_BANK[1]}$", "green",
                         attrs=['bold'])
        print("What a victory!")
        print(f"Let's not forget {PLAYER[0]}. You were sensational too.")

    print("\nThe competition was fierce and you both have been")
    print("amazing contestants.")
    print("Thank you sooo very much!\n ")
    print("But alas! All good things must end,")
    print("and it is now time to say good bye.\n")
    print("BUT FEAR NOT! We will be back soon.")
    print("After all we are just one click away.\n")
    print("Ladies and gentlemen!")
    print("My name is Mr Boty and I will welcome you next time")
    print("to once more turn the WHEEL")
    sleep(2)
    print("OF")
    sleep(2)
    print("FORTUUUUUNE!!!!")

    exit()  # end of the game.


def main():
    """
    The function that runs other functions
    """
    play_game()
    convert_letter(select_row())


main()
