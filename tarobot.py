#!/usr/bin/env python3

from dotenv import load_dotenv
import openai
import os
from tarot import TarotDeck

"""This module provides a script that draws N cards from a shuffled tarot card deck and returns an
interpretation of the generated tarot card spread."""

APP_NAME = "Tarobot"
API_KEY_ENV_VAR = "OPENAI_KEY"


class MissingEnvVar(Exception):
    """This exception is raised when a required environment variable has not been defined."""
    pass


def main():
    """The main method: draws 3 tarot cards at random and has openai generate a tarot card reading."""
    initialize_app()

    # generate a tarot card reading of the user's spread and display
    deck = TarotDeck()
    tarot_spread = deck.draw(3)
    tarot_reading_prompt = generate_tarot_reading_prompt(tarot_spread)
    ask_openai_to_generate_response(tarot_reading_prompt)


def initialize_app():
    """Loads the app's associated dot env file and raises an exception if required env vars are not defined."""
    load_dotenv()
    try:
        openai.api_key = os.environ[API_KEY_ENV_VAR]
    except KeyError:
        raise MissingEnvVar("%s requires an api key set in env var %s" % (APP_NAME, API_KEY_ENV_VAR))


def generate_tarot_reading_prompt(spread, teller="an optimist"):
    """Generates the prompt to openai for how to generate a tarot card reading for the given spread."""
    prompt = "Tarot card reading for the seeker with the cards "
    if len(spread) < 2:
        prompt += spread[0]
    else:
        [*head, tail] = spread
        prompt += ", ".join(str(card) for card in head) + ", and " + str(tail)
    prompt += " in the style of " + teller
    return prompt


def ask_openai_to_generate_response(prompt):
    """Displays the prompt to and associated response from openai."""
    print("\nPrompt:\n{}".format(prompt))
    completion = openai.Completion.create(model='text-davinci-003', prompt=prompt, max_tokens=2000)
    response = "\n".join(list(choice.text for choice in completion.choices)).strip()
    print("\nResponse:\n{}".format(response))
    return completion


if __name__ == "__main__":
    main()
