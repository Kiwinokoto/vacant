import test from "node:test";
import assert from "node:assert/strict";
import {createHash} from "node:crypto";
import {validateManifest,loadLocalManifest,loadVisibleGrid,SOURCE_SHA256} from "../site/apur-grid-client.mjs";
import {labEnabled} from "../site/apur-lab-contract.mjs";

const poly={type:"Polygon",coordinates:[[[2.374,48.854],[2.375,48.854],[2.375,48.855],[2.374,48.855],[2.374,48.854]]]};
function encode(x){const b=Buffer.from(JSON.stringify(x));return {b:b.buffer.slice(b.byteOffset,b.byteOffset+b.length),hash:createHash("sha256").update(b).digest("hex")};}
function source(){
 const tile=encode({type:"FeatureCollection",features:[{type:"Feature",geometry:poly,
  properties:{object_id:20001,period_code:11,height_m:18.5}}]});
 const data={research_only:false,public_release_allowed:true,contains_vacancy_data:false,
  source_archive_sha256:SOURCE_SHA256,source_crs:"EPSG:2154",output_crs:"EPSG:4326",
  license:"ODbL-1.0",license_uri:"https://opendatacommons.org/licenses/odbl/1-0/",
  source_attribution:"© Atelier parisien d'urbanisme (Apur)",
  scientific_vintage:"not confirmed by Apur",grid_cell_m:500,source_count:128206,
  unique_features:128089,cell_count:1,cells:{"1308,13723":{file:"cell_1308_13723.geojson",
   count:1,bytes:tile.b.byteLength,sha256:tile.hash,bbox_wgs84:[2.37,48.85,2.38,48.86]}}};
 return {data,tile,manifest:encode(data)};
}
test("public host enables Apur view; local lab still requires opt-in",()=>{
 assert.equal(labEnabled({hostname:"vacant.kiwinokoto.fr",search:""}),true);
 assert.equal(labEnabled({hostname:"localhost",search:""}),false);
});
test("public database contract requires ODbL attribution",()=>{
 const {data}=source();assert.equal(validateManifest(data),data);
 assert.throws(()=>validateManifest({...data,license_uri:"https://example.com/"}),/provenance/);
 assert.throws(()=>validateManifest({...data,source_attribution:""}),/provenance/);
});
test("publication manifest SHA pin and cells are validated unchanged",async()=>{
 const {manifest,tile}=source(),seen=[];
 const pub=await loadLocalManifest(manifest.hash,async url=>{seen.push(url);return {ok:true,arrayBuffer:async()=>manifest.b}},"./data/apur-grid/");
 assert.equal(pub.public_release_allowed,true);
 const result=await loadVisibleGrid(pub,[2.371,48.851,2.376,48.856],async url=>{
  seen.push(url);return {ok:true,arrayBuffer:async()=>tile.b};},"./data/apur-grid/");
 assert.equal(result.uniqueObjects,1);
 assert.deepEqual(seen,["./data/apur-grid/manifest.json","./data/apur-grid/cell_1308_13723.geojson"]);
});
test("tampered public manifest is rejected",async()=>{
 const {manifest}=source();
 await assert.rejects(loadLocalManifest("0".repeat(64),async()=>({ok:true,arrayBuffer:async()=>manifest.b}),
  "./data/apur-grid/"),/SHA-256/);
});
