import test from "node:test";
import assert from "node:assert/strict";
import { PERIODS, MAX_FEATURES, periodFor, makeQuery, validGeometry, sanitizeCollection, fetchBoundedPeriodLayer } from "../experiments/apur-periods/periods.mjs";
const bounds = {west:2.373,south:48.854,east:2.376,north:48.856};
const geometry = {type:"Polygon",coordinates:[[[2.373,48.854],[2.374,48.854],[2.374,48.855],[2.373,48.855],[2.373,48.854]]]};
const feature = (id, code=3, geom=geometry) => ({type:"Feature",properties:{OBJECTID:id,n_sq_eb:1000+id,c_perconst:code,address:"should be dropped",vacancy:42},geometry:geom});
test("nomenclature Apur 2019: 11 périodes distinctes + 99",()=>{
  assert.equal(PERIODS.length,12);
  assert.equal(periodFor(11).label,"2000–2007");
  assert.equal(periodFor(null).code,99);
  assert.throws(()=>periodFor(4),/inattendu/);
});
test("query rejects enlarged, inverted and distant envelopes",()=>{
  assert.throws(()=>makeQuery({...bounds,east:2.38}),/Zone/);
  assert.throws(()=>makeQuery({...bounds,west:2.39}),/Zone/);
  assert.throws(()=>makeQuery({...bounds,south:40,north:40.001}),/Zone/);
  const u=new URL(makeQuery(bounds,false));
  assert.equal(u.searchParams.get("outFields"),"OBJECTID,n_sq_eb,c_perconst");
  assert.equal(u.searchParams.get("resultRecordCount"),String(MAX_FEATURES));
  assert.equal(u.searchParams.get("f"),"geojson");
  assert.equal(new URL(makeQuery(bounds,true)).searchParams.get("returnCountOnly"),"true");
});
test("geometry validation rejects open ring and non-Paris coordinates",()=>{
  assert.ok(validGeometry(geometry));
  assert.ok(!validGeometry({type:"Polygon",coordinates:[[[2.373,48.854],[2.374,48.854],[2.374,48.855],[2.373,48.855]]]}));
  assert.ok(!validGeometry({type:"Polygon",coordinates:[[[0,0],[1,0],[1,1],[0,0]]]}));
  assert.ok(!validGeometry(null));
});
test("sanitization removes unexpected attributes and excludes vacancy",()=>{
  const result=sanitizeCollection({type:"FeatureCollection",features:[feature(1,11)]},1);
  assert.deepEqual(result.collection.features[0].properties,{object_id:1,period_code:11});
  assert.equal(result.counts["11"],1);
  assert.ok(!JSON.stringify(result).includes("vacancy"));
});
test("reject duplicate ids and unexpected category",()=>{
  assert.throws(()=>sanitizeCollection({type:"FeatureCollection",features:[feature(1),feature(1)]},2),/invalide/);
  assert.throws(()=>sanitizeCollection({type:"FeatureCollection",features:[feature(1,4)]},1),/inattendu/);
});
test("reject truncated GeoJSON or mismatched count",()=>{
  assert.throws(()=>sanitizeCollection({type:"FeatureCollection",features:[feature(1)]},2),/cardinalité/);
  assert.throws(()=>sanitizeCollection({type:"FeatureCollection",features:[feature(1)],exceededTransferLimit:true},1),/cardinalité/);
});
test("count cap prevents requesting any geometry",async()=>{
  const requests=[];
  const fetcher=async url=>{requests.push(url);return {ok:true,text:async()=>JSON.stringify({count:MAX_FEATURES+1})};};
  await assert.rejects(fetchBoundedPeriodLayer(bounds,fetcher),/plafond/);
  assert.equal(requests.length,1);
});
test("two step query validates and does not invent empty records",async()=>{
  let n=0;
  const fetcher=async url=>{n++;
    return {ok:true,text:async()=>JSON.stringify(n===1?{count:1}:{type:"FeatureCollection",features:[feature(11,99)]})};
  };
  const result=await fetchBoundedPeriodLayer(bounds,fetcher);
  assert.equal(n,2);
  assert.equal(result.counts["99"],1);
  assert.equal(result.collection.features.length,1);
});
test("empty area is not fetched again",async()=>{
  let n=0;const f=async()=>{n++;return {ok:true,text:async()=>JSON.stringify({count:0})};};
  const r=await fetchBoundedPeriodLayer(bounds,f);
  assert.equal(n,1);assert.equal(r.collection.features.length,0);
});
test("network error is not silently replaced",async()=>{
  const f=async()=>{throw new Error("CORS ou réseau");};
  await assert.rejects(fetchBoundedPeriodLayer(bounds,f),/CORS/);
});
