import py_stuff.send_wrapper as sw
import os
import py_stuff.session_binding as sb
import random


hangman_sprites = [
       str(
        "   t----\n"
        "   |   |\n"
        "       |\n"
        "       |\n"
        "       |\n"
        "       |\n"
        "--------\n"
       ),
       str(
        "   t----\n"
        "   |   |\n"
        "   0   |\n"
        "       |\n"
        "       |\n"
        "       |\n"
        "--------\n"
       ),
       str(
        "   t----\n"
        "   |   |\n"
        "   0   |\n"
        "  /|   |\n"
        "       |\n"
        "       |\n"
        "--------\n"
       ),
       str(
        "   t----\n"
        "   |   |\n"
        "   0   |\n"
        "  /|\  |\n"
        "       |\n"
        "       |\n"
        "--------\n"
       ),
       str(
        "   t----\n"
        "   |   |\n"
        "   0   |\n"
        "  /|\  |\n"
        "  /    |\n"
        "       |\n"
        "--------\n"
       ),
       str(
        "   t----\n"
        "   |   |\n"
        "   0   |\n"
        "  /|\  |\n"
        "  / \  |\n"
        "       |\n"
        "--------\n"
       ),
]

async def run(message):

  # TODO 