import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {checkLovac} from "../site/lovac-public-contract.mjs";
import {SHARE_BINS,longTermSnapshot,referenceForShare,shareLongColor} from "../site/lovac-long-analysis.mjs";
const data=checkLovac(JSON.parse(readFileSync(new URL("../site/data/lovac-paris-open-2026.json",import.meta.url))));
test("2026 valid same-day denominator is vacant private dwellings, not housing stock",()=>{
 const x=longTermSnapshot(data,2026);
 assert.equal(x.date,"2025-01-01");
 assert.equal(x.parisLong,26264);assert.equal(x.parisVacant,105785);
 assert.ok(Math.abs(x.paris-24.827)<.01);assert.equal("housingRate" in x,false);
 assert.equal(x.rows[0].arrondissement,8);
 assert.ok(Math.abs(x.rows[0].value-41.17)<.02);
 assert.equal(longTermSnapshot(data,2026,"long").rows[0].arrondissement,18);
});
test("2023 unequal reference dates must never produce an apparent percentage",()=>{
 assert.throws(()=>referenceForShare(data,2023),/dates de référence/);
 assert.throws(()=>longTermSnapshot(data,2023,"share-long"),/dates de référence/);
 assert.equal(longTermSnapshot(data,2023,"long").rows.length,20);
});
test("weighted Paris percentage and basic validity",()=>{
 const x=longTermSnapshot(data,2026);
 const sum=x.rows.reduce((n,r)=>n+r.long,0);
 assert.equal(sum,x.parisLong);
 assert.equal(x.paris,100*x.parisLong/x.parisVacant);
 assert.ok(x.rows.every(row=>row.value>=0&&row.value<=100));
 assert.equal(SHARE_BINS.length,5);
 assert.notEqual(shareLongColor(20),shareLongColor(20.01));
 assert.throws(()=>shareLongColor(101));assert.throws(()=>longTermSnapshot(data,2027));
 const bogus=structuredClone(data);bogus.arrondissements[0].series["2026"].long=2000;
 assert.throws(()=>longTermSnapshot(bogus,2026));
});
test("all supported snapshots use same dated numerator/denominator",()=>{
 for(const y of [2020,2021,2022,2024,2025,2026])assert.ok(referenceForShare(data,y).endsWith("-01-01"));
});
