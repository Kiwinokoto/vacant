import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { parseOfflineFixture, FIXTURE_SHA256, SOURCE_SHA256, EXPECTED_FEATURES }
  from "../experiments/apur-periods/offline-contract.mjs";

const geometry={type:"Polygon",coordinates:[[
  [2.373,48.854],[2.374,48.854],[2.374,48.855],[2.373,48.855],[2.373,48.854]
]]};
function fixture(){
  return {type:"FeatureCollection",metadata:{
    research_only:true,public_release_allowed:false,not_vacancy_data:true,
    source_crs:"EPSG:2154",output_crs:"EPSG:4326",license:"ODbL-1.0",
    source_archive_sha256:SOURCE_SHA256,
    scientific_vintage:"not confirmed by Apur",
    matched_source_features:EXPECTED_FEATURES,included_features:EXPECTED_FEATURES,excluded:{}
  },features:Array.from({length:EXPECTED_FEATURES},(_,i)=>({
    type:"Feature",geometry,properties:{object_id:i+1,period_code:i%2===0?3:11}
  }))};
}
function encode(data){
 const buf=Buffer.from(JSON.stringify(data));
 return {bytes:buf.buffer.slice(buf.byteOffset,buf.byteOffset+buf.byteLength),
   sha256:createHash("sha256").update(buf).digest("hex")};
}
test("offline defaults to pinned real fixture SHA-256",()=>{
 assert.match(FIXTURE_SHA256,/^[a-f0-9]{64}$/);
 assert.match(SOURCE_SHA256,/^[a-f0-9]{64}$/);
});
test("accepts only complete validated, 150-feature snapshot",async()=>{
 const {bytes,sha256}=encode(fixture());
 const result=await parseOfflineFixture(bytes,sha256);
 assert.equal(result.collection.features.length,150);
 assert.equal(result.counts[3],75);
 assert.equal(result.counts[11],75);
 assert.equal(result.sha256,sha256);
});
test("rejects modified bytes even when schema remains valid",async()=>{
 const {bytes}=encode(fixture());
 await assert.rejects(parseOfflineFixture(bytes),/empreinte SHA-256/);
});
test("refuses truncated fixture, no invented objects",async()=>{
 const f=fixture();f.features.pop();
 const {bytes,sha256}=encode(f);
 await assert.rejects(parseOfflineFixture(bytes,sha256),/cardinalité/);
});
test("refuses duplicate identifiers",async()=>{
 const f=fixture();f.features[1].properties.object_id=1;
 const {bytes,sha256}=encode(f);
 await assert.rejects(parseOfflineFixture(bytes,sha256),/dupliqué/);
});
test("refuses unexpected attributes such as vacancy",async()=>{
 const f=fixture();f.features[1].properties.vacancy=1;
 const {bytes,sha256}=encode(f);
 await assert.rejects(parseOfflineFixture(bytes,sha256),/champs non autorisés/);
});
test("refuses invalid geometry",async()=>{
 const f=fixture();f.features[0].geometry={type:"Polygon",coordinates:[[[0,0],[1,0],[1,1],[0,0]]]};
 const {bytes,sha256}=encode(f);
 await assert.rejects(parseOfflineFixture(bytes,sha256),/géométrie/);
});
test("refuses unknown period",async()=>{
 const f=fixture();f.features[0].properties.period_code=4;
 const {bytes,sha256}=encode(f);
 await assert.rejects(parseOfflineFixture(bytes,sha256),/période/);
});
test("refuses unexpected origin metadata",async()=>{
 const f=fixture();f.metadata.public_release_allowed=true;
 const {bytes,sha256}=encode(f);
 await assert.rejects(parseOfflineFixture(bytes,sha256),/métadonnées/);
});
test("refuses oversized buffer before parsing",async()=>{
 await assert.rejects(parseOfflineFixture(new ArrayBuffer(250001),FIXTURE_SHA256),/taille/);
});
