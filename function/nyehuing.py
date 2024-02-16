from random import randint

from tool.config import names


def make_nyehuing(length: int):
    name = ""

    for _ in range(length):
        name += names[randint(0, 2349)]

    return name
