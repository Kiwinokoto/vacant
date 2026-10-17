import {test} from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {checkBDCOMHistory,historyRows} from "../site/bdcom-history-contract.mjs";
const data=JSON.parse(readFileSync(new URL("../site/data/bdcom-paris-history-2017-2023.json",import.meta.url),"utf8"));
test("Ground floor surveys 2017/2020/2023 are counts, not an invented stock-based series",()=>{
 const rows=historyRows(data);
 assert.deepEqual(rows.map(x=>x.year),[2017,2020,2023]);
 assert.deepEqual(rows.map(x=>x.vacant),[6954,7247,7495]);
 assert.deepEqual(rows.map(x=>x.in_works),[899,1517,1565]);
 assert.deepEqual(rows.map(x=>x.combined),[7853,8764,9060]);
 assert.equal("rate" in rows[0],false);
 assert.deepEqual(rows.map(x=>x.surveyed),[83720,83399,83154]);
 assert.equal(data.count_unit,"premises");
});
test("2020 lowercase AA101 is part of count, contradictory 2020 publications retained",()=>{
 const d=checkBDCOMHistory(data);
 assert.equal(d.provenance["2020"].activity_field,"C20_CODACT");
 assert.match(d.provenance["2020"].note,/3/);
 assert.equal(d.observations[1].publication_rounded,8760);
 assert.equal(d.observations[1].publication_revised_2023,8560);
 assert.equal(d.observations[0].publication_original_vacant,7804);
 assert.equal(d.observations[1].publication_retro_2023_works,1310);
});
test("Reject fabricated history, unrecognized rows, local addresses, or missing discrepancies",()=>{
 const bad=structuredClone(data);bad.observations[0].combined++;
 assert.throws(()=>checkBDCOMHistory(bad));
 const address=structuredClone(data);address.observations[2].address="somewhere";
 assert.throws(()=>checkBDCOMHistory(address));
 const extra=structuredClone(data);extra.observations.push({...extra.observations[2],year:2022});
 assert.throws(()=>checkBDCOMHistory(extra));
 const badStock=structuredClone(data);badStock.observations[1].surveyed=83720;
 assert.throws(()=>checkBDCOMHistory(badStock));
 const nope=structuredClone(data);delete nope.observations[1].publication_revised_2023;
 assert.throws(()=>checkBDCOMHistory(nope));
});
test("Accessible chart and exact-count table wired without inferred vacancy rate",()=>{
 const html=readFileSync(new URL("../site/potentiel.html",import.meta.url),"utf8");
 assert.match(html,/id="bdcom-history-bars"/);
 assert.match(html,/id="bdcom-history-rows"/);
 assert.match(html,/bdcom-history.mjs/);
 assert.match(html,/sans taux comparables/);
});

test("surveyed denominators have verified per-year provenance and do not become rates",()=>{
 const rows=historyRows(data);
 assert.deepEqual(rows.map(r=>r.surveyed),[83720,83399,83154]);
 assert.ok(rows.every(r=>!("rate" in r)));
 const bogus=structuredClone(data);bogus.observations[2].surveyed_source="https://invalid.example";
 assert.throws(()=>checkBDCOMHistory(bogus));
});
