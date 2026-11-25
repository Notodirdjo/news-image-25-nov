# Wednesday 25 November 2026 — in one picture

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Notodirdjo/news-image-25-nov/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Notodirdjo/news-image-25-nov/reward.svg)](https://make.fun/bounty/news-image-20261125)

One image that sums up Wednesday 25 November 2026's world news, drawn
as a newspaper front page. This is an entry for the make.fun
competition [news-image-20261125](https://make.fun/bounty/news-image-20261125).

## What the picture shows

34 stories from 7 regions, every one checked against reporting from
25 November 2026. The five lead stories:

- **Jiuquan** — China launches Shenzhou-24, carrying the first foreign
  astronaut ever to visit its Tiangong station: Pakistani payload
  specialist Muhammad Zeeshan Ali.
- **Gulf of Finland** — Zelenskyy confirms Ukraine's drones hit the
  Russian cargo ship Sparta II, which he says was carrying weapons.
- **Riyadh** — Houthi fighters hit the Saudi capital's tallest tower,
  wounding 11, the second such strike in under a week.
- **New York** — a US jury convicts Huawei of stealing trade secrets
  and bank fraud, acquitting it of racketeering.
- **New York** — Nvidia shares fall 7% a day after the 31% surge on
  Jensen Huang's return, as the AI rally fizzles.

Then "THE DAY IN BRIEF": the Iowa explosives detonation, the Sarkozy
trial order, the Democrats' 259 House seats, the CIA breach, the Shein
settlement, and twenty more — plus an "ALSO TODAY" line.

## How it works

`draw.py` renders `entry.png` (1024x1024) with Pillow from the verified
facts in the brief — real text, no AI-generated imagery. `main.py`
(Python 3.13, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` and prints the copy's SHA-256 hash.
It needs no network and writes identical bytes on every run.

```sh
python3 draw.py        # render entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copy it to out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
