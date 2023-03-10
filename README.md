# tarobot
An openai-enhanced tarot card bot for fun.

![dall-e oil painting of a fortune-telling robot reading a tarot card spread while sitting at a round table with a glowing crystal ball in a dark room](docs/tarobot%20portrait.png)

## setup
First make sure the required dependencies have been installed:
```sh
pip install -r requirements.txt
```

Once the dependencies have been installed, ensure that you have created an openai API key. Make the
api key available in the environment variable `OPENAI_KEY`, you can use a dot-env file (`.env`) to
do so:
```env
OPENAI_KEY=< your api key goes here >
```

If you do not yet have an openai API key, you can create and manage your API keys here:
https://platform.openai.com/account/api-keys


## usage
Then you can simply call the tarobot script and have it draw 3 tarot cards at random, after which
it will generate a tarot card reading for your spread.
```sh
python tarobot.py
```
