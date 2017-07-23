# Conway's Game of Life Twitter Bot

A twitter bot that tweets an 8x8 board of cells, and each hour produces the next "generation" of cells according to [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). When the game produces an "extinct" board or the configuration turns stable, an alert is tweeted instead followed by a new randomly generated board.

Watch it go [@gameoflife_bot](https://twitter.com/gameoflife_bot)

## Details

<uh you need heroku and it runs hourly using a scheduler>

## Acknowledgments

* Twitter API connection and basic structure taken from [this Science Friday tutorial](https://medium.com/science-friday-footnotes/how-to-make-a-twitter-bot-in-under-an-hour-259597558acf).
