#!/usr/bin/env node
// Takes PREPARED inputs, never downloads, invents or silently interpolates observations.
// Usage: node scripts/validate-iris.mjs contours-and-stats.geojson manifest.json [output.geojson]
import { readFile, writeFile } from "node:fs/promises";
import { validateIrisImport } from "../site/iris-contract.mjs";

const [input, manifestFile, output] = process.argv.slice(2);
if (!input || !manifestFile || process.argv.length > 5) {
  console.error("Usage: node scripts/validate-iris.mjs <input.geojson> <manifest.json> [output.geojson]");
  process.exitCode=2;
} else {
  try {
    const [content, metadata] = await Promise.all([readFile(input,"utf8"),readFile(manifestFile,"utf8")]);
    const result = validateIrisImport(JSON.parse(content),JSON.parse(metadata),{forPublication:Boolean(output)});
    if (output) {
      // Fail closed if destination already exists. Never overwrite a reviewed artifact.
      await writeFile(output,JSON.stringify(result)+"\n",{flag:"wx"});
      console.log("Saved validated IRIS file:",output);
    }
    console.log("Validated IRIS import:",JSON.stringify(result.metadata.quality));
  } catch (error) {
    console.error("IRIS import rejected:",error.message);
    process.exitCode=1;
  }
}
