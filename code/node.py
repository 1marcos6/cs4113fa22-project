import socket
import time
import pokemon_ou_pb2
import pokemon_ou_pb2_grpc
import grpc
import random
import sys


class pokemonserver(pokemon_ou_pb2_grpc.PokemonOuServicer):
    def __init__(self, port):
        self.port = port
        self.board = {}
        self.trainer = {}
        self.moves = {}
        self.path = {}
        self.pokemon = {}
        self.pokemon['pikachu'] = {'type': 'electric', 'hp': 35, 'attack': 55, 'defense': 40, 'special_attack': 50, 'special_defense': 50, 'speed': 90}
        self.pokemon['bulbasaur'] = {'type': 'grass', 'hp': 45, 'attack': 49, 'defense': 49, 'special_attack': 65, 'special_defense': 65, 'speed': 45}
        self.pokemon['charmander'] = {'type': 'fire', 'hp': 39, 'attack': 52, 'defense': 43, 'special_attack': 60, 'special_defense': 50, 'speed': 65}
        self.pokemon['squirtle'] = {'type': 'water', 'hp': 44, 'attack': 48, 'defense': 65, 'special_attack': 50, 'special_defense': 64, 'speed': 43}
        self.pokemon['caterpie'] = {'type': 'bug', 'hp': 45, 'attack': 30, 'defense': 35, 'special_attack': 20, 'special_defense': 20, 'speed': 45}
        self.pokemon['weedle'] = {'type': 'bug', 'hp': 40, 'attack': 35, 'defense': 30, 'special_attack': 20, 'special_defense': 20, 'speed': 50}
        self.pokemon['pidgey'] = {'type': 'normal', 'hp': 40, 'attack': 45, 'defense': 40, 'special_attack': 35, 'special_defense': 35, 'speed': 56}
        self.pokemon['rattata'] = {'type': 'normal', 'hp': 30, 'attack': 56, 'defense': 35, 'special_attack': 25, 'special_defense': 35, 'speed': 72}



def trainer(n):
   .

def pokemon(n):
    .

def server(n):
    .