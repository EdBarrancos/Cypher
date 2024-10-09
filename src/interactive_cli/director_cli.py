import functools
from typing import Callable

import inquirer

from src.game.characters import Character
from src.interactive_cli.cli import Cli


class DirectorCli(Cli):

    def __init__(self, message_call: Callable[[str], None]):
        self.characters = []
        self.current_character = None
        self.message_call = message_call
        self.current_language = None

    def _is_char_configured(self):
        if not self.current_character:
            print("You want to play without a character?")
            return False
        return True

    def _confirm(self, message):
        answer = self.inquirer_prompt(
            [inquirer.Confirm('option', message=message)]
        )
        return answer['option']

    def _add_char(self):
        print("Let's start by creating you character!\n")

        questions = [
            inquirer.Text(name='name', message='What\'s your character\'s name?'),
            inquirer.Text(name='languages', message='What languages do it speak? (comma separated)'),
        ]

        answers = self.inquirer_prompt(questions)
        character = Character(answers['name'], answers['languages'].split(','))

        if self._confirm("Is this the character you want to create?"):
            self.characters.append(character)
        if self._confirm("Do you want to select this character"):
            self.current_character = character
            self._select_language()

    def _connect(self):
        self.message_call(f"DIRECTOR")
        print("Welcome to the game!\n")

    def _query_character(self):
        if not self.characters:
            print("Configure some character first!")
            return

        answer = self.inquirer_prompt(
            [inquirer.List('option', message="What character will you be?", choices=[(char.name, char) for char in self.characters], carousel=True)]
        )
        return answer['option']

    def _select_character(self):
        if not self.characters:
            print("Configure some character first!")
            return

        self.current_character = self._query_character()

    def _query_language(self, character: Character):
        answer = self.inquirer_prompt(
            [inquirer.List('option', message="What language will you speak?", choices=character.languages, carousel=True)]
        )
        return answer['option']

    def _select_language(self):
        if not self.current_character:
            return

        self.current_language = self._query_language(self.current_character)
        
    def _single_speak(self, message: str, character: Character = None, language: str = None):
        if not character:
            character = self._select_character()    
        if not language:
            language = self._select_language()

        self.message_call(f"{character.name}:{language}:{message}")

    def _menu(self):
        options = [
            ('Configure New Character', 'configure'),
            ('Select Character', 'character'),
            ('Select Language', 'language'),
            ('Speak', 'speak'),
            ('Speak Single', 'speak_single')
        ]

        answer = self.inquirer_prompt(
            [inquirer.List('option', message="Select Command", choices=options, carousel=True)]
        )

        match answer['option']:
            case 'configure':
                self._add_char()
                self._menu()
            case 'character':
                self._select_character()
                self._menu()
            case 'language':
                self._select_language()
                self._menu()
            case 'speak':
                return
            case 'speak_single':
                self._single_speak()
                self._menu()
            case _:
                print("I'm confused, you want to do what?\n")
                self._menu()

    def _speak(self, message):
        if not self.current_language:
            print("Can't speak without choosing which language you'll use now can you?\n")
            return
        self.message_call(f"{self.current_character.name}:{self.current_language}:{message}")

    @staticmethod
    def _print_help():
        print()
        print("\\menu                                               -> go to interactive menu")
        print("\\configure                                          -> configure new character")
        print("\\character                                          -> select character")
        print("\\language                                           -> select language")
        print("\\speak_single <character> <language> <message>      -> speak single line with character and language")
        print("\\exit                                               -> leave game")
        print("\\help                                               -> print this :)")

    def start_cli(self):

        self._connect()

        print("Configure your first character!")
        self._add_char()

        print("Well, go on... Start speaking!")
        print("\\help for help :D")

        while True:
            message = input('')
            command_check = message.split(' ')[0]
            if command_check[0] == "\\":
                match command_check:
                    case "\\menu":
                        self._menu()
                    case "\\configure":
                        self._add_char()
                    case "\\character":
                        self._select_character()
                    case "\\language":
                        self._select_language()
                    case "\\speak_single":
                        parts = message.split(' ')
                        self._single_speak("".join(parts[3:]), parts[1], parts[2])
                    case "\\help":
                        self._print_help()
                    case "\\exit":
                        return
                    case _:
                        print("What are you trying to do??")
                        self._print_help()
            else:
                self._speak(message)
