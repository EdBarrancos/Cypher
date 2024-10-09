import inquirer
from inquirer.themes import BlueComposure


class Cli:

    @staticmethod
    def inquirer_prompt(questions):
        return inquirer.prompt(questions, theme=BlueComposure())
