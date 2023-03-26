# tarobot
An openai-enhanced tarot card bot for fun.

![dall-e oil painting of a fortune-telling robot reading a tarot card spread while sitting at a round table with a glowing crystal ball in a dark room](docs/tarobot%20portrait.png)

## setup
First make sure the required dependencies have been installed:
```sh
pip3 install -r requirements.txt
```

Once the dependencies have been installed, ensure that you have created an openai API key. Make the
api key available in the environment variable `OPENAI_KEY`, you can use a dot-env file (`.env`) to
do so:
```env
OPENAI_API_KEY=< put your openai api key here >
```

If you do not yet have an openai API key, you can create and manage your API keys here:
https://platform.openai.com/account/api-keys


## usage
Then you can simply call the tarobot script and have it draw 3 tarot cards at random, after which
it will generate a tarot card reading for your spread.
```sh
python3 tarobot.py --help
```
```text
usage: tarobot [-h] [--card_count {1,2,3,4,5}] [--subject SUBJECT]
               [--teller TELLER]

Tarot deck cartomancy application

options:
  -h, --help            show this help message and exit
  --card_count {1,2,3,4,5}
                        number of tarot cards to draw in the spread [1-5]
                        default: 3 card spread
  --subject SUBJECT     the name of the person receiving the tarot card
                        reading default: "the seeker"
  --teller TELLER       the "person" conducting the tarot card reading
                        (optional)
```

## example tarot reading
```text
$ python3 tarobot.py --subject Paul --teller Tarobot
Generating a tarot card reading for Paul for the following spread:
        Knight of Wands, Ten of Pentacles, Knight of Cups

Response:
Paul, the combination of cards you've drawn is a positive sign of successful accomplishments in
business, financial stability and emotional gratification. The Knight of Wands signifies that you
will enter a period of determined and focused ambition in your chosen field of endeavor. Your hard
work and dedication will pay off and your projects will come to fruition. The Ten of Pentacles
speaks to financial and material abundance, likely through your own hard work or investments. This
card indicates you have set yourself up for long-term security and have put measures in place for a
sound future. Finally, the Knight of Cups indicates that you will find emotional fulfillment and
success. You will find yourself deeply immersed in activities that bring you a sense of emotional
satisfaction, as well as potentially a new romantic relationship if you are currently single.
Overall, these cards represent a period of great progress for you. With diligence, you can reach
your goals and experience the rewards of success.
```
