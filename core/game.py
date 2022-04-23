"""
MIT License
Copyright (c) 2021 Peter Sovietov
Forked from https://github.com/true-grue/DandyBot
"""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from random import shuffle
import tkinter as tk
from typing import Callable, List, Tuple, Any
import types

from overrides import overrides

import sync as sc
from main import SCRIPT_STUB
from core.plitk import load_tileset, PliTk
from tkinter import Tk
from tkinter import messagebox as msg


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

_KEYS = ('w', 'a', 's', 'd', '<space>')


class _IBoard(ABC):
    @abstractmethod
    def getMasterPlayer(S) -> Any: pass


_iboard: _IBoard


class Board(_IBoard):

    def __init__(self, game, canvas, label, fetchedPlayers, onResize, script, root):
        global _iboard
        _iboard = self

        self.game = game
        self.canvas = canvas
        self.label = label
        self.tileset = load_tileset(game["tileset"])
        self.screen = PliTk(canvas, 0, 0, 0, 0, self.tileset, 1)

        self.fetchedPlayers = fetchedPlayers
        self.onResize = onResize
        self.masterScript = script
        self.root = root

        self.load_players()
        self.level_index = 0
        self.load_level()

    @overrides
    def getMasterPlayer(S) -> Any:
        return S.getPlayer(sc.pid)

    def load_players(self):
        self.players = []
        for i, fplayer in enumerate(self.fetchedPlayers):
            script = self.initModule(self.masterScript if i == 0 else SCRIPT_STUB)

            tile = self.game["tiles"]["@"][0 if i == 0 else 1]
            self.players.append(Player(fplayer[1], script, self, tile, fplayer[0]))
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

    def take_gold(self, x, y, isMaster: bool):
        if isMaster: self.gold += self.check("gold", x, y)
        self.map[x][y] = " "
        self.update(x, y)
        self.update_score()
        if isMaster: sc.updateBoard((x, y))

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

    '''def checkForConnectedPlayers(S) -> List[Tuple[int, str]]:
        fetchedOnes = sc.checkForPlayers()
        if len(fetchedOnes) <= len(S.players): return fetchedOnes

        for new in fetchedOnes:
            isAlreadyAdded = False

            for old in S.players:
                if new[0] == old.id:
                    isAlreadyAdded = True
                    break

            if not isAlreadyAdded:
                print(sc.name, 'adds', new[1])
                script = S.initModule(SCRIPT_STUB)
                tile = S.game["tiles"]["@"][1]
                S.players.append(Player(new[1], script, S, tile, new[0]))
        return fetchedOnes'''

    '''def checkForDisconnectedPlayers(S, fetchedOnes: List[Tuple[int, str]]):
        if len(fetchedOnes) + 1 >= len(S.players): return
        for old in S.players:
            if old.id == sc.pid: continue
            isNotPresent = True

            for new in fetchedOnes:
                if new[0] == old.id:
                    isNotPresent = False
                    break

            if isNotPresent:
                print(sc.name, 'rems', old.name, list(map(lambda a: a.name, fetchedOnes)))
                S.remove_player(old)
                S.players.remove(old)'''

    #                                               id   lvl   x    y   gold
    def updateOtherPlayers(S, positions: List[Tuple[int, int, int, int, int]]):
        # if len(positions) != len(S.players):
        #     S.root.withdraw()
        #     msg.showerror('Players changed, restart required', parent=S.root)

        '''fs = S.checkForConnectedPlayers()
        S.checkForDisconnectedPlayers(fs)'''

        for p in positions:
            player = S.getPlayer(p[0])
            S.remove_player(player)

            if p[2] == S.level_index:
                player.gold = p[5]
                S.add_player(player, p[3], p[4])

    #                                            pid   x    y
    def updateCurrentBoard(S, takens: List[Tuple[int, int, int]]):
        for i in takens:
            S.take_gold(i[1], i[2], False)

    def play(self):
        master = self.getPlayer(sc.pid)
        master.act(master.script(self.check, master.x, master.y))

        if self.gold >= self.level["gold"]:
            sc.level += 1
            return self.select_next_level()

        sc.updatePlayer(self.level_index, master.x, master.y, master.gold)

        if (traced := sc.tracePlayers()) is not None:
            self.updateOtherPlayers(traced)

        if (takens := sc.traceBoard()) is not None:
            self.updateCurrentBoard(takens)

        self.steps += 1

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
    def __init__(self, name, script, board, tile, _id):
        self.name = name
        self.script = script
        self.board = board
        self.tile = tile
        self.x, self.y = 0, 0
        self.gold = 0
        self.id = _id

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
            self.board.take_gold(self.x, self.y, True)


def start_game(frame, players, onResize: Callable, script, root):
    def update():
        board.play()
        frame.after(DELAY, update)

    frame.configure(background="black")
    canvas = tk.Canvas(frame, bg="black", highlightthickness=0)
    canvas.pack(side=tk.LEFT)
    label = tk.Label(frame, font=("TkFixedFont",),
                     justify=tk.RIGHT, fg="white", bg="gray20")
    label.pack(side=tk.RIGHT, anchor="n")
    filename = "core/game.json"
    game = json.loads(Path(filename).read_text())

    board = Board(game, canvas, label, players, onResize, script, root)
    frame.after(0, update)


class _BoardStub(_IBoard):
    @overrides
    def getMasterPlayer(S) -> Any: raise Exception()


_iboard = _BoardStub()


def bindKeys(root: Tk):
    root.bind(_KEYS[0], lambda event: _onKeyPressed(UP))    # w
    root.bind(_KEYS[1], lambda event: _onKeyPressed(LEFT))  # a
    root.bind(_KEYS[2], lambda event: _onKeyPressed(DOWN))  # s
    root.bind(_KEYS[3], lambda event: _onKeyPressed(RIGHT)) # d
    root.bind(_KEYS[4], lambda event: _onKeyPressed(TAKE))  # <space>


def _onKeyPressed(key: str):
    if not isinstance(_iboard, Board): return
    _iboard.getMasterPlayer().act(key)
