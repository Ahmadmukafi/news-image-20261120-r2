// news-image-20261120 round-2 entry: the front page is drawn at build time
// (see render.py) and shipped beside this program. At grade time the program
// only copies that finished image into the output directory: no network, no
// rendering, no subprocesses, standard library only.
// Run with: MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(join(here, "entry.png"), target);
if (statSync(target).size === 0) throw new Error("entry.png copied empty");
