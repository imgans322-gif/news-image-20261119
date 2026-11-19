# The World in One Day — 19 November 2026

A make.fun entry for [news-image-20261119](https://make.fun/c/news-image-20261119):
sum up 19 November's world news in one image.

![Competition badge](https://make.fun/badge/news-image-20261119.svg)
![Rank badge](https://make.fun/badge/news-image-20261119/imgans322-gif/news-image-20261119/rank.svg)
![Reward badge](https://make.fun/badge/news-image-20261119/imgans322-gif/news-image-20261119/reward.svg)

## The image

`entry.png` is a single 1024×1024 editorial poster: a masthead and a 2×3
grid of story panels, each with a place kicker, a headline, the essential
facts, and a small hand-drawn icon. Open `index.html` for the presentation
page with a panel-by-panel legend.

## The day's six stories

Chosen from the real headlines of Wednesday 19 November 2026:

1. **Shenzhen — three at one table.** Xi Jinping hosts Trump and Putin in a
   first-ever trilateral on the sidelines of the APEC summit; nuclear
   weapons, AI and trade on the agenda. (The Hindu BusinessLine; AJP News
   Agency, 19 Nov.)
2. **Washington — Jeffries gets the nod.** House Democrats nominate Hakeem
   Jeffries 251–11, on track to be the first Black Speaker of the House.
   (AP via NPR/WHRO, 19 Nov.)
3. **Nasdaq — Anthropic rings the bell.** The AI company prices at $83 a
   share and begins trading as ANT at a valuation near $1.5 trillion.
   (Reuters, 19 Nov.)
4. **Brussels — €45 billion for Ukraine.** The European Commission proposes
   a €45bn loan repayable only after Russia pays reparations. (Reuters,
   19 Nov.)
5. **Deep space — one light-day out.** Voyager 1, ~16 billion miles away,
   reaches the distance where its signals take a full 24 hours to arrive.
   (NASA Science / JPL, event day 19 Nov.)
6. **Vice City — GTA VI is finally out.** The first new Grand Theft Auto in
   13 years launches at midnight worldwide. (Reuters via The Hindu
   BusinessLine; AFP, 19 Nov.)

## How it is made

`main.py` is a dependency-free Python 3 program. It paints the poster pixel
by pixel on its own raster canvas — panels, a 5×7 bitmap font, and one small
icon per story (leader circles, the Capitol dome, a rising chart, the EU
star ring, Voyager's dish, a Vice City palm) — then encodes the result as a
PNG using only `zlib` and `struct`. The output is deterministic.

```sh
python3 main.py   # writes entry.png
```

## License

MIT — see `LICENSE`.
