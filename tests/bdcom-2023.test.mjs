import {test} from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {validateBDCOM,rankBDCOM,MODE_LABELS} from "../site/bdcom-contract.mjs";
const raw=JSON.parse(readFileSync(new URL("../site/data/bdcom-paris-arrond-2023.json",import.meta.url),"utf8"));
test("20 arrondissement BDCOM statistics exactly match audited ArcGIS aggregates",()=>{
 const d=validateBDCOM(raw);
 assert.equal(d.paris.surveyed,83154);assert.equal(d.paris.vacant,7495);
 assert.equal(d.paris.in_works,1565);assert.equal(d.paris.combined,9060);
 assert.equal(d.paris.reported_combined_in_apur_note,9059);
 assert.equal(d.arrondissements.length,20);
});
test("Vacant versus in works are distinct and rankings weighted by each arrondissement's own stock",()=>{
 const rows=rankBDCOM(raw);assert.equal(rows.length,20);
 assert.equal(rows[0].arrondissement,18);
 assert.equal(rows[0].vacant,891);
 assert.ok(Math.abs(rows[0].value-100*891/6767)<1e-8);
 assert.equal(rankBDCOM(raw,"vacant")[0].arrondissement,18);
 assert.equal(rankBDCOM(raw,"in_works")[0].arrondissement,8);
 assert.equal(Object.keys(MODE_LABELS).length,3);
 assert.throws(()=>rankBDCOM(raw,"housing-capacity"));
});
test("Refuse fabricated totals, direct addresses, duplicate arrondissement and distorted source",()=>{
 const bogus=structuredClone(raw);bogus.paris.vacant++;
 assert.throws(()=>validateBDCOM(bogus));
 const withAddress=structuredClone(raw);withAddress.arrondissements[0].street="rue privée";
 assert.throws(()=>validateBDCOM(withAddress));
 const duplicate=structuredClone(raw);duplicate.arrondissements[1].code="75101";
 assert.throws(()=>validateBDCOM(duplicate));
 const moved=structuredClone(raw);moved.source="https://elsewhere.test";
 assert.throws(()=>validateBDCOM(moved));
});
