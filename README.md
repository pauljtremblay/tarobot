# Tarobot
An openai-enhanced tarot card bot for fun.

![dall-e oil painting of a fortune-telling robot reading a tarot card spread while sitting at a round table with a glowing crystal ball in a dark room](docs/tarobot%20portrait.png)

## Setup
First make sure the required dependencies have been installed:
`pip install -r requirements.txt`

Once the dependencies have been installed, ensure that you have created an openai API key. Make the
api key available in the environment variable `OPENAI_KEY`, you can use a dot-env file (`.env`) to
do so. You will also need to define a database password env var, even if not using database
integration (a dummy value is sufficient).
```env
OPENAI_API_KEY=< put your openai api key here >
TAROBOT_SCHEMA_PASS=some-placeholder-value
```

If you do not yet have an openai API key, you can create and manage your API keys here:
https://platform.openai.com/account/api-keys


## Usage
Then you can simply call the tarobot script and have it draw 3 tarot cards at random, after which
it will generate a tarot card reading for your spread.
`python -m tarobot --help`
```text
usage: tarobot [-h] [--show-prompt] [--show-diagnostics] [--persist-reading]
               {card-list,one-card,past-present-future,seeker-subject-relationship,situation-obstacle-advice}
               ...

Tarot deck cartomancy application

options:
  -h, --help            show this help message and exit
  --show-prompt         displays the generated prompt ahead of the response
  --show-diagnostics    displays diagnostic output from the completion
                        response returned from openai
  --persist-reading     inserts a record of the tarot card reading (inputs,
                        prompt, result, metadata) in the database

spread-type:
  {card-list,one-card,past-present-future,seeker-subject-relationship,situation-obstacle-advice}
                        spread-type help
    card-list           Perform a tarot card spread on a list of cards, with a
                        fortune teller and seeker
    one-card            Perform a simple one card tarot card spread
    past-present-future
                        Perform a three card tarot card spread: C1 = past, C2
                        = present, C3 = future
    seeker-subject-relationship
                        Perform a three card tarot card spread: C1 = seeker,
                        C2 = subject, C3 = relationship
    situation-obstacle-advice
                        Perform a three card tarot card spread: C1 =
                        situation, C2 = obstacle, C3 = advice
```

`python -m tarobot card-list --help`
```text
usage: tarobot card-list [-h]
                         [--card-count {1,2,3,4,5} | --card CARD [CARD ...]]
                         [--seeker SEEKER] [--teller TELLER]

options:
  -h, --help            show this help message and exit
  --card-count {1,2,3,4,5}
                        number of tarot cards to draw in the spread [1-5]
                        default: 3 card spread
  --card CARD [CARD ...]
                        takes specific card[s] from the user instead of a
                        random draw from the deck
  --seeker SEEKER       tarot reading recipient default: "the seeker"
  --teller TELLER       person performing tarot reading default: "a mystic"
```

`python -m tarobot situation-obstacle-advice --help`
```text
usage: tarobot situation-obstacle-advice [-h] --situation SITUATION --obstacle
                                         OBSTACLE

options:
  -h, --help            show this help message and exit
  --situation SITUATION
                        situation being explored by tarot card reading
  --obstacle OBSTACLE   obstacle in the situation being addressed by the tarot
                        card reading
```

<br />
<hr />

## Sample tarot card readings

### Basic tarot card readings
`python -m tarobot card-list --subject Paul --teller Tarobot`
```text
Generating a card-list tarot card reading for Paul for the following spread:
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
`python -m tarobot --show-prompt --card-list --teller "Hulk Hogan" --card TheTower ThreeOfCups TheWorld`
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

### Try tarobot's hand at relationship advice (actually, don't)
` python -m tarobot --show-prompt seeker-subject-relationship`
```text
Generating a seeker-subject-relationship tarot card reading for the following cards:
        Three of Pentacles, Nine of Swords, Seven of Pentacles

Prompt:
Tarot card reading for love and relationships with Three of Pentacles representing the seeker, Nine of Swords
representing the subject, Seven of Pentacles representing the relationship.

Response:
The Three of Pentacles suggests that the seeker is someone who is hardworking and ambitious, and is willing to put in
the effort to make their dreams come true. They are also likely to be a good problem solver and have a strong sense of
responsibility.

The Nine of Swords suggests that the subject is someone who is struggling with inner turmoil and anxiety. They may be
feeling overwhelmed by their current situation and may be struggling to find a way out.

The Seven of Pentacles suggests that the relationship between the seeker and the subject is one that is full of
potential. Both parties are willing to put in the effort to make it work, and if they can find a way to work through
their issues, the relationship could be very rewarding. However, it will require patience and dedication from both
parties in order to make it work.

The tarot card reading sentiment:
Positive
```

### Inspire tarobot to write some poetry:
`python -m tarobot --show-prompt card-list --teller "a Robert Frost poem"`
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

An answer to the dilemma you seek,
In a universe so frequently bleak,
Will come from the surprises that this moment meek
Despite other cards of ill-fame cast in its shadow deep.

Your destiny to craft is in your hand,
An Ace of Wands, set to expand
To explore and understand,
Defeating fate and triumphant stand.
```

### Ask tarobot for some potentially deep advice on challenges in life:
`python -m tarobot --show-prompt situation-obstacle-advice
 --situation "being overlooked at work"
 --obstacle "not being seen or appreciated"`
```text
Generating a situation-obstacle-advice tarot card reading for the following cards:
        Justice, Three of Pentacles, The Wheel of Fortune

Prompt:
Tarot card reading with Justice representing the situation, Three of Pentacles representing the obstacle, The Wheel of
Fortune representing the advice. The seeker wants advice about being overlooked at work. The obstacle in their situation
is not being seen or appreciated.

Response:
Justice is a card of balance and fairness, and it suggests that the seeker is in a situation where they are not being
treated fairly. The Three of Pentacles is a card of hard work and dedication, and it suggests that the seeker is putting
in a lot of effort but not being recognized for it. The Wheel of Fortune is a card of luck and chance, and it suggests
that the seeker should take a chance and make their voice heard. They should speak up and make sure that their hard work
is noticed and appreciated. They should also take the time to recognize and appreciate the hard work of their
colleagues. By doing this, they will create a more balanced and fair work environment.

The tarot card reading sentiment:
Positive
```
