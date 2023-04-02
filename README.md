# Tarobot
An openai-enhanced tarot card bot for fun.

![dall-e oil painting of a fortune-telling robot reading a tarot card spread while sitting at a round table with a glowing crystal ball in a dark room](docs/tarobot%20portrait.png)

## Setup
First make sure the required dependencies have been installed:
`pip3 install -r requirements.txt`

Once the dependencies have been installed, ensure that you have created an openai API key. Make the
api key available in the environment variable `OPENAI_KEY`, you can use a dot-env file (`.env`) to
do so:
```env
OPENAI_API_KEY=< put your openai api key here >
```

If you do not yet have an openai API key, you can create and manage your API keys here:
https://platform.openai.com/account/api-keys


## Usage
Then you can simply call the tarobot script and have it draw 3 tarot cards at random, after which
it will generate a tarot card reading for your spread.
`python3 tarobot.py --help`
```text
usage: tarobot [-h] [--card-count {1,2,3,4,5}] [--subject SUBJECT]
               [--teller TELLER]
               [--use-card-list USE_CARD_LIST [USE_CARD_LIST ...]]
               [--show-prompt]

Tarot deck cartomancy application

options:
  -h, --help            show this help message and exit
  --card-count {1,2,3,4,5}
                        number of tarot cards to draw in the spread [1-5]
                        default: 3 card spread
  --subject SUBJECT     the name of the person receiving the tarot card
                        reading default: "the seeker"
  --teller TELLER       the "person" conducting the tarot card reading
                        (optional)
  --use-card-list USE_CARD_LIST [USE_CARD_LIST ...]
                        takes specific cards from the user instead of a random
                        draw from the deck
  --show-prompt         displays the generated prompt ahead of the response
```

<br />
<hr />

## Sample tarot card readings

### Basic tarot card readings
`python3 tarobot.py --subject Paul --teller Tarobot`
```text
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

### You can provide the tarot cards to use for the reading
`python3 tarobot.py --teller "Hulk Hogan" --use-card-list TheTower ThreeOfCups TheWorld --show-prompt`
```text
Generating a tarot card reading for the seeker for the following spread:
	The Tower, Three of Cups, The World

Prompt:
Tarot card reading for the seeker with the cards The Tower, Three of Cups, and The World in the
style of Hulk Hogan

Response:
Well, Hulkamaniacs - it looks like the Tarot cards have been dealt, and they reveal that you have a
lot of changes headed your way! The Tower card is a sign of a huge shake-up and breakthrough
happening in your life, so be ready for it! The Three of Cups is a call for celebration and even
marks a new beginning. Get ready to let go of the past and move into a whole new world! Finally, The
World card speaks of the benefits of manifesting your dreams. It signifies completion and
accomplishment, as well as the reward for all your hard work. So grab your thunder belt, brother -
it looks like you've got some major breakthroughs headed your way!
```

### Try tarobot's hand at songwriting
`python3 tarobot.py --teller "Iron Maiden lyrics" --show-prompt`
```text
Generating a tarot card reading for the seeker for the following spread:
	Seven of Cups, Queen of Pentacles, The Sun

Prompt:
Tarot card reading for the seeker with the cards Seven of Cups,
Queen of Pentacles, and The Sun in the style of Iron Maiden lyrics

Response:
Verse 1:
The Seven of Cups brings confusion,
A crossroads up ahead.
But the Queen of Pentacles knows the answer can be found,
From The Sun enlightening her instead

Chorus:
A new path, a new day,
A wiser choice will lead the way.
An inner journey, a brighter light,
Answers come in second sight.

Verse 2:
The Queen of Pentacles stands still,
Confident in her decision.
Ignoring the distraction of the Seven of Cups,
In the Sun lies her true vision.

Chorus:
A new path, a new day,
A wiser choice will lead the way.
An inner journey, a brighter light,
Answers come in second sight.
```

### Inspire tarobot to write some poetry:
`python3 tarobot.py --teller "a Robert Frost poem" --show-prompt`
```text
Generating a tarot card reading for the seeker for the following spread:
Ace of Wands, The Tower, Seven of Cups

Prompt:
Tarot card reading for the seeker with the cards Ace of Wands,
The Tower, and Seven of Cups in the style of a Robert Frost poem

Response:
A glimpse of the future through these cards three,
A Tower filled with sudden calamity,
An Ace of Wands in potential to see,
A dream of good luck throughout, the Seven of Cups all we.

So now what, the seeker asks,
Amidst the chaos of Great Task?
Look past the present’s stormy mask
As what you seek lies in the path that wand did cast.

An answer to the dilemna you seek,
In a universe so frequently bleak,
Will come from the surprises that this moment meek
Despite other cards of ill-fame cast in its shadow deep.

Your destiny to craft is in your hand,
An Ace of Wands, set to expand
To explore and understand,
Defeating fate and triumphant stand.
```
