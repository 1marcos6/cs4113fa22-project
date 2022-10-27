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
For Pokemon, I will keep track of how many Pokemon have been previously introduced into the game, and I will use an array containing the CLDR shortcodes of every emoji mentioned in the project spec (https://emojipedia.org/nature/) in combination with the Python emoji module. I will use the count of how many pokemon have been introduced as an index for the next available shortcode to be used with the module's emoji.emojize() command. 