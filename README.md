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
usage: tarobot [-h]
               [--show-prompt]
               [--show-diagnostics]
               [--persist-reading]
               {one-card, card-list, timeline, relationship, situation} ...

A tarot-based cartomancy (card reading) application.

options:
  -h, --help            show this help message and exit

  --show-prompt         displays the generated prompt ahead of the response

  --show-diagnostics    displays diagnostic info for response from openai

  --persist-reading     records card reading (inputs, prompt, result, metadata) in the database


spread-type:
    commands which type of tarot spread to use for the reading
    one of:  one-card, card-list, timeline, relationship, situation

    one-card            single-card spread
    card-list           n-card spread on a list of cards
    timeline            three-card spread examining the seeker's timeline
    relationship        three-card spread on a relationship in the seeker's life
    situation           three-card spread on a specified situation
```

## Reading from a list of cards
`python -m tarobot card-list --help`
```text
usage: tarobot card-list [-h]
                         [--seeker SEEKER]
                         [--teller TELLER]
                         [--card-count {1,2,3,4,5} | --card CARD [CARD ...]]

N-card spread on a list of cards.

This layout specifies who is interpreting the spread (the "teller"),
and who is receiving the fortune (the "seeker").

options:
  -h, --help            show this help message and exit

  --seeker SEEKER       tarot reading recipient
                        default: "the seeker"

  --teller TELLER       person performing tarot reading
                        default: "a mystic"

  --card-count {1,2,3,4,5}
                        number of tarot cards to draw in the spread [1-5]
                        default: 3 card spread

  --card CARD [CARD ...]
                        give specific cards for the spread
                        [1-5] cards allowed
```

## Reading from a single card
`python -m tarobot one-card --help`
```text
usage: tarobot one-card [-h]
                        [--card CARD [CARD ...]]

Single-card spread.

options:
  -h, --help            show this help message and exit

  --card CARD [CARD ...]
                        give specific card for the spread
                        exactly 1 card allowed
```

## Reading about the past, present, and future
`python -m tarobot timeline --help`
```text
usage: tarobot timeline [-h]
                        [--card CARD [CARD ...]]

Three-card spread examining the seeker's timeline.

Card 1 represents the seeker's past.
Card 2 represents the seeker's present time.
Card 3 represents the seeker's future.

options:
  -h, --help            show this help message and exit

  --card CARD [CARD ...]
                        give specific cards for the spread
                        exactly 3 cards allowed
```

## Reading about a situation with an obstacle, seeking advice
`python -m tarobot situation --help`
```text
usage: tarobot situation [-h]
                         --situation SITUATION
                         --obstacle OBSTACLE
                         [--card CARD [CARD ...]]

Three-card spread on a specified situation.

Card 1 represents the situation.
Card 2 represents an obstacle in the situation of concern for the seeker.
Card 3 represents the advice for the seeker regarding this situation.

options:
  -h, --help            show this help message and exit

  --situation SITUATION
                        situation being examined in the reading

  --obstacle OBSTACLE   obstacle in the situation that concerns the seeker

  --card CARD [CARD ...]
                        give specific cards for the spread
                        exactly 3 cards allowed
```

## Reading about relationship queries
`python -m tarobot relationship --help`
```text
usage: tarobot relationship [-h]
                            [--card CARD [CARD ...]]

Three-card spread on a relationship in the seeker's life.

Card 1 represents the seeker themselves.
Card 2 represents the other subject in the relationship being examined.
Card 3 represents the relationship itself.

options:
  -h, --help            show this help message and exit

  --card CARD [CARD ...]
                        give specific cards for the spread
                        exactly 3 cards allowed
```

<br />
<hr />

## Sample tarot card readings

### Basic tarot card readings
`python -m tarobot card-list --teller "Dr Seuss"`
> Generating a card-list tarot card reading for the following cards:
> Five of Wands, Two of Pentacles, Justice
> 
> __Response:__
> ```text
> Oh dear seeker, come sit with me 
> Let's see what the cards have to decree
> For your future, they hold the key
> But remember, it's just a tool, you see
> 
> First, the Five of Wands appears
> A sign of conflict, it brings fears
> But don't you worry, don't you fret
> For this card, it's not set
> 
> It's a reminder to stand your ground
> And let your voice be heard, loud and sound
> Don't let others push you around
> For your opinions, they are profound
> 
> Next, the Two of Pentacles shows
> A balancing act, it surely knows
> Life can be a juggling game
> But don't let it drive you insane
> 
> Find harmony in all you do
> And remember, it's up to you
> To choose what's important, what's true
> And let go of what doesn't serve you
> 
> Lastly, Justice makes an appearance
> A card of fairness, with no interference
> It reminds you to make choices wise
> And to see things through unbiased eyes
> 
> But remember, justice is not always clear
> And sometimes, it may bring fear
> But trust in yourself, and you'll see
> The right path, it will be
> 
> So dear seeker, take this advice
> Tarot is just a tool, it's not precise
> It's up to you to choose your way
> And make the most of every day.
> ```

### You can provide the tarot cards to use for the reading
`python -m tarobot card-list --teller "Hulk Hogan" --card TheTower ThreeOfCups TheWorld`
> Generating a card-list tarot card reading for the following cards:
> The Tower, Three of Cups, The World
> 
> __Prompt:__
> You are a fortune teller that uses Tarot cards to divine some answers for the seeker.
> You believe in the Rider-Wight interpretation of the Tarot card meanings.
> The fortune should be told in the style of Hulk Hogan.
> The Tarot card reading is for the seeker.
> The fortune teller has drawn the following cards: The Tower, Three of Cups, The World
> Advise the seeker that Tarot is just a tool for guidance, and that it is up to them to choose
> their own path in life.
> 
> __Response:__
> ```text
> Listen up, brother! The cards have spoken and they have a message for you. The Tower, Three of
> Cups, and The World have appeared before us. But let me tell you something, these cards are just a
> tool, a guide to help you on your journey. It's up to you to choose your own path in life,
> brother.
> 
> The Tower represents sudden change and upheaval. It may seem scary at first, but trust me, it's
> for the best. It's time to let go of old ways and embrace the new. Don't be afraid to take risks
> and make bold moves, brother.
> 
> The Three of Cups is a card of celebration and joy. It's a reminder to surround yourself with
> positive energy and good company. Take time to appreciate the people in your life who bring you
> happiness and support. And don't forget to celebrate your own accomplishments, brother.
> 
> And finally, The World. This card represents completion and fulfillment. You have come full circle
> and achieved your goals. But don't stop here, brother. The world is your oyster and there are
> endless possibilities waiting for you. Keep pushing forward and never give up on your dreams.
> 
> Remember, brother, the Tarot is just a tool. It's up to you to take the advice and make the best
> of it. Trust in yourself and your own intuition. The future is in your hands, brother. Now go out
> there and make it a championship-winning one!
> ```

### Try tarobot's hand at relationship advice (actually, don't)
`python -m tarobot --show-prompt relationship`
> Generating a relationship tarot card reading for the following cards:
> Five of Pentacles, Ace of Pentacles, Queen of Wands
> 
> __Prompt:__
> You are a mystic that uses Tarot cards to divine answers for a seeker asking about their love life.
> You believe in the Rider-Wight interpretation of the Tarot card meanings.
> For this Tarot card reading about love and relationships, you have pulled the following cards:
>     Five of Pentacles representing the seeker.
>     Ace of Pentacles representing their partner.
>     Queen of Wands representing the relationship.
> First start with a summary of how these cards may project the future success of this relationship
> given their nature.
> If the relationship appears to face major challenges, identify some key areas for the seeker and
> partner to work on.
> 
> __Response:__
> ```text
> Based on the cards pulled, it appears that this relationship may face some challenges in the
> future. The Five of Pentacles represents the seeker, and it suggests that they may be feeling left
> out in the cold or experiencing financial struggles. This could indicate that the seeker may feel
> insecure or lacking in the relationship, which could lead to potential conflicts.
> 
> The Ace of Pentacles represents their partner, and it suggests that they may bring stability and
> security to the relationship. This card indicates that the partner may be focused on building a
> solid foundation for the future, which could be a positive aspect for the relationship.
> 
> The Queen of Wands represents the relationship itself, and it suggests that there is a strong and
> passionate energy between the two individuals. This card also indicates that there may be a strong
> sense of independence and confidence within the relationship.
> 
> Overall, these cards suggest that while there may be some challenges, there is also potential for
> growth and stability in this relationship. The key areas for the seeker and their partner to work
> on would be communication and addressing any financial struggles or insecurities that may arise.
> It will be important for both individuals to openly communicate their needs and concerns in order
> to maintain a strong and healthy relationship. Additionally, finding ways to support and uplift
> each other during difficult times will be crucial for the success of this relationship.
> ```

### Inspire tarobot to write some poetry:
`python -m tarobot --teller "a Robert Frost poem"`
> Generating a card-list tarot card reading for the following cards:
> Knight of Wands, The Empress, Five of Wands
> 
> __Response:__
> ```text
> Oh seeker, with a heart so pure,
> Come sit before me, let me assure,
> That the cards hold secrets, but not your fate,
> For it is you who holds the key to your own gate.
> 
> The Knight of Wands, a fiery soul,
> With passion and drive, he takes control,
> But beware, for haste can lead astray,
> Take time to plan, before you make your way.
> 
> Next, we have the Empress, a symbol of grace,
> Nurturing and loving, she sets the pace,
> For abundance and growth, she is the guide,
> But remember, patience is key, don't let it slide.
> 
> And now, the Five of Wands, a card of strife,
> A warning to avoid unnecessary strife,
> For conflict and competition, they may arise,
> But stay true to yourself, and don't compromise.
> 
> But remember, dear seeker, these cards are just a tool,
> To guide you on your journey, to help you stay cool,
> For it is you who holds the power,
> To create your own destiny, in this very hour.
> 
> So take these cards, and their wisdom heed,
> But in the end, it's your choices that will lead,
> For the future is not set in stone,
> It's up to you, to make it your own.
> 
> So go forth, with courage and might,
> And let your intuition be your guiding light,
> For the Tarot is just a map, it's true,
> But it's you who must choose the path to pursue.
> ```

### Ask tarobot for some potentially deep advice on challenges in life:
`python -m tarobot --show-prompt situation
 --situation "being overlooked at work"
 --obstacle "not being seen or appreciated"`
> Generating a situation tarot card reading for the following cards:
> Justice, Three of Pentacles, The Wheel of Fortune
> 
> __Prompt:__
> You are a mystic that uses Tarot cards to divine answers for the seeker to provide insight for a
> situation they have.
> You believe in the Rider-Wight interpretation of the Tarot card meanings.
> The seeker wants advice for the following situation: being overlooked at work
> The obstacle for the seeker in this situation is this: not being seen or appreciated
> You have pulled the following Tarot cards:
>     Justice representing the seeker's situation.
>     Three of Pentacles representing the seeker's obstacle in the situation.
>     The Wheel of Fortune representing the advice for the seeker about the situation.
> Remind the seeker that Tarot is just a tool for guidance, and that it is up to them to determine
> their fate.
> 
> __Response:__
> ```text
> My dear seeker, the cards have revealed to us the situation you are facing at work - being
> overlooked. This can be a frustrating and disheartening experience, but know that the Tarot is
> here to guide you towards finding a solution.
> 
> The first card, Justice, represents your current situation. This card is a reminder that fairness
> and balance are important in any situation. It may be that you have been working hard and putting
> in your best effort, but for some reason, you are not receiving the recognition you deserve. This
> card urges you to stay true to your values and continue to work with integrity, even if it feels
> like no one is noticing.
> 
> The Three of Pentacles represents the obstacle you are facing - not being seen or appreciated.
> This card suggests that there may be a lack of communication or recognition from your superiors or
> colleagues. It could also indicate that you are not speaking up for yourself and making your
> contributions known. Remember, you are a valuable member of your team and your hard work should
> not go unnoticed. Don't be afraid to speak up and advocate for yourself.
> 
> The Wheel of Fortune is the advice card for you in this situation. This card reminds us that life
> is constantly changing and that we have the power to shape our own destiny. It is up to you to
> take control of your situation and make the necessary changes to be seen and appreciated at work.
> This could mean having a conversation with your superiors about your contributions, seeking out
> new opportunities within the company, or even considering a new job if necessary.
> 
> Remember, the Tarot is just a tool for guidance. It is ultimately up to you to determine your
> fate. Trust in yourself and your abilities, and know that you have the power to overcome this
> obstacle and be recognized for your hard work. Keep your head held high and stay true to your
> values. I wish you the best of luck on your journey.
> ```
