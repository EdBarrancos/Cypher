import functools
from typing import Callable

import inquirer

from src.game.characters import Character
from src.interactive_cli.cli import Cli


class PlayerCli(Cli):

    def __init__(self, message_call: Callable[[str], None]):
        self.character = None
        self.message_call = message_call
        self.current_language = None

    def _is_char_configured(self):
        if not self.character:
            print("You want to play without a character? What are you, the director?")
            return False
        return True

    def _confirm(self):
        answer = self.inquirer_prompt(
            [inquirer.Confirm('option', message="Are you sure of who you are?")]
        )
        return answer['option']

    def _configure_char(self):
        print("Let's start by creating you character!\n")

        questions = [
            inquirer.Text(name='name', message='What\'s your name?'),
            inquirer.Text(name='languages', message='What languages do you speak, {name}? (comma separated)'),
        ]

        answers = self.inquirer_prompt(questions)
        self.character = Character(answers['name'], answers['languages'].split(','))

        self._connect() if self._confirm() else self._configure_char()

    def _connect(self):
        self.message_call(f"{self.character.name}:{functools.reduce(lambda a, b: a + ',' + b, self.character.languages)}")
        print("Welcome to the game!\n")

    def _single_speak(self, message: str, language: str = None):
        if not self.character:
            print("You need to configure your character first!")
            return
        
        if not language:
            language = self._query_language()

        self.message_call(f"{language}:{message}")

    def _query_language(self):
        answer = self.inquirer_prompt(
            [inquirer.List('option', message="What language will you speak?", choices=self.character.languages, carousel=True)]
        )
        return answer['option']

    def _select_language(self):
        if not self._is_char_configured():
            return

        self.current_language = self._query_language()

    def _menu(self):
        options = [
            ('Select Language', 'language'),
            ('Speak', 'speak'),
            ('Speak Single', 'speak_single')
        ]

        answer = self.inquirer_prompt(
            [inquirer.List('option', message="Select Command", choices=options, carousel=True)]
        )

        match answer['option']:
            case 'language':
                self._select_language()
                self._menu()
            case 'speak':
                return
            case 'speak_single':
                self._single_speak(input("Enter your message: "))
                self._menu()
            case _:
                print("I'm confused, you want to do what?\n")
                self._menu()

    def _speak(self, message):
        if not self.current_language:
            print("Can't speak without choosing which language you'll use now can you?\n")
            return
        self.message_call(f"{self.current_language}:{message}")

    @staticmethod
    def _print_help():
        print()
        print("\\menu                         -> go to interactive menu")
        print("\\language                     -> select language")
        print("\\speak_single <language> <message> -> speak single line with specified language")
        print("\\exit                         -> leave game")
        print("\\help                         -> print this :)")

    def start_cli(self):

        self._configure_char()

        print("Well, go on... Start speaking!")
        print("\\help for help :D")

        while True:
            message = input('')
            command_check = message.split(' ')[0]
            if command_check[0] == "\\":
                match command_check:
                    case "\\menu":
                        self._menu()
                    case "\\language":
                        self._select_language()
                    case "\\speak_single":
                        parts = message.split(' ')
                        self._single_speak(" ".join(parts[2:]), parts[1])
                    case "\\help":
                        self._print_help()
                    case "\\exit":
                        return
                    case _:
                        print("What are you trying to do??")
                        self._print_help()
            else:
                self._speak(message)
