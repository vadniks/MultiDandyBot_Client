"""
MIT License
Copyright (c) 2021 Peter Sovietov
https://github.com/true-grue/DandyBot
"""

import random


def script(check, x, y):
    if check("gold", x, y):
        return "take"
    return random.choice(["pass", "left", "right", "up", "down"])
