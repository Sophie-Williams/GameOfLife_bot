# Life (lived on Twitter)

A twitter bot that tweets a wrapped 8x8 board of cells, and each hour produces the next "generation" of live and dead cells according to the rules of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). When the game produces an "extinct" board or the configuration turns stable, an alert is tweeted instead followed by a new, randomly generated board.

A twitter bot simulating [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)—each hour it tweets the next "generation" of live and dead cells on a wrapped 8x8 board. When the game produces an "extinct" board or the configuration turns stable, an alert is tweeted instead followed by a new, randomly generated board.

Watch it go [@gameoflife_bot](https://twitter.com/gameoflife_bot)

## Details

The code is pushed to a Heroku app, and tweets hourly using a Heroku scheduler, calling `tweet`. It can also be manually triggered to tweet by navigating to the local repository and running `heroku run tweet`.

## Acknowledgments

* Twitter API connection and basic structure taken from [this Science Friday tutorial](https://medium.com/science-friday-footnotes/how-to-make-a-twitter-bot-in-under-an-hour-259597558acf).
* The [Numberphile Youtube channel](https://www.youtube.com/channel/UCoxcjq-8xIDTYp3uz647V5A), for [doing a video](https://www.youtube.com/watch?v=R9Plq-D1gEk) on this "no-player" game.
