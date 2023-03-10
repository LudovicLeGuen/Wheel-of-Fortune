# Wheel-Of-Fortune
![Abyss diving club on devices](assets/readme-files/wheel-of-fortune.PNG)

[Click here to access live project](https://the-wheel-of-fortune.herokuapp.com/)
## Table of contents
1. [Introduction](#Introduction)
2. [UX](#UX)
    1. [Ideal User Demographic](#Ideal-User-Demographic)
    2. [User Stories](#User-Stories)
    3. [Development Planes](#Development-Planes)
    4. [Design](#Design)
3. [Features](#Features)
    1. [Design Features](#Design-Features) 
    2. [Existing Features](#Existing-Features)
    3. [Features to Implement in the future](#Features-to-Implement-in-the-future)
4. [Issues and Bugs](#Issues-and-Bugs)
5. [Technologies Used](#Technologies-Used)
     1. [Main Languages Used](#Main-Languages-Used)
     3. [Frameworks, Libraries & Programs Used](#Frameworks,-Libraries-&-Programs-Used)
6. [Testing](#Testing)
     1. [Testing.md](TESTING.md)
7. [Deployment](#Deployment)
     1. [Deploying on GitHub Pages](#Deploying-on-GitHub-Pages)
8. [Credits](#Credits)
     1. [Media](#Media)
     2. [Code](#Code)
9. [Acknowledgements](#Acknowledgements)
***

## Introduction
The wheel of Fortune game is the 3rd Portfolio Project of Code institute.  The developper has chosen this theme because it is a game that everybody knows or at least has heard of and because the rules are pretty universaly understood.

The requirement of this project is simple:
* "build a command-line application that allows the user to manage a common dataset about a particular domain".

[Back to top ⇧](#Wheel-Of-Fortune)

## UX
### Ideal User Demographic
There are two types of ideal users:
* Frequent user
* New user

### User-Stories
#### Frequent User Goals
* As a frequent user, I want a game that resembles the original wheel of fortune game play.
* As a frequent user, I want a challenging game.
* As a frequent user, I want to have new experiences and discover new things when playing.

#### New User Goals
* As a new user, I want the commands to be clear.
* As a new user, I want to understand the rules.
* As a new user, I want a fun experience.

[Back to top ⇧](#Wheel-Of-Fortune)

### Development-Planes
To build a command-line application that answer all aforementionned needs.

#### Strategy
The game will focus on the following target audience
* Audience
    * New Users
    * Experienced players
    
* Demographic
    * All ages
    
* Psycho Characteristics
    * Curious
    * Determined
    * Puzzle solver
    * competitor

All Users must be able to:
* Play the wheel of fortune
* Insert a player name
* Read the rules
* Choose the number of round
* Restart a game at will
* Know who is winning
* Play each round with a random sentence to guess 
* Choose whether they want to guess a consonant, a vowel or the sentence itself
* See the results of their guesses
* And, certainly the most iconic move of the original, being able to turn the wheel of fortune itself
    
The Administrator has to receive these information:
    * The name of the players
    * The number of rounds to be played
    
#### Scope

Now that we have established the goals of the game we can deduce the necessary features:
* Required functionality
    * Name input
    * Number of round imput
    * A random sentence creator
    * A score board
    * A function to choose between consonant and vowels
    * A function to guess the sentence
    * Turning the wheel
    * Calculating the rewards
    * Printing the players guesses

#### Scope
A flowchart was created in [LUCID](https://lucid.app.com/ "Link to Lucid") to illustrate the logic of the game.

<details>
<summary>Pre game flowchart</summary>
    
![Pre Game](assets/readme-files/pre-game.png)

</details> 

<details>
<summary>Game flowchart</summary>

![Pre Game](assets/readme-files/game.png)

</details> 
    

[Back to top ⇧](#Wheel-Of-Fortune)

### Design
The design of a command line application is by nature pretty basic, but the developper has decided to highlight the sentence during the game since it is the mot important factor for the player.
The sentence is therefore "wrapped" between two lines made of the * characters and spaces.

Moreover, the devlopper has decided to insert a printing effect to add a feeling of continuity to the game. This effect gives the player the sensation to be in a narrated game.

The developper has also decided to add a Game Host in the person of Mr Boty to even more emulate the TV game. 
[Back to top ⇧](#Wheel-Of-Fortune)

## Features
### Existing Features
- **Player names input** - 
- **Number of round imput** - 
- **Score board** - 
- **Choose between consonant and vowels** - 
- **Guessing the sentence** - 
- **Turning the wheel** - 
- **Calculating the rewards** - 
- **Printing the players guesses** - 

[Back to top ⇧](#Wheel-Of-Fortune)

### Features to Implement in the future
* More players
     Only 2 players can play now but the real show has 3. a feature to ask how many people can play would be fun.
* Special price and special wheel value
     Special prize such as trips or cars at certain rounds just like in the real game. 

[Back to top ⇧](#Wheel-Of-Fortune)

## Issues and Bugs 
Several issues were encountered during developpement but the most troublesome are listed below.

**Bankrupt would reset the player overall gains instead of the player round earnings** The issues was easily fixed. The developper had used the wrong variable. Instead of coding ROUND_BANK[TURN % 2] = 0, the developer made a mistake and wrote PLAYER_BANK[TURN % 2] = 0

**The number of round question** popped several times thus asking how many rounds the players wanted. The developper made a mistake and instead of using the variable name in several literal string, he used the function itself.

### Unfixed Bugs 
The screen is supposed to be cleared each time the function clear() is called. The function is working. But the issue is that only the last 24 lines are removed.
For example. The rules are pretty long: they are 38 lines long. 
When clear() is called at the end of it, only the last 24 lines are cleared and the first 14 lines stay all game long. 

[Back to top ⇧](#Wheel-Of-Fortune)

## Technologies Used
### Main Languages Used
* Python3
### Frameworks, Libraries & Programs Used
- [Heroku](https://heroku.com/ "Link to Heroku") was used to deploy the game.
- [GitPod](https://gitpod.io/ "Link to GitPod homepage") was used for writing, commiting, and pushing code.
- [GitHub](https://github.com/ "Link to GitHub")
- [Am I Responsive?](http://ami.responsivedesign.is/# "Link to Am I Responsive Homepage") was used to verify responsiveness and to create the top picture of this README.md

[Back to top ⇧](#Wheel-Of-Fortune)

## Testing
Refer to this [page](TESTING.md) please

## Deployment
The site was developped on Gitpod, commiting and pushing to github.

### Deploying on Heroku
Deploying on Heroky required the following:

* Type "pip freeze > requirements.txt" in your Github terminal to update the requirements.txt file with the list of dependencies used in the project . Save, commit and push.

* Create an Heroku account, select Python as the 'Primary development language'.

* Open the email sent to your address and click the link to verify your email address. Follow the instructions to create a password and log in.

* Click the 'create new app' button on the dashboard. Name your app, select your region and click 'Create App'

* In the "Settings" tab, add both the python and node.js build packs.

* Create a "Config VAR" named 'CREDS' KEY and copy/paste the creds.json file in it.

* Create another "Config VAR" called PORT as the KEY with 8000 as VALUE.

* In the "Deploy" tab, choose GitHub as a deployment method.

* Search for the wanted repository.

* Click on "enable automatic deploys" and then deploy branch.

* once the app built (a minute or two needed)click "View" to access the site.
   
[Back to top ⇧](#Wheel-Of-Fortune)

## Credits 
### Code 
The developer has consulted countless times Stack Overflow and W3Schools in ordeer to build the game.
The code inspired by other developpers is commented directly in the code.

[Back to top ⇧](#Wheel-Of-Fortune)

## Acknowledgements
I would like to thank:
* My wife  for her patience and her kind words when I was in doubt.
* my mentor, Seun, for her counseling and her contagious enthusiasm and love for coding.
* my fellow coding students of Code institue who have been invaluable on Slack.

[Back to top ⇧](#Wheel-Of-Fortune)

***