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

title = SHEET.worksheet('title')
data = title.get_all_values()


def select_row():
    """
    The function selects randomly a row in the google 
    worksheet called "title" and creates a sentence 
    said by Mr Boty and the sentence to guess in the turn.
    """
    row = random.choice(list(data))
    sentence = row[0]
    print(f"In the '{row[4]}' category.\n")
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
    convert_letter(select_row())


main()

