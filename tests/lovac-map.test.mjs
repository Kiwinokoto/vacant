import test from "node:test";import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {COUNT_BINS,lovacColor,validateLovacGeography,districtLovac} from "../site/lovac-map-contract.mjs";
import {checkLovac} from "../site/lovac-public-contract.mjs";
const d=checkLovac(JSON.parse(readFileSync(new URL("../site/data/lovac-paris-open-2026.json",import.meta.url))));
test("LOVAC count-only fixed classes",()=>{assert.equal(COUNT_BINS.vacant.length,5);assert.notEqual(lovacColor(12000,"vacant"),lovacColor(12001,"vacant"));assert.throws(()=>lovacColor(-1,"long"));});
test("2026 dates and counts without invented rate",()=>{const a=districtLovac(d,"75101",2026,"vacant");assert.equal(a.count,1583);assert.equal("rate" in a,false);assert.throws(()=>districtLovac(d,"75101",2027,"vacant"));});
test("reject wrong/duplicate geography and accept twenty 2025 boundaries",()=>{
 const geo={type:"FeatureCollection",metadata:{geometry:"2025 arrondissement display boundary (IGN)"},features:d.arrondissements.map(x=>({properties:{arrondissement_code:x.code},geometry:{type:"Polygon",coordinates:[]}}))};
 assert.equal(validateLovacGeography(geo,d),true);
 const dup=structuredClone(geo);dup.features[19].properties.arrondissement_code="75101";assert.throws(()=>validateLovacGeography(dup,d));
});
