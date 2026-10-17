import test from "node:test";
import assert from "node:assert/strict";
import {createHash} from "node:crypto";
import {validateManifest,selectCells,verifiedJson,loadVisibleGrid,SOURCE_SHA256}
  from "../experiments/apur-grid/grid-client.mjs";

function encode(data){
  const buffer=Buffer.from(JSON.stringify(data));
  return {buffer:buffer.buffer.slice(buffer.byteOffset,buffer.byteOffset+buffer.length),
          sha:createHash("sha256").update(buffer).digest("hex")};
}
const poly={type:"Polygon",coordinates:[[
  [2.373,48.854],[2.374,48.854],[2.374,48.855],[2.373,48.855],[2.373,48.854]
]]};
const feature=(id)=>({type:"Feature",properties:{
  object_id:id,period_code:3,height_m:id===2?null:15
},geometry:poly});
const CELL_A={type:"FeatureCollection",features:[feature(1),feature(2)]};
const CELL_B={type:"FeatureCollection",features:[feature(2),feature(3)]};
function fixture(){
  const a=encode(CELL_A),b=encode(CELL_B);
  const cells={
    "1308,13723":{file:"cell_1308_13723.geojson",bbox_wgs84:[2.37,48.85,2.38,48.86],
      count:2,bytes:a.buffer.byteLength,sha256:a.sha},
    "1309,13723":{file:"cell_1309_13723.geojson",bbox_wgs84:[2.375,48.85,2.385,48.86],
      count:2,bytes:b.buffer.byteLength,sha256:b.sha}
  };
  const manifest={research_only:true,public_release_allowed:false,contains_vacancy_data:false,
    source_archive_sha256:SOURCE_SHA256,source_crs:"EPSG:2154",output_crs:"EPSG:4326",
    license:"ODbL-1.0",scientific_vintage:"not confirmed by Apur",grid_cell_m:500,
    source_count:128206,unique_features:128089,cell_count:2,cells};
  const fetcher=async url=>{
    const isA=url.includes("1308_13723"),src=isA?a.buffer:b.buffer;
    return {ok:true,arrayBuffer:async()=>src};
  };
  return {manifest,fetcher};
}
test("source hash has fixed provenance",()=>{
  assert.match(SOURCE_SHA256,/^[a-f0-9]{64}$/);
});
test("reject public or non-ODbL manifest",()=>{
  const {manifest}=fixture();
  assert.equal(validateManifest(manifest),manifest);
  assert.throws(()=>validateManifest({...manifest,public_release_allowed:true}),/provenance/);
  assert.throws(()=>validateManifest({...manifest,license:"unknown"}),/provenance/);
});
test("reject hostile filename",()=>{
  const {manifest}=fixture();
  manifest.cells["1308,13723"].file="../../api/data.json";
  assert.throws(()=>validateManifest(manifest),/cellule/);
});
test("select only geographically relevant cells",()=>{
  const {manifest}=fixture();
  const {selected,expectedPlacements}=selectCells(manifest,[2.371,48.852,2.374,48.856]);
  assert.equal(selected.length,1);
  assert.equal(expectedPlacements,2);
});
test("overlap deduplicated by source OBJECTID, not assumed separate buildings",async()=>{
  const {manifest,fetcher}=fixture();
  const result=await loadVisibleGrid(manifest,[2.371,48.853,2.379,48.858],fetcher);
  assert.equal(result.cellsLoaded,2);
  assert.equal(result.placements,4);
  assert.equal(result.uniqueObjects,3);
  assert.deepEqual(result.collection.features.map(f=>f.properties.object_id),[1,2,3]);
});
test("bad SHA fails with no partial return",async()=>{
  const {manifest,fetcher}=fixture();
  manifest.cells["1309,13723"].sha256="0".repeat(64);
  await assert.rejects(loadVisibleGrid(manifest,[2.37,48.853,2.38,48.858],fetcher),
    /SHA-256/);
});
test("HTTP errors propagate without substituting geometry",async()=>{
  const {manifest}=fixture();
  const fail=async()=>({ok:false,status:404});
  await assert.rejects(loadVisibleGrid(manifest,[2.37,48.853,2.38,48.858],fail),/HTTP 404/);
});
test("too many cells are refused before any request",async()=>{
  const {manifest}=fixture();
  const a=manifest.cells["1308,13723"];
  manifest.cells={};
  for(let i=0;i<13;i++){
    manifest.cells[(1300+i)+",13723"]={
      ...a,file:"cell_"+(1300+i)+"_13723.geojson",
      bbox_wgs84:[2.37,48.85,2.38,48.86]
    };
  }
  let called=false;
  await assert.rejects(loadVisibleGrid(manifest,[2.371,48.853,2.379,48.858],
    async()=>{called=true;throw Error("unexpected call")}),/zone trop large/);
  assert.equal(called,false);
});
test("altered payload fields and invalid geometry are rejected",async()=>{
  const {manifest}=fixture();
  const altered=structuredClone(CELL_A);altered.features[0].properties.vacant=true;
  const e=encode(altered);manifest.cells["1308,13723"].sha256=e.sha;
  manifest.cells["1308,13723"].bytes=e.buffer.byteLength;
  const fetcher=async()=>({ok:true,arrayBuffer:async()=>e.buffer});
  await assert.rejects(loadVisibleGrid(manifest,[2.371,48.853,2.374,48.858],fetcher),
    /attribut/);
});
test("small buffer hash validated",async()=>{
  const e=encode({hello:"world"});
  assert.deepEqual(await verifiedJson(e.buffer,e.sha,1000),{hello:"world"});
  await assert.rejects(verifiedJson(e.buffer,"1".repeat(64),1000),/SHA-256/);
});
