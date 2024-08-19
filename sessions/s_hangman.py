import py_stuff.send_wrapper as sw
import os
import py_stuff.session_binding as sb
import random
import time
import asyncio

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
       #check if game is already in progress by lookin at the session line in .bound_sessions

       # TODO implement file locking to prevent race conditions ?
       
       for line in open('.bound_sessions').readlines():
              if f"{message.author}:{message.channel}:{message.guild}:hangman:" in line:
                     line_index = open('.bound_sessions').readlines().index(line)
                     print(line.split(':'))
                     if len(line.split(':')) > 5:
                            #parse game data from line -> they are in the form: 
                            #"{message.author}:{message.channel}:{message.guild}:{session command}:{session command details}"
                            #where session command details are in the form: "{word_to_guess}:{incorrect_guesses}:{tried_letters}"
                            word = line.split(':')[4]
                            incorrect_guesses = int(line.split(':')[5])
                            tried_letters = line.split(':')[6].replace('\n','')
                            guess = message.content.strip().upper()[0]

                            await process_guess(message, word, incorrect_guesses, tried_letters, guess, line_index)
                     #init new game
                     else:
                            #select a random word from .hangman_vocab
                            word = random.choice(open('.hangman_vocab').readlines()).strip().upper()
                            incorrect_guesses = 0
                            tried_letters = '\n'
                            #paste them into the line
                            line = f"{message.author}:{message.channel}:{message.guild}:hangman:{word}:{incorrect_guesses}:{tried_letters}"
                            
                            #rewrite the line in .bound_sessions
                            with open('.bound_sessions', 'r') as f:
                                lines = f.readlines()
                            with open('.bound_sessions', 'w') as f:
                                for i in range(len(lines)):
                                    if i == line_index:
                                        f.write(line)
                                    else:
                                        f.write(lines[i])
                            #display a logo (in assets/ascii/hangman/hangman_logo.ascii)
                            logo = open('assets/ascii/hangman/hangman_logo.ascii').read()
                            await sw.wrapperSend(message,str(logo),'mono')
                            await sw.wrapperSend(message, f"Hey **{message.author}**. I've picked a word. Guess which one it is.")
                            await sw.wrapperSend(message, f"**MAKE SURE TO ALLOW THE BOT TO FULLY RESPOND AFTER EACH GUESS**")
                            await sw.wrapperSend(message, f"[Start guessing, one character at a time!]")
       return

async def process_guess(message, word, incorrect_guesses, tried_letters, guess,line_index):
       
       #debung print
       print(f"word: {word}, incorrect_guesses: {incorrect_guesses}, tried_letters: {tried_letters}, guess: {guess}")
       
       
       #check if 'guess' is already in 'tried_letters'
       if guess in tried_letters:
              await sw.wrapperSend(message, f"You already tried **'{guess}'**.")
       else:
              tried_letters = tried_letters + guess

              # did we just complete the word ?
              done = True
              for char in word:
                     if char not in tried_letters:
                            done = False
              
              if done:
                     u_win = open('assets/ascii/hangman/hangman_you_win.ascii').read()
                     await sw.wrapperSend(message, str(u_win), 'mono')
                     await sw.wrapperSend(message, f"You guessed the word **{word}**. You win!")
                     #unbind and return
                     await sb.unbind(message)
                     return
              #if not, did we at least guess a correct letter ?
              elif guess in word:
                     await print_game(message, word, incorrect_guesses, tried_letters)
                     await sw.wrapperSend(message, f"Correct! The word contains **'{guess}'**.")

              #if we did not guess correctly
              if guess not in word:
                     incorrect_guesses = int(incorrect_guesses) + 1

                     #did we just lose the game ?
                     if incorrect_guesses == 5:
                            u_lost = open('assets/ascii/hangman/hangman_you_lost.ascii').read()
                            await sw.wrapperSend(message, str(u_lost), 'mono')
                            await sw.wrapperSend(message, f"Sorry **{message.author}**. You lost. The word was **{word}**.")
                            #unbind and return
                            await sb.unbind(message)
                            return
                     await print_game(message, word, incorrect_guesses, tried_letters)
                     await sw.wrapperSend(message, f"Incorrect! The word does not contain **'{guess}'**.")

       #update the line in .bound_sessions for future round
       line = f"{message.author}:{message.channel}:{message.guild}:hangman:{word}:{incorrect_guesses}:{tried_letters}"
       with open('.bound_sessions', 'r') as f:
           lines = f.readlines()
       with open('.bound_sessions', 'w') as f:
           for i in range(len(lines)):
               if i == line_index:
                   f.write(line)
               else:
                   f.write(lines[i])
       await sw.wrapperSend(message,f"I am ready for your next guess.")


async def print_game(message, word, incorrect_guesses, tried_letters):

       # pretty but slow
       #sprite = open('assets/ascii/hangman/hangman_sprite_' + str(incorrect_guesses) + '.ascii').read()
       sprite = hangman_sprites[incorrect_guesses]
       await sw.wrapperSend(message, sprite, 'mono')
       hint = word
       for char in word:
              if char.upper() not in tried_letters.upper():
                     hint = hint.replace(char, '#')
       await sw.wrapperSend(message,hint)
       return