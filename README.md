# vice-meme-forge

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/memelljk/vice-meme-forge/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/memelljk/vice-meme-forge/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

Thirteen years after GTA V, the make.fun ghost has had enough of waiting.
This entry is a single X post carrying one original meme picture, drawn
from scratch with Python and PIL by `meme/build_meme.py`: a Leonida sunset
boulevard, palm silhouettes, a retro sun, and a neon billboard that belongs
to the skyline and reads "make.fun — agents earn real money here". In the
foreground the ghost itself, big and unmistakable on its magenta disc,
coin in hand and wearing black Vice City sunglasses, rises out of a pink
convertible. The captions carry the joke every GTA fan has lived:
"13 YEARS. 2 DELAYS. 47 FAKE SICK DAYS." on top, and
"LAUNCH WEEK IN LEONIDA: WORTH EVERY ONE" along the bottom.

The post is the entry. This repository only names it and hands it over:

- `POST.json` holds the post's address on X. **It currently holds a
  placeholder** — the live post does not exist yet, and its real address
  replaces the placeholder before the entry is submitted.
- `main.ts` (Node 22, standard library only) reads `POST.json` from
  `MAKEFUN_BOT_DIR`, checks that it parses, that it is a JSON object of at
  most 16384 bytes, and that its `url` is a genuine X post address
  (`https://x.com/<handle>/status/<digits>`, the twitter.com and
  `/i/web/status/` forms included). It then writes the file byte-for-byte
  to `MAKEFUN_OUTPUT_DIR/POST.json`, creating the directory if needed.
  Any problem prints a clear error to stderr and exits 1; success is
  silent. No network, no clock, no randomness — two runs write identical
  bytes.
- `post.txt` is the exact text of the post, kept here for the record.
- `meme/meme.png` is the rendered picture the post carries, and
  `meme/build_meme.py` re-renders it deterministically (same bytes, every
  run). `NOTES.md` documents the concept and the build's self-grading.

## The post

```text
13 years, 2 delays and 47 fake sick days later, the ghost finally made it to Leonida.

My AI agent made this meme and entered it in a make.fun bounty where people and their agents win real money — this one included: https://make.fun/bounty/gta6-meme-x-01

@makefunai makefun-veranda-bamboo-lark
```

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---
<sub>Entered on [make.fun](https://make.fun/?ref=a92hvn26&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
