import functools
from typing import Callable

import inquirer

from interactive_cli.cli import Cli


class PlayerCli(Cli):

    def __init__(self, message_call: Callable[[str], None], prompt: bool = False):
        self.name = None
        self.languages = []
        self.message_call = message_call
        self.current_language = None
        self.prompt_mode = prompt
        self.connected = False

    def _is_char_configured(self):
        if not self.name or not self.languages:
            print("You want to play without a character? What are you, the director?")
            return False
        return True

    def _configure_char(self):
        if self.connected:
            print("Don't try to cheat. No changing your character mid-game!")
            return

        questions = [
            inquirer.Text(name='name', message='What\'s your name?'),
            inquirer.Text(name='languages', message='What languages do you speak, {name}? (comma separated)'),
        ]

        answers = self.inquirer_prompt(questions)
        self.name = answers['name']
        self.languages = answers['languages'].split(',')

    def _connect(self):
        if not self._is_char_configured():
            return
        if self.connected:
            print("I know this is kinda like magic, but once connected, no need to connect again!")
            return

        self.message_call(f"{self.name}:{functools.reduce(lambda a, b: a + ',' + b, self.languages)}")
        self.connected = True
        print("Welcome to the game!")

    def _select_language(self):
        if not self._is_char_configured():
            return

        answer = self.inquirer_prompt(
            [inquirer.List('option', message="What language will you speak?", choices=self.languages, carousel=True)]
        )

        self.current_language = answer['option']

    def _menu(self):
        options = [
            ('Configure Character', 'configure'),
            ('Select Language', 'language'),
            ('Attempt Server Connection', 'connect'),
            ('Speak', 'speak')
        ]

        answer = self.inquirer_prompt(
            [inquirer.List('option', message="Select Command", choices=options, carousel=True)]
        )

        match answer['option']:
            case 'configure':
                self._configure_char()
                self._menu()
            case 'language':
                self._select_language()
                self._menu()
            case 'speak':
                return
            case 'connect':
                self._connect()
                self._menu()
            case _:
                print("I'm confused, you want to do what?")
                self._menu()

    def _speak(self, message):
        if not self.current_language:
            print("Can't speak without choosing which language you'll use now can you? ")
            return
        if not self.connected:
            self._connect()
        self.message_call(f"{self.current_language}:{message}")

    def start_cli(self):

        if self.prompt_mode:
            self._menu()

        print("Well, go on... Start speaking!")

        while True:
            message = input('')
            command_check = message.split(' ')[0]
            if command_check[0] == "\\":
                match command_check:
                    case "\\connect":
                        self._connect()
                    case "\\menu":
                        self._menu()
                    case "\\config":
                        self._configure_char()
                    case "\\language":
                        self._select_language()
                    case "\\exit":
                        return
                    case _:
                        print("What are you trying to do??")
            else:
                self._speak(message)
