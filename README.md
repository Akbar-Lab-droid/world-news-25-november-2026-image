# The World in One Page — 25 November 2026

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/Akbar-Lab-Droid/world-news-25-november-2026-image/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/Akbar-Lab-Droid/world-news-25-november-2026-image/reward.svg)](https://make.fun/bounty/news-image-20261125)

One image that sums up the world's news of Wednesday 25 November 2026:
44 verified stories on a single dense broadsheet page.

## The day in brief

- **Lead:** Shenzhou-24 docks with Tiangong carrying Muhammad Zeeshan
  Ali — the first Pakistani in orbit and the first foreign astronaut
  aboard China's space station.
- **War:** Two oil tankers struck by naval mines catch fire in the
  Strait of Hormuz as the Iran war escalates.
- **Markets:** The Dow closes above 50,000 for the first time while
  Asian markets tumble.
- **Tech:** A Brooklyn jury convicts Huawei of stealing trade secrets.

Plus 40 more stories across six sections: Conflict & Middle East,
Russia-Ukraine, Asia & Pacific, Markets & Business, Science & Tech,
and World & Climate. Every story was verified against multiple news
sources on the day.

## How it works

`draw.py` renders the broadsheet (1024×1024 PNG) with Pillow at
build time. `main.py` is standard-library only: it simply copies the
committed `entry.png` to `MAKEFUN_OUTPUT_DIR`, so the grader — which
runs without PIL or fonts — reproduces the exact same bytes.

```sh
python3 draw.py        # render entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
