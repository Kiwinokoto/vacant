import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {checkLovac} from "../site/lovac-public-contract.mjs";
const data=JSON.parse(readFileSync(new URL("../site/data/lovac-paris-open-2026.json",import.meta.url),"utf8"));
test("official 20 districts and dates",()=>{
 const x=checkLovac(data);
 assert.equal(x.arrondissements.length,20);
 assert.equal(x.years[6].paris.vacant,105785);
 assert.equal(x.years[6].date_by_variable.vacant,"2025-01-01");
});
test("suppressed or falsified aggregate is rejected",()=>{
 const a=structuredClone(data);a.arrondissements[0].series["2026"].long="s";
 assert.throws(()=>checkLovac(a));
 const b=structuredClone(data);b.years[6].paris.vacant++;
 assert.throws(()=>checkLovac(b));
});
