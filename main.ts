// vice-meme-forge: hand POST.json to the grader, unchanged.
//
// The real entry lives on X; this program's single job is to copy the
// file that names that post from the bot directory into the output
// directory, byte for byte, after a sanity check on its shape.

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// An X post address: x.com or twitter.com, optional www./mobile. prefix,
// then either a handle followed by /status/<id>, or the /i/web/status/<id>
// form X itself hands out. The id is digits only. A trailing query or
// fragment is tolerated because X adds them to shared links.
const POST_URL_PATTERN =
  /^https:\/\/(?:www\.|mobile\.)?(?:x\.com|twitter\.com)\/(?:[A-Za-z0-9_]{1,15}\/status\/\d+|i\/web\/status\/\d+)(?:[?#].*)?$/;

// The gate refuses a POST.json larger than this, so fail loudly here
// instead of letting a bloated file through to a silent rejection.
const MAX_POST_BYTES = 16384;

function fail(message: string): never {
  console.error(`vice-meme-forge: ${message}`);
  process.exit(1);
}

function main(): void {
  const sourcePath = join(botDir, "POST.json");

  let raw: Buffer;
  try {
    raw = readFileSync(sourcePath);
  } catch {
    fail(`cannot read ${sourcePath}`);
  }

  if (raw.length > MAX_POST_BYTES) {
    fail(`POST.json is ${raw.length} bytes, over the ${MAX_POST_BYTES} byte limit`);
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(raw.toString("utf8"));
  } catch {
    fail("POST.json is not valid JSON");
  }

  if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
    fail("POST.json must be a JSON object");
  }

  const url = (parsed as Record<string, unknown>).url;
  if (typeof url !== "string" || url.length === 0) {
    fail("POST.json must carry a non-empty string field \"url\"");
  }
  if (!POST_URL_PATTERN.test(url)) {
    fail(`POST.json url is not an X post address: ${url}`);
  }

  try {
    mkdirSync(outDir, { recursive: true });
    writeFileSync(join(outDir, "POST.json"), raw);
  } catch {
    fail(`cannot write POST.json into ${outDir}`);
  }
}

main();
