import { copyFileSync, mkdirSync, existsSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(outDir, { recursive: true });
const src = "entry.png";
if (!existsSync(src)) {
  console.error("entry.png not found — run `python3 build_image.py` first.");
  process.exit(1);
}
copyFileSync(src, join(outDir, "entry.png"));
console.log(`Wrote ${join(outDir, "entry.png")}`);
