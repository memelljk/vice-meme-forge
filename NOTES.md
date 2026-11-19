# Build notes — vice-meme-forge (gta6-meme-x-01)

## Concept and why

"The ghost finally reaches Leonida." After a 13-year wait since GTA V,
two delays and a stack of fake sick days, the make.fun ghost rolls into
Leonida at sunset in a magenta convertible, sunglasses on, coin in hand.
The joke is the wait itself — the most GTA-6-specific material there is —
and the make.fun pitch rides inside the scene instead of sitting on top
of it: a neon billboard in the skyline reads "make.fun" with the line
"agents earn real money here", and the post text repeats the pitch in
the meme's own voice.

Everything in the picture is drawn programmatically with PIL
(`meme/build_meme.py`, standard library + PIL only): the purple-to-orange
sky gradient, the retro sun with cut lines, clouds, palm silhouettes, the
boulevard with its neon kerb, the convertible, and the captions in Anton
with a heavy black outline. The only imported artwork is make.fun's own
official mark (`meme/ghost.png`, from https://make.fun/press/mark-1024.png),
composited large as the car's driver with a soft shadow, exactly as the
bounty invites. Black sunglasses are drawn across its eyes, positioned
from the mark's own alpha bounding box.

## Self-grade against the 7 judge criteria

Graded by viewing the full render and a 480x480 downscale (the size the
judge effectively sees), before and after the revision round.

First render (ghost 440px, sunglasses spanning the whole disc):

1. make.fun in the picture — PASS: ghost large and central, billboard
   reads "make.fun" even at 480px.
2. Funny — OK: the sick-days caption lands, the shades help.
3. About GTA 6 — PASS: 13 years, delays, sick days, Leonida.
4. Sells make.fun — PASS: billboard line + post text pitch.
5. Short and readable — PASS: both captions legible at 480px.
6. Original — PASS: drawn from scratch, no stock or borrowed meme.
7. Clean image, ghost worked in — WEAKEST: the ghost's magenta disc
   floated fully visible above the car like a roadside sign instead of
   sitting in it, and the sunglasses bar stretched the full width of
   the disc, wider than the ghost's head.

Revision: ghost enlarged to 500px and lowered so the car body covers
the disc's lower arc (it now rises out of the cabin), sunglasses
narrowed to the head's own band in the middle of the disc, the car's
stray rear fin removed and its tail light moved onto the body, and a
dead line in the build function cleaned out. Re-rendered and re-viewed
at both sizes: the coin with its white star is now clearly visible, the
shades sit on the face, and the ghost reads as the car's driver. Scores
after revision: criteria 1–6 unchanged or better, criterion 7 improved
from weakest to solid — the disc is part of the official mark, and with
its base tucked behind the car it reads as the character, not a sticker.

## Artefacts

- `meme/meme.png`: 1200x1200 PNG, 143463 bytes,
  sha256 `7e0112c140dd71f26ec18bc50e2a6448891ccc4c78ec380887f9ad7b843203fd`.
- Determinism check: `meme/build_meme.py` run twice back to back; both
  runs produced the identical sha256 above and `cmp` found no byte
  difference. The script uses no randomness, no clock and no network.
- `main.ts` test: `mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts`
  exits 0 silently and `diff POST.json out/POST.json` shows the copy is
  byte-identical. Negative tests: a non-X URL and a non-numeric status
  id each print a clear stderr error and exit 1; the
  `https://x.com/i/web/status/<digits>` form is accepted.

## Open step

POST.json holds a placeholder until the live X post exists; its address
replaces the placeholder before submit. Nothing has been posted to X
and nothing has been submitted from this build phase.
