﻿"""
MIT License
Copyright (c) 2021 Peter Sovietov
Forked from https://github.com/true-grue/DandyBot
"""

import time
import json
from pathlib import Path
from random import shuffle
import tkinter as tk
from typing import Callable, List, Tuple, Any
import types
import sync as sc
from main import SCRIPT_STUB
from core.plitk import load_tileset, PliTk


DELAY = 50

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
TAKE = "take"
PASS = "pass"
PLAYER = "player"
GOLD = "gold"
WALL = "wall"
EMPTY = "empty"


class Board:
    def __init__(self, game, canvas, label, fetchedPlayers, onResize, script):
        self.game = game
        self.canvas = canvas
        self.label = label
        self.tileset = load_tileset(game["tileset"])
        self.screen = PliTk(canvas, 0, 0, 0, 0, self.tileset, 1)

        self.fetchedPlayers = fetchedPlayers
        self.onResize = onResize
        self.masterScript = script

        self.load_players()
        self.level_index = 0
        self.load_level()

    def load_players(self):
        self.players = []
        for i, fplayer in enumerate(self.fetchedPlayers):
            script = self.initModule(self.masterScript if i == 0 else SCRIPT_STUB)

            tile = self.game["tiles"]["@"][0 if i == 0 else 1]
            self.players.append(Player(fplayer[1], script, self, tile, fplayer[0]))

        sc.tracePlayers(self.onPlayersTrace)
        shuffle(self.players)

    @staticmethod
    def initModule(code) -> str:
        module = types.ModuleType('masterScript')
        exec(code, module.__dict__)
        # noinspection PyUnresolvedReferences
        return module.script

    def getPlayer(S, _id: int) -> Any | None:
        for i in S.players:
            if i.id == _id:
                return i
        return None

    #                                           id   lvl   x    y   gold
    def onPlayersTrace(S, positions: List[Tuple[int, int, int, int, int]]):
        for p in positions:
            player = S.getPlayer(p[0])
            S.remove_player(player)

            if p[1] == S.level_index:
                player.gold = p[4]
                S.add_player(player, p[2], p[3])

    def load_level(self):
        self.gold = 0
        self.steps = 0
        self.level = self.game["levels"][self.level_index]
        data = self.game["maps"][self.level["map"]]
        cols, rows = len(data[0]), len(data)
        self.map = [[data[y][x] for y in range(rows)] for x in range(cols)]
        self.has_player = [[None for y in range(rows)] for x in range(cols)]

        width = cols * self.tileset["tile_width"]
        height = rows * self.tileset["tile_height"]

        self.canvas.config(width=width, height=height)
        self.level["gold"] = sum(sum(int(cell)
            if cell.isdigit() else 0 for cell in row) for row in data)
        self.screen.resize(cols, rows)
        for y in range(rows):
            for x in range(cols):
                self.update(x, y)
        for p in self.players:
            self.add_player(p, *self.level["start"])
        self.update_score()

        self.label.update()
        self.onResize(width + self.label.winfo_reqwidth(), height)

    def get(self, x, y):
        if x < 0 or y < 0 or x >= self.screen.cols or y >= self.screen.rows:
            return "#"
        return self.map[x][y]

    def update(self, x, y):
        if self.has_player[x][y]:
            self.screen.set_tile(x, y, self.has_player[x][y].tile)
        else:
            self.screen.set_tile(x, y, self.game["tiles"][self.map[x][y]])

    def remove_player(self, player):
        self.has_player[player.x][player.y] = None
        self.update(player.x, player.y)

    def add_player(self, player, x, y):
        player.x, player.y = x, y
        self.has_player[x][y] = player
        self.update(x, y)

    def take_gold(self, x, y):
        self.gold += self.check("gold", x, y)
        self.map[x][y] = " "
        self.update(x, y)
        self.update_score()

    def check(self, cmd, *args):
        if cmd == "level":
            return self.level_index + 1
        x, y = args
        item = self.get(x, y)
        if cmd == "wall":
            return item == "#"
        if cmd == "gold":
            return int(item) if item.isdigit() else 0
        if cmd == "player":
            return item != "#" and self.has_player[x][y]

    def play(self):
        for p in self.players:
            p.act(p.script(self.check, p.x, p.y))
            if self.gold >= self.level["gold"]:
                return self.select_next_level()
        self.steps += 1
        return self.steps < self.level["steps"]

    def update_score(self):
        lines = [("Level:%4d\n" % (self.level_index + 1))]
        players = sorted(self.players, key=lambda x: x.gold, reverse=True)
        for p in players:
            lines.append("%s:%4d" % (p.name, p.gold))
        self.label["text"] = "\n".join(lines)

    def select_next_level(self):
        self.level_index += 1
        if self.level_index < len(self.game["levels"]):
            self.load_level()
            return True
        return False


class Player:
    def __init__(self, name, script, board, tile, id):
        self.name = name
        self.script = script
        self.board = board
        self.tile = tile
        self.x, self.y = 0, 0
        self.gold = 0
        self.id = id

    def act(self, cmd):
        dx, dy = 0, 0
        if cmd == UP:
            dy -= 1
        elif cmd == DOWN:
            dy += 1
        elif cmd == LEFT:
            dx -= 1
        elif cmd == RIGHT:
            dx += 1
        elif cmd == TAKE:
            self.take()
        self.move(dx, dy)

    def move(self, dx, dy):
        x, y = self.x + dx, self.y + dy
        board = self.board
        board.remove_player(self)
        if not board.check("wall", x, y) and not board.check("player", x, y):
            self.x, self.y = x, y
        board.add_player(self, self.x, self.y)

    def take(self):
        gold = self.board.check("gold", self.x, self.y)
        if gold:
            self.gold += gold
            self.board.take_gold(self.x, self.y)


def start_game(root, players, onResize: Callable, script):
    def update():
        t = time.time()
        if board.play():
            dt = int((time.time() - t) * 1000)
            root.after(max(DELAY - dt, 0), update)
        else:
            label["text"] += "\n\nGAME OVER!"

    root.configure(background="black")
    canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    canvas.pack(side=tk.LEFT)
    label = tk.Label(root, font=("TkFixedFont",),
                     justify=tk.RIGHT, fg="white", bg="gray20")
    label.pack(side=tk.RIGHT, anchor="n")
    filename = "core/game.json"
    game = json.loads(Path(filename).read_text())

    board = Board(game, canvas, label, players, onResize, script)

    root.after(0, update)