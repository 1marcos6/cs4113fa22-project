## TODO
* Pokemon and Trainers are circularly moving around the map (on a 10x10 board, node can move from 1d idx 9 to 1d idx 10) This shouldn't be possible and is only possible now because of the use of the 1d array format to store the 2d board. [FIXED]

* Print all move records on game end.

* Add star moves to Pokemon move selection; a starmove is a move to a square with no pokemon on it. A move to a square with pokemon is valid but undesirable. [ADDED]

## Development Schedule

I plan to use my weekends from now until the due date, 12/01, to complete this project. Specifically Saturdays and Sundays.

* Saturday 11/02 and Sunday 11/03: 4-5 hours combined 

This upcoming weekend, I intend to build out the general design of my distributed system. I will create my Dockerfile, my docker-compose file, and the protos.

* Saturday 11/09 and Sunday 11/10: 4-5 hours combined

This weekend, I will work on my general game design including the loop of the game, rules, and the general structure of the game "board". I'll also begin to work on the communicative aspects of the node.py file. (gRPC)

* Saturday 11/16 and Sunday 11/17: 4-5 hours combined

Hopefully by this weekend I'll be able to get a working version of the game running. I will refine the game logic and ensure that connectivity with all nodes is working as expected, as well as making sure that my initial design constraints made in the past couple of weekends were reasonable.

* Saturday 11/23 and Sunday 11/24: 2 hours

This weekend is optimally reserved for refinement and optimization of my project. I hope that I will have my project running correctly by this point but I will reserve this time in case I need to make any last minute changes.

* Saturday 11/30 and Sunday 12/01: 2 hours

Again, this time can be used for last minute changes and I will also begin to work on my presentation for the project. The submission is due on Sunday.

* Saturday 12/07 and Sunday 12/08: 2 hours

I will finish my presentation during this time and compose a script and general structure for how I will give it in class.

## Emoji Chooser

I preliminarily plan to use the following scheme for assigning emojis to trainers and pokemon:
For Pokemon, I will keep track of how many Pokemon have been previously introduced into the game, and I will use two arrays containing the CLDR shortcodes of every emoji mentioned in the project spec (https://emojipedia.org/nature/ and https://emojipedia.org/people/) in combination with the Python emoji module. I will use the count of how many pokemon have been introduced as an index for the next available shortcode to be used with the module's emoji.emojize() command. As for initializing the amount of trainers and pokemon, I intend to use the --scale argument that can be given when composing a docker file. For example, if I had a trainer service name and wanted to build 5 trainers, I would type docker-compose up --scale trainer=5. As for the NxN size of the board, I am aware that I am able to specify cmd line arguments in the Dockerfile and could easily manually type N in the file, but I am currently looking into a more convenient soltuion to this and the scaling situation.

## Interface

So far I only have created the functions that have been required of me in the project description.

### Server
Captured() will take an empty message and return feedback that indicates to a Pokemon that it has been captured.
Moves() will take an empty message and return a list of all moves that have been executed
Board() will take an empty message and return a graphical representation of the board

### Trainer

Capture() will take an empty message and return a message that indicates to the trainer that it has captured a Pokemon
Move() will take a message that contains the direction of the move and return a message that indicates to the trainer that it has moved
Path() will take an empty message and return a list of all moves that have been executed
Pokedex() will take an empty message and return a list of all Pokemon that have been captured
CheckBoard() will take an empty message and return a list of all possible moves

### Pokemon
CheckBoard() will take an empty message and return a list of all possible moves
Move() will take a message that contains the direction of the move and return a message that indicates to the Pokemon that it has moved
Path() will take an empty message and return a list of all moves that have been executed
Trainer() will take an empty message and return a message that explains the information about past capture and about the trainer holding it


## First Version

### Compile
![Gif](./media/COmpile.gif)

The program is compiled by passing the amount of trainers and pokemon as arguments to the docker compose command. The program is then compiled and the trainers and pokemon are initialized and given emojis in the next gif.

### Board Initialization

![Gif](./media/New.gif)

The program is now compiled and nodes begin to request connection and are assigned a name and a spot on the board if successful. Due to temporary timing delays the complete board assignment takes about 10-15 seconds but when the project is complete I will remove these delays. To avoid board conflicts, I use locks to ensure that an assignment can take place without another assignment at the same spot occuring at the same time.
