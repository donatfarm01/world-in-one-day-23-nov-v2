import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry program for news-image-20261123.
// The front page is drawn by draw.py and shipped as entry.png; this program
// only copies it to /output. Deterministic by construction: same input bytes
// in, same output bytes out.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";

// Fail loudly instead of copying garbage: entry.png must exist, be non-empty,
// and start with the PNG magic bytes. A broken input must never silently
// become a graded output.
const src = join(here, "entry.png");
const header = readFileSync(src).subarray(0, 8);
if (header.length < 8 || header[0] !== 0x89 || header[1] !== 0x50 ||
    header[2] !== 0x4e || header[3] !== 0x47) {
  throw new Error("entry.png is missing or is not a PNG file");
}
const expectedBytes = statSync(src).size;
if (expectedBytes === 0 || expectedBytes > 1048576) {
  throw new Error(`entry.png has an implausible size: ${expectedBytes} bytes`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));

// Confirm the copy landed whole: same size as the source.
if (statSync(join(outDir, "entry.png")).size !== expectedBytes) {
  throw new Error("entry.png copy is incomplete");
}
