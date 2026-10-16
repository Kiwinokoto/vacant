import test from "node:test";
import assert from "node:assert/strict";
import {createHash} from "node:crypto";
import {loadLocalManifest,loadVisibleGrid,validateManifest} from "../site/apur-grid-client.mjs";
import {labEnabled} from "../site/apur-lab-contract.mjs";

const source="f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11";
const polygon={type:"Polygon",coordinates:[[[2.373,48.854],[2.374,48.854],[2.374,48.855],[2.373,48.855],[2.373,48.854]]]};
const encode=x=>{const b=Buffer.from(JSON.stringify(x));return {
  raw:b.buffer.slice(b.byteOffset,b.byteOffset+b.length),
  sha:createHash("sha256").update(b).digest("hex")
}};
function fixture(){
  const a=encode({type:"FeatureCollection",features:[1,2].map(id=>({type:"Feature",geometry:polygon,properties:{object_id:id,period_code:11,height_m:15}}))});
  const manifest=validateManifest({research_only:true,public_release_allowed:false,
    contains_vacancy_data:false,source_archive_sha256:source,source_crs:"EPSG:2154",
    output_crs:"EPSG:4326",license:"ODbL-1.0",scientific_vintage:"not confirmed by Apur",
    grid_cell_m:500,source_count:128206,unique_features:128089,cell_count:1,cells:{
      "1308,13723":{file:"cell_1308_13723.geojson",count:2,bytes:a.raw.byteLength,
        sha256:a.sha,bbox_wgs84:[2.37,48.85,2.38,48.86]}
    }});
  const m=encode(manifest);
  return {manifest,m,a};
}
test("site gate rejects public hosts even with query parameter",()=>{
  assert.equal(labEnabled({hostname:"vacant.kiwinokoto.fr",search:"?apur_lab=1"}),false);
  assert.equal(labEnabled({hostname:"127.0.0.1",search:"?apur_lab=1"}),true);
});
test("site uses private, pinned manifest without contacting an API",async()=>{
  const {m}=fixture(),urls=[];
  const fetcher=async url=>{urls.push(url);return {ok:true,arrayBuffer:async()=>m.raw}};
  const result=await loadLocalManifest(m.sha,fetcher,"./data/apur-grid/");
  assert.equal(result.cell_count,1);
  assert.deepEqual(urls,["./data/apur-grid/manifest.json"]);
});
test("site grid loads validated cells and counts unique objects",async()=>{
  const {manifest,a}=fixture(),urls=[];
  const fetcher=async url=>{urls.push(url);return {ok:true,arrayBuffer:async()=>a.raw}};
  const result=await loadVisibleGrid(manifest,[2.371,48.851,2.376,48.857],fetcher,"./data/apur-grid/");
  assert.deepEqual(urls,["./data/apur-grid/cell_1308_13723.geojson"]);
  assert.equal(result.uniqueObjects,2);
  assert.equal(result.collection.features[0].properties.height_m,15);
});
test("external URLs are refused before any fetch",async()=>{
  const {manifest,m}=fixture();
  let requests=0;
  const fn=async()=>{requests++;throw Error("no");};
  await assert.rejects(loadLocalManifest(m.sha,fn,"https://opendata.apur.org/"),/chemin/);
  await assert.rejects(loadVisibleGrid(manifest,[2.371,48.851,2.376,48.857],fn,"../secrets/"),/chemin/);
  assert.equal(requests,0);
});
test("missing or corrupted cell fails without returning partial data",async()=>{
  const {manifest,a}=fixture();
  const missing=async()=>({ok:false,status:404});
  await assert.rejects(loadVisibleGrid(manifest,[2.371,48.851,2.376,48.857],missing,"./data/apur-grid/"),/HTTP 404/);
  const bad=async()=>({ok:true,arrayBuffer:async()=>new ArrayBuffer(a.raw.byteLength)});
  await assert.rejects(loadVisibleGrid(manifest,[2.371,48.851,2.376,48.857],bad,"./data/apur-grid/"),/SHA-256/);
});
