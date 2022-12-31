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

GUESSED_LETTERS = []
TURN = "1"
VOWELS = ["a", "e", "i", "o", "u"]
PLAYER1 = ""
PLAYER2 = ""
PLAYER1CASH = 0
PLAYER2CASH = 0
WHEEL = ["Bankrupt", 600, 400, 300, "Pass your turn",
         800, 350, 450, 700, 300, 600, 5000, 600, 500, 300, 500,
         800, 550, 400, 300, 900, 500, 300, 900]

title = SHEET.worksheet('title')
data = title.get_all_values()


def play_game():
    """
    The Funtion starts the game and registers the 2 players names.
    """
    print("Hello and welcome to the Wheel ... of ...  Fortuuuuuune!")
    print("\n")
    print("My Name is Mr Boty and I will be your host!")
    print("\n")  
    print("Lets introduce our 2 contestants. ")
    print("\n")   
    PLAYER1 = str(input("Contestant number 1. What is you name please? "))
    print("Welcome and good luck " + str(PLAYER1))
    print("\n")

    PLAYER2 = str(input("Contestant number 2. How should we call you? "))
    print("Thank you and good luck to you too " + str(PLAYER2))
    print("\n")
    print("And now that that we know our contestants!")
    print("\n")
    print("Let's have a look at the rules!")
    print("\n")


def rules():
    """
    The function shows the game rules and ask whether the players 
    have understood them and are ready to proceed.
    """
    while True:       
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

        user_input = ''

        while True:
            user_input = input('Have you understood? (type yes when ready)')

            if user_input.lower() != 'yes':                
                print("It's ok. Take your time. Read thoroughly.")
                print("Enter yes when you are ready")  
                break
            
            else:
                print('Very well. IT IS NOW TIME TO PLAY!!')
            return user_input.lower()


def select_row():
    """
    The function selects randomly a row in the google 
    worksheet called "title" and creates a quote 
    said by Mr Boty and the sentence to guess in the turn.
    """    
    row = random.choice(list(data))
    sentence = row[0]
    print("Dear contestants,")
    print(f"in the '{row[4]}' category.\n")
    print(f"The guess contains {row[1]} words and {row[2]} letters.\n")
    print("Take it away!")
    print(sentence)
    return sentence


def convert_letter(sentence):
    """
    The function turns each letter of the sentence 
    created in the function in an underscore and therefore
    creates the guess users will try to solve.
    The function is inspired by Hayley Guillou on stack overflow 
    https://stackoverflow.com/questions/32960141/how-can-i-replace-the-letters-of-a-string-with-underscores
    """
    guess = sentence
    for i in range(0, len(sentence)):
        if ord(sentence[i]) != 32:
            guess = guess.replace(sentence[i], '_ ')
    print(guess)


def main():    
    play_game()
    rules()    
    convert_letter(select_row())
    

main()
