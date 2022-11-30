import socket
import time
import pokemon_ou_pb2
import pokemon_ou_pb2_grpc
import grpc
import random
import sys
import concurrent.futures
from Pokemon import Pokemon
from Trainer import Trainer
import threading

class space:  # Helper structure that represents a space on the board, occupied by at most one Trainer, and any number of Pokemon
    def __init__(self):
        self.pokemon = [] # Because Pokemon can occupy the same space, we need to keep track of all of them with a list
        self.trainer = None # There can only be one trainer per space, so no list is needed

class gameserver(pokemon_ou_pb2_grpc.gameserverServicer): # The server class, which implements the gRPC interface and calls
    def __init__(self):
        self.animals = ['🐕', '🐈', '🐁', '🐹', '🐰', '🐺', '🐸', '🐯', '🐨', '🐻', '🐷', '🐽', '🐮', '🐗', '🐵', '🐒', '🐴', '🐎', '🐫', '🐑', '🐘', '🐼', '🐍', '🐦', '🐤', '🐥', '🐣', '🐔', '🐧', '🐢', '🐛', '🐝', '🐜', '🐞', '🐌', '🐙', '🐠', '🐟', '🐳', '🐋', '🐬', '🐄', '🐏', '🐀', '🐃', '🐅', '🐇', '🐉', '🐐', '🐓', '🐕', '🐖', '🐁', '🐂', '🐲', '🐡', '🐡', '🐊', '🐪', '🐆', '🐈', '🐩', '🐾', '💐', '🌸', '🌷', '🍀', '🌹', '🌻', '🌺', '🌿', '🌾', '🍄', '🌵', '🌴', '🌲', '🌳', '🌰', '🌱', '🌼', '🌐', '🌞', '🌝', '🌚', '🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘', '🌙', '🌜', '🌛', '🌔', '🌍', '🌎', '🌏', '🌋', '🌌', ' ⛅️', '🐙', '🚢', '🐿'] # List of all possible Pokemon emojis
        self.people = ["😀","😃","😄","😁","😆","😅","😂","🤣","😊","😇","🙂","🙃","😉","😌","😍","🥰","😘","😗","😙","😚","😋","😛","😝","😜","🤪","🤨","🧐","🤓","😎","🤩","🥳","😏","😒","😞","😔","😟","😕","🙁","😣","😖","😫","😩","🥺","😢","😭","😤","😠","😡","🤬","🤯","😳","🥵","🥶","😱","😨","😰","😥","😓","🤗","🤔","🤭","🤫","🤥","😶","😐","😑","😬","🙄","😯","😦","😧","😮","😲","🥱","😴","🤤","😪","😵","🤐","🥴","🤢","🤮","🤧","😷","🤒","🤕","🤑","🤠","😈","👿","👹","👺","💀","👻","👽","👾","🤖","💩","😺","😸","😹","😻","😼","😽","🙀","😿","😾"] # List of all possible Trainer emojis
        self.pokecount = 0 # Number of Pokemon on the board
        self.peoplecount = 0 # Number of Trainers on the board
        self.board = [] * (n*n) # The board, represented as a one dimensional list of spaces
        self.boardLocks = [] * (n*n) # A list of locks, one for each space on the board
        self.gameover = 'no' # Whether or not the game is over
        self.pathRec = '' # A string that will contain the paths of all Trainers and Pokemon
        self.pokedexRec = '' # A string that will contain the pokedexes of all Trainers

        for i in range(n*n):
            self.board.append(space())
        for i in range(n*n):                                # Initializing the locks and the board
            self.boardLocks.append(threading.Lock())
            
    def Capture(self, request, context): # The Capture RPC, which is called by a Trainer to capture a Pokemon
        returned = [] # The list of Pokemon that will be returned to the Trainer as captured
        if(len(self.board[request.pos].pokemon)>0): # If there still is a Pokemon at the requested position
            self.boardLocks[request.pos].acquire() # Lock the space for changes
            for pokemon in self.board[request.pos].pokemon: # For each Pokemon at the requested position (as there can be more than one)
                    returned.append(pokemon) # Add the Pokemon to the list of captured Pokemon
                    self.board[request.pos].pokemon.remove(pokemon) # Remove the Pokemon from the space
                    self.pokecount-=1 # Decrement the number of Pokemon on the board
                    if(self.pokecount==0): # If there are no more Pokemon on the board
                        self.pokecount = -1 # Set the number of Pokemon to -1, so that the game will end
            self.boardLocks[request.pos].release() # Release the lock on the space
        return pokemon_ou_pb2.CapturedMessage(names = returned) # Return the list of captured Pokemon to the Trainer

    def Board(self, request, context):  # RPC that prints the board
        self.print()  # Calls helper function to print the board
        return pokemon_ou_pb2.Empty()

    def isGameOver(self, request, context): # RPC that checks if the game is over
        return pokemon_ou_pb2.Feedback(status = self.gameover) # Returns the status of the game (yes or no)
    
    def passInfo(self, request, context): # RPC that passes the paths and pokedexes of all Trainers and Pokemon to the server
        self.pathRec+= request.name + ' ' + str(request.path) + '\n' # Add the path of the node to the path string
        if(request.dex != []): # If the node has a pokedex
            self.pokedexRec+= request.name + ': ' + str(request.dex) + '\n' # Add the pokedex of the node to the pokedex string
        return pokemon_ou_pb2.Empty()


    def Connect(self, request, context): # RPC that connects a node to the server
        if(request.type == 'poke'): # If the node is a Pokemon
            self.pokecount += 1 # Increment Pokemon count
            name = self.animals[self.pokecount-1] # Get the emoji of the Pokemon
            x = random.randint(0,(n*n)-1) # Get a random position on the board
            self.boardLocks[x].acquire() # Lock the space for changes
            if(self.board[x].trainer == None and len(self.board[x].pokemon) == 0): # If the space is empty
                self.board[x].pokemon.append(name) # Add the Pokemon to the space
            else:   # If the space is not empty
                self.boardLocks[x].release() # Release the lock on the space
                while(self.board[x].trainer != None or len(self.board[x].pokemon) != 0): # While the space is not empty
                    x = random.randint(0,(n*n)-1) # Get a new random position on the board
                    self.boardLocks[x].acquire() # Lock the space for changes
                    if(self.board[x].trainer == None and len(self.board[x].pokemon) == 0): # If the space is empty
                        self.board[x].pokemon.append(name) # Add the Pokemon to the space
                        break # Break out of the loop
                    else: 
                        self.boardLocks[x].release() # Release the lock on the space if it is still not empty
            self.boardLocks[x].release() # Release the lock on the space
            return pokemon_ou_pb2.ConnectResponse(status = name, pos = x) # Return the name and position of the node to the node
        else: # If the node is a Trainer
            self.peoplecount += 1 # Increment Trainer count
            name = self.people[self.peoplecount-1]  # Get the emoji of the Trainer
            x = random.randint(0,(n*n)-1) # Get a random position on the board
            self.boardLocks[x].acquire() # Lock the space for changes
            if(self.board[x].trainer == None and len(self.board[x].pokemon) == 0): # If the space is empty
                self.board[x].trainer = name # Add the Trainer to the space
            else:  # If the space is not empty
                self.boardLocks[x].release() # Release the lock on the space
                while(self.board[x].trainer != None or len(self.board[x].pokemon) != 0): # While the space is not empty
                    x = random.randint(0,(n*n)-1)   # Get a new random position on the board
                    self.boardLocks[x].acquire() # Lock the space for changes
                    if(self.board[x].trainer == None and len(self.board[x].pokemon) == 0): # If the space is empty
                        self.board[x].trainer = name # Add the Trainer to the space
                        break # Break out of the loop
                    else:
                        self.boardLocks[x].release() # Release the lock on the space if it is still not empty
            self.boardLocks[x].release() # Release the lock on the space
            return pokemon_ou_pb2.ConnectResponse(status = name, pos = x) # Return the name and position of the node to the node


    def MoveRequest(self, request, context): # RPC that handles a move request from a node
        if(request.type == 'poke'): # If the node is a Pokemon
            if(request.name not in self.board[request.curr].pokemon): # If the Pokemon is not at the position it is supposed to be at
                return pokemon_ou_pb2.Feedback(status = "Captured") # then it has been captured, and can no longer move
            if(len(self.board[request.move].pokemon) == 0): # If the space the Pokemon wants to move to is empty
                self.boardLocks[request.move].acquire() # Lock the space for changes
                self.boardLocks[request.curr].acquire() # Lock the space the Pokemon is currently at for changes
                self.board[request.move].pokemon.append(request.name) # Add the Pokemon to the space it wants to move to
                self.board[request.curr].pokemon.remove(request.name) # Remove the Pokemon from the space it is currently at
                self.boardLocks[request.move].release() # Release the lock on the new space
                self.boardLocks[request.curr].release() # Release the lock on the previous space
                return pokemon_ou_pb2.Feedback(status = "yes") # Return positive feedback
            else:
                return pokemon_ou_pb2.Feedback(status = "no") # Return negative feedback if move is not possible 
        else: # If the node is a Trainer
            if(self.board[request.move].trainer == None):  # If the space the Trainer wants to move to is empty
                self.boardLocks[request.move].acquire()  # Lock the space for changes
                self.boardLocks[request.curr].acquire()  # Lock the space the Trainer is currently at for changes
                self.board[request.move].trainer = request.name # Add the Trainer to the space it wants to move to
                self.board[request.curr].trainer = None # Remove the Trainer from the space it is currently at
                self.boardLocks[request.move].release() # Release the lock on the new space
                self.boardLocks[request.curr].release() # Release the lock on the previous space
                if(self.board[request.move].pokemon != []): # If the space the Trainer moved to has a Pokemon
                    return pokemon_ou_pb2.Feedback(status = "poke") # Return "poke" indicating the move was successful and there is a Pokemon at the new space
                return pokemon_ou_pb2.Feedback(status = "yes") # Return positive feedback if the move was successful
            else:
                return pokemon_ou_pb2.Feedback(status = "no") # Return negative feedback if move is not possible


    def BoardCheck(self, request, context): # RPC that handles a board check request from a node
        possibleMoves =[] # List of possible moves (not preferred)
        starMoves =[] # List of preferred moves
        if(request.type == 'poke'): # If the node is a Pokemon then a preferred move is a move that is not to a trainer, and one where no other Pokemon is already occupying. A non-preferred move is a move that is not to a trainer, but where another Pokemon is already occupying
            x = request.location
            if(0<x-(n+1)<len(self.board) and len(self.board[x-(n+1)].pokemon) ==0 and self.board[x-(n+1)].trainer == None and x%n != 0):
                starMoves.append(x-(n+1))
            elif (0<x-(n+1)<len(self.board) and self.board[x-(n+1)].trainer == None and x%n != 0):
                possibleMoves.append(x-(n+1))
            if(0<x-(n)<len(self.board) and len(self.board[x-(n)].pokemon) ==0 and self.board[x-(n)].trainer == None):
                starMoves.append(x-(n))
            elif (0<x-(n)<len(self.board) and self.board[x-(n)].trainer == None):
                possibleMoves.append(x-(n))
            if(0<x-(n-1)<len(self.board) and len(self.board[x-(n-1)].pokemon) ==0 and self.board[x-(n-1)].trainer == None and (x+1)%n != 0):
                starMoves.append(x-(n-1))
            elif (0<x-(n-1)<len(self.board) and self.board[x-(n-1)].trainer == None and (x+1)%n != 0):
                possibleMoves.append(x-(n-1))
            if(0<x-1<len(self.board) and len(self.board[x-1].pokemon) ==0 and self.board[x-1].trainer == None and x%n != 0):
                starMoves.append(x-1)
            elif (0<x-1<len(self.board) and self.board[x-1].trainer == None and x%n != 0):
                possibleMoves.append(x-1)
            if(0<x+1<len(self.board) and len(self.board[x+1].pokemon) ==0 and self.board[x+1].trainer == None and (x+1)%n != 0):
                starMoves.append(x+1)
            elif (0<x+1<len(self.board) and self.board[x+1].trainer == None and (x+1)%n != 0):
                possibleMoves.append(x+1)
            if(0<x+(n-1)<len(self.board) and len(self.board[x+(n-1)].pokemon) ==0 and self.board[x+(n-1)].trainer == None and x%n != 0):
                starMoves.append(x+(n-1))
            elif (0<x+(n-1)<len(self.board) and self.board[x+(n-1)].trainer == None and x%n != 0):
                possibleMoves.append(x+(n-1))
            if(0<x+n<len(self.board) and len(self.board[x+(n)].pokemon) ==0 and self.board[x+(n)].trainer == None):
                starMoves.append(x+(n))
            elif (0<x+n<len(self.board) and self.board[x+(n)].trainer == None):
                possibleMoves.append(x+(n))
            if(0<x+(n+1)<len(self.board) and len(self.board[x+(n+1)].pokemon) ==0 and self.board[x+(n+1)].trainer == None and (x+1)%n != 0):
                starMoves.append(x+(n+1))
            elif (0<x+(n+1)<len(self.board) and self.board[x+(n+1)].trainer == None and (x+1)%n != 0):
                possibleMoves.append(x+(n+1))

        else: # If the node is a Trainer then a preferred move is a move that is to a Pokemon, and one where no other Trainer is already occupying. A non-preferred move is a move that is to a space not occupied by a Trainer, but where no Pokemon is present
            x = request.location
            if(0<x+1<len(self.board) and len(self.board[x+1].pokemon) >0 and self.board[x+1].trainer == None and (x+1)%n != 0):
                starMoves.append(x+1)
            elif (0<x+1<len(self.board) and self.board[x+1].trainer == None and (x+1)%n != 0):
                possibleMoves.append(x+1)
            if(0<x+n<len(self.board) and len(self.board[x+(n)].pokemon) >0 and self.board[x+(n)].trainer == None):
                starMoves.append(x+(n))
            elif (0<x+n<len(self.board) and self.board[x+(n)].trainer == None):
                possibleMoves.append(x+(n))
            if(0<x-(n)<len(self.board) and len(self.board[x-(n)].pokemon) > 0 and self.board[x-(n)].trainer == None):
                starMoves.append(x-(n))
            elif (0<x-(n)<len(self.board) and self.board[x-(n)].trainer == None):
                possibleMoves.append(x-(n))
            if(0<x+(n+1)<len(self.board) and len(self.board[x+(n+1)].pokemon) >0 and self.board[x+(n+1)].trainer == None and (x+1)%n != 0):
                starMoves.append(x+(n+1))
            elif (0<x+(n+1)<len(self.board) and self.board[x+(n+1)].trainer == None and (x+1)%n != 0):
                possibleMoves.append(x+(n+1))
            if(0<x-(n-1)<len(self.board) and len(self.board[x-(n-1)].pokemon) >00 and self.board[x-(n-1)].trainer == None and (x+1)%n != 0):
                starMoves.append(x-(n-1))
            elif (0<x-(n-1)<len(self.board) and self.board[x-(n-1)].trainer == None and (x+1)%n != 0):
                possibleMoves.append(x-(n-1))
            if(0<x-1<len(self.board) and len(self.board[x-1].pokemon) >0 and self.board[x-1].trainer == None and x%n != 0):
               starMoves.append(x-1)
            elif (0<x-1<len(self.board) and self.board[x-1].trainer == None and x%n != 0):
                possibleMoves.append(x-1)
            if(0<x+(n-1)<len(self.board) and len(self.board[x+(n-1)].pokemon) >0 and self.board[x+(n-1)].trainer == None and x%n != 0):
                starMoves.append(x+(n-1))
            elif (0<x+(n-1)<len(self.board) and self.board[x+(n-1)].trainer == None and x%n != 0):
                possibleMoves.append(x+(n-1))
            if(0<x-(n+1)<len(self.board) and len(self.board[x-(n+1)].pokemon) > 0 and self.board[x-(n+1)].trainer == None and x%n != 0):
                starMoves.append(x-(n+1))
            elif (0<x-(n+1)<len(self.board) and self.board[x-(n+1)].trainer == None and x%n != 0):
                possibleMoves.append(x-(n+1))
        return pokemon_ou_pb2.PossibleMoves(moves = possibleMoves, starmoves = starMoves) # Return the possible moves split by preferred and non-preferred

    def print(self): # Print the board
        output = ""

        for i in range(n*n):
            if((i+1)%n==0):
                if(self.board[i].trainer!=None): # Preference is given to printing the trainer over the pokemon
                    output += self.board[i].trainer
                elif(len(self.board[i].pokemon)>0): # If there is a pokemon, print it
                    output += self.board[i].pokemon[0] # If there are multiple pokemon, only print the first one
                else:
                    output += "⬜" # Empty space represented by a white square
                output += "\n" # New line to represent the end of a row (the board is a square but saved as a 1D array)
            else:
                if(self.board[i].trainer!=None):
                    output += self.board[i].trainer
                elif(len(self.board[i].pokemon)>0):
                    output += self.board[i].pokemon[0]
                else:
                    output += "⬜"

        output+='\n'
        print(output)
    


def server():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=20)) # Create a server with 10 threads
    servicer = gameserver() # Create a new instance of the gameserver class
    pokemon_ou_pb2_grpc.add_gameserverServicer_to_server(servicer, server) # Add the servicer to the server
    server.add_insecure_port('[::]:50051') # Add the port to the server
    server.start() # Start the server
    print('Server started') # Print that the server has started
    try:
        print('\n') # Print a new line
        print('\033[H\033[J') # Clear the terminal
        print('\033[H\033[J') # Clear the terminal again (sometimes one clear isn't enough)

        while True: # Loop for the server to run
            print('\033[H') # Move the cursor to the top of the terminal to overwrite the previous board
            servicer.print() # Print the board
            if(servicer.pokecount == -1): # If the pokecount is -1, the game is over because all the pokemon have been caught
                print('\033[H\033[J') # Clear the terminal again to remove the board
                servicer.gameover = 'yes' # Set the gameover variable to yes
                time.sleep(5) # Wait 5 seconds to allow all nodes to receive the gameover message (they check constantly and cannot receive it correctly if the server shuts down too quickly)
                f = open("/log/path.txt", "w") # Open a file to write the path to
                f.write(servicer.pathRec) # Write the path to the file
                f.close() # Close the file
                f = open("/log/pokedex.txt","w") # Open a file to write the pokedex to
                f.write(servicer.pokedexRec) # Write the pokedex to the file
                f.close() # Close the file
                print("Full game move history saved to ./path.txt") # Print that the path has been saved
                print("Full game pokedex saved to ./pokedex.txt") # Print that the pokedex has been saved
                print("GAME OVER") # Print that the game is over
                break # Break the loop and close the server
            
              
    except KeyboardInterrupt:
        server.stop(0)
        

if __name__== '__main__': 
    curr = socket.gethostname() # Get the current hostname
    if curr == "Server": # If the current hostname is Server, run the server method
        n = int(sys.argv[1]) # Get the size of the board from the command line
        server() # Run the server method
    elif curr[0:7] == "Trainer": # If the current hostname starts with Trainer, run the trainer method
        time.sleep(4) # Wait 4 seconds to allow the server to start
        train = Trainer() # Create a new instance of the Trainer class
    elif curr[0:7] == "Pokemon": # If the current hostname starts with Pokemon, run the pokemon method
        time.sleep(4) # Wait 4 seconds to allow the server to start
        poke = Pokemon() # Create a new instance of the Pokemon class
