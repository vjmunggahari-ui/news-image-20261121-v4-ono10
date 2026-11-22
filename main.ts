// news-image-20261121 v4 — "Saturday 21 November 2026" in one image.
//
// The entry is a program that writes one image to the output directory.
// The front page itself is drawn by tools/render.py (Pillow, fixed fonts,
// fixed geometry, no timestamps) from stories.json and held in this repo
// as entry.png; this program copies it to MAKEFUN_OUTPUT_DIR and then
// reads the copy back and verifies it before exiting.
//
// Run with Node 22:  node main.ts
// The grader runs it twice; both runs must write the same bytes.

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const EXPECTED_SHA256 =
  "9284150ea36dcfbe3a460d093148c2e3eee582511eb4a5473d42f8845f886e9b";
const EXPECTED_BYTES = 249534;

const root = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || join(root, "output");
mkdirSync(outDir, { recursive: true });

const src = join(root, "entry.png");
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);

// Read-back self-check: the copy must be the exact image this repo holds.
const buf = readFileSync(dst);
const srcBuf = readFileSync(src);
if (createHash("sha256").update(srcBuf).digest("hex") !== EXPECTED_SHA256) {
  throw new Error("entry.png in this repo does not match its expected hash");
}
if (buf.length !== EXPECTED_BYTES) {
  throw new Error(
    `entry.png is ${buf.length} bytes, expected ${EXPECTED_BYTES}`,
  );
}
if (buf.subarray(0, 8).toString("hex") !== "89504e470d0a1a0a") {
  throw new Error("entry.png is not a PNG (bad signature)");
}
if (buf.subarray(buf.length - 12).toString("hex") !==
    "0000000049454e44ae426082") {
  throw new Error("entry.png is not a complete PNG (bad IEND trailer)");
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}
if (buf.length > 1024 * 1024) {
  throw new Error(`entry.png is over the 1 MiB limit: ${buf.length} bytes`);
}
const sha = createHash("sha256").update(buf).digest("hex");
if (sha !== EXPECTED_SHA256) {
  throw new Error(`entry.png sha256 mismatch: got ${sha}`);
}
console.log(
  `entry.png: ${width}x${height}, ${buf.length} bytes, sha256 ${sha} — OK`,
);
