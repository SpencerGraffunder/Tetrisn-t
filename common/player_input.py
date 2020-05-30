import pygame
from enum import Enum


class EventType(Enum):
    KEY_UP = 0
    KEY_DOWN = 1
    SPECIAL = 2


class ControlType(Enum):
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    CCW = 3
    CW = 4
    PAUSE = 5
    QUIT = 6


class Event:
    def __init__(self, event_type, control_type):
        self.type = event_type
        self.control = control_type


class PlayerInput:
    def __init__(self, player_number):
        self.events = []
        self.new_game = False
        self.starting_level = 0
        self.player_count = 1
        self.pause = False
        self.resume = False
        self.player_number = player_number

    def __nonzero__(self):
        return self.__bool__()

    def __bool__(self):
        return bool(self.events) or self.new_game or self.pause or self.resume

    def add_event(self, event):
        self.events.append(event)

    def start_game(self):
        self.new_game = True

    def set_starting_level(self, starting_level):
        self.starting_level = starting_level

    def set_player_count(self, player_count):
        self.player_count = player_count

    def pause_game(self):
        self.pause = True

    def resume_game(self):
        self.resume = True
