#!/usr/bin/env python3

from argparse import ArgumentParser, ArgumentError
from dotenv import load_dotenv
import openai
import os
import sys
from tarot import TarotDeck

APP_NAME = "Tarobot"
API_KEY_ENV_VAR = "OPENAI_API_KEY"


class MissingEnvVar(Exception):
    """This exception is raised when a required environment variable has not been defined."""
    pass


class App:
    """This class processes input from command line arguments and executes the request."""

    def __init__(self):
        # initialize openai module, or error out if api key is not defined
        load_dotenv()
        try:
            openai.api_key = os.environ[API_KEY_ENV_VAR]
        except KeyError:
            raise MissingEnvVar("%s requires an api key set in env var %s" % (APP_NAME, API_KEY_ENV_VAR))
        self.__model = "text-davinci-003"
        self.parser = None
        self.subject = None
        self.teller = None
        self.deck = None
        self.card_count = None
        self.spread = None

    def main(self):
        """The main method: draws 3 tarot cards at random and has openai generate a tarot card reading."""
        try:
            self.parse_command_line_args(sys.argv[1:])
        except ArgumentError as arg_error:
            # exit the app with an error code and a formatted message
            self.parser.error(arg_error)
        self.draw_tarot_spread()
        self.interpret_tarot_spread()

    def draw_tarot_spread(self):
        """Shuffles a fresh tarot deck and draws N cards."""
        self.deck = TarotDeck()
        self.spread = self.deck.draw(self.card_count)

    def interpret_tarot_spread(self):
        """Generates a tarot card reading for the given spread and prints to standard output."""
        print("Generating a tarot card reading for {} for the following spread:\n\t{}\n".format(
            self.subject, str(self.spread).strip("[]")))
        tarot_reading_prompt = self.generate_tarot_reading_prompt()
        _, response = self.__ask_openai_to_generate_response(tarot_reading_prompt)
        print("Response:\n{}".format(response))

    def parse_command_line_args(self, command_line_args):
        """Parses command line arguments into instructions for the application."""
        self.parser = ArgumentParser(prog='tarobot',
                                     description='Tarot deck cartomancy application',
                                     exit_on_error=False)
        self.parser.add_argument('--card_count',
                                 help='number of tarot cards to draw in the spread [1-5]\n\tdefault: 3 card spread',
                                 type=int,
                                 choices=range(1, 5 + 1),
                                 default=3)
        self.parser.add_argument('--subject',
                                 help='the name of the person receiving the tarot card reading\n\tdefault: "the seeker"',
                                 type=str,
                                 default='the seeker')
        self.parser.add_argument('--teller',
                                 help='the "person" conducting the tarot card reading\n\t(optional)',
                                 type=str)
        args = self.parser.parse_args(command_line_args)
        self.card_count = args.card_count
        self.subject = args.subject
        if args.teller is not None:
            self.teller = args.teller

    def generate_tarot_reading_prompt(self):
        """Generates the prompt to openai for how to generate a tarot card reading for the given spread."""
        prompt = "Tarot card reading for {} with the cards ".format(self.subject)
        if len(self.spread) < 2:
            prompt += self.spread[0]
        else:
            [*head, tail] = self.spread
            prompt += ", ".join(str(card) for card in head) + ", and " + str(tail)
        if self.teller is not None:
            prompt += " in the style of " + self.teller
        return prompt

    def __ask_openai_to_generate_response(self, prompt):
        """Displays the prompt to and associated response from openai."""
        completion = openai.Completion.create(model=self.__model, prompt=prompt, max_tokens=2000)
        response = "\n".join(list(choice.text for choice in completion.choices)).strip()
        return completion, response
