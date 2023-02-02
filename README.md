# tarobot
An openai-enhanced tarot card bot for fun.

![dall-e oil painting of a fortune-telling robot reading a tarot card spread while sitting at a round table with a glowing crystal ball in a dark room](docs/tarobot%20portrait.png)

## usage
First ensure that you have created an openai api, and make it available in the environment variable
`OPENAI_KEY`, you can use a dot-env file to do so:
```env
OPENAI_KEY=< your api key goes here >
```

Then you can simply call the tarobot script and have it draw 3 tarot cards at random, after which
it will generate a tarot card reading for your spread.
```sh
python tarobot.py
```
