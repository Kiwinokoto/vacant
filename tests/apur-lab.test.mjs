import test from "node:test";
import assert from "node:assert/strict";
import {createHash} from "node:crypto";
import {labEnabled,PERIODS,HEIGHT_BANDS,periodStyle,heightStyle,polygonValid,
 parseSnapshot, SOURCE_SHA256} from "../site/apur-lab-contract.mjs";

const polygon={type:"Polygon",coordinates:[[[2.373,48.854],[2.373,48.8545],
 [2.3735,48.8545],[2.3735,48.854],[2.373,48.854]]]};
function sample(){
 return {type:"FeatureCollection",metadata:{
   research_only:true,public_release_allowed:false,not_vacancy_data:true,
   scientific_vintage:"not confirmed by Apur",source_archive_sha256:SOURCE_SHA256,
   output_crs:"EPSG:4326",source_crs:"EPSG:2154",height_field:"h_med",
   height_unit:"m",license:"ODbL-1.0",expected_features:150,included_features:150
 },features:Array.from({length:150},(_,i)=>({type:"Feature",geometry:polygon,
   properties:{object_id:i+1,period_code:i%2?11:3,height_m:i%2?null:14.5}
 }))};
}
function encode(raw){
 const bin=Buffer.from(JSON.stringify(raw));
 return {buffer:bin.buffer.slice(bin.byteOffset,bin.byteOffset+bin.byteLength),
 sha:createHash("sha256").update(bin).digest("hex")};
}
test("public Apur grid is enabled on VACANT, local preview still opt-in",()=>{
 for(const hostname of ["example.com","192.168.0.3"]){
  assert.equal(labEnabled({hostname,search:"?apur_lab=1"}),false);
 }
 assert.equal(labEnabled({hostname:"vacant.kiwinokoto.fr",search:""}),true);
 assert.equal(labEnabled({hostname:"localhost",search:""}),false);
 assert.equal(labEnabled({hostname:"127.0.0.1",search:"?apur_lab=1"}),true);
});
test("periods carry documented Apur classes without inventing year",()=>{
 assert.equal(PERIODS.length,12);
 assert.equal(periodStyle(11).label,"2000–2007");
 assert.equal(periodStyle(null).label,"Non datée");
 assert.throws(()=>periodStyle(4),/période/);
});
test("height scale uses real meters, keeps missing gray and > 200 real",()=>{
 assert.equal(HEIGHT_BANDS.length,6);
 assert.equal(heightStyle(null).label,"Indisponible / incohérente");
 assert.equal(heightStyle(300).label,"60 m et plus");
 assert.equal(heightStyle(12).label,"10 à moins de 20 m");
 assert.throws(()=>heightStyle(-1),/hauteur/);
});
test("geometry only accepts bounded, closed Paris rings",()=>{
 assert.equal(polygonValid(polygon),true);
 assert.equal(polygonValid({type:"Point",coordinates:[2.3,48.8]}),false);
 assert.equal(polygonValid({type:"Polygon",coordinates:[[[0,0],[1,0],[1,1],[0,0]]]}),false);
});
test("valid 150 record fixture retains period and height independently",async()=>{
 const {buffer,sha}=encode(sample());
 const {collection}=await parseSnapshot(buffer,sha);
 assert.equal(collection.features.length,150);
 assert.equal(collection.features[0].properties.height_m,14.5);
 assert.equal(collection.features[1].properties.height_m,null);
});
test("SHA-256 mismatch is fatal",async()=>{
 const {buffer}=encode(sample());
 await assert.rejects(parseSnapshot(buffer,"1".repeat(64)),/SHA-256/);
});
test("truncation is fatal",async()=>{
 const raw=sample();raw.features.pop();
 const {buffer,sha}=encode(raw);
 await assert.rejects(parseSnapshot(buffer,sha),/cardinalité/);
});
test("duplicate object IDs are fatal",async()=>{
 const raw=sample();raw.features[0].properties.object_id=raw.features[1].properties.object_id;
 const {buffer,sha}=encode(raw);
 await assert.rejects(parseSnapshot(buffer,sha),/ID/);
});
test("any vacancy field is forbidden",async()=>{
 const raw=sample();raw.features[0].properties.vacant_count=10;
 const {buffer,sha}=encode(raw);
 await assert.rejects(parseSnapshot(buffer,sha),/attribut/);
});
test("unconfirmed vintage must be visible in metadata",async()=>{
 const raw=sample();raw.metadata.scientific_vintage="2025-02";
 const {buffer,sha}=encode(raw);
 await assert.rejects(parseSnapshot(buffer,sha),/provenance/);
});
test("unexpected wrong unit and source refused",async()=>{
 const raw=sample();raw.metadata.height_unit="floors";
 const {buffer,sha}=encode(raw);
 await assert.rejects(parseSnapshot(buffer,sha),/provenance/);
});
