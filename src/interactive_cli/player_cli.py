import functools
from typing import Callable

import inquirer

from interactive_cli.cli import Cli


class PlayerCli(Cli):

    def __init__(self, message_call: Callable[[str], None]):
        self.name = None
        self.languages = []
        self.message_call = message_call
        self.current_language = None

    def _is_char_configured(self):
        if not self.name or not self.languages:
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
        self.name = answers['name']
        self.languages = answers['languages'].split(',')

        self._connect() if self._confirm() else self._configure_char()

    def _connect(self):
        self.message_call(f"{self.name}:{functools.reduce(lambda a, b: a + ',' + b, self.languages)}")
        print("Welcome to the game!\n")

    def _select_language(self):
        if not self._is_char_configured():
            return

        answer = self.inquirer_prompt(
            [inquirer.List('option', message="What language will you speak?", choices=self.languages, carousel=True)]
        )

        self.current_language = answer['option']

    def _menu(self):
        options = [
            ('Select Language', 'language'),
            ('Speak', 'speak')
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
        print("\\menu       -> go to interactive menu")
        print("\\language   -> select language")
        print("\\exit       -> leave game")
        print("\\help       -> print this :)")

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
                    case "\\help":
                        self._print_help()
                    case "\\exit":
                        return
                    case _:
                        print("What are you trying to do??")
                        self._print_help()
            else:
                self._speak(message)
