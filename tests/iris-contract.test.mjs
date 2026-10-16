import {test} from "node:test";
import assert from "node:assert/strict";
import {validateIrisImport, IRIS_GEOGRAPHY} from "../site/iris-contract.mjs";

// Synthetic fixtures ONLY for internal contract tests, never displayed or exported.
const shape={type:"Polygon",coordinates:[[
  [2.374,48.854],[2.376,48.854],[2.376,48.856],[2.374,48.854]
]]};
const point=()=>({type:"Feature",properties:{iris_code:"751110101",housing_count:120.5,vacant_count:12.25},geometry:shape});
const collection=()=>({type:"FeatureCollection",features:[point()]});
const manifest=()=>({
  census_year:2023,geography_year:2025,zone:"Paris",geography:"IRIS",
  metric:"vacant_housing_rp",extracted_at:"2026-10-16",expected_iris_count:1,
  statistics:{url:"https://www.insee.fr/fr/statistiques/9061333",sha256:"a".repeat(64),licence:"Licence Ouverte 2.0"},
  contours:{url:"https://www.data.gouv.fr/datasets/contours-iris-r-2",sha256:"b".repeat(64),licence:"Licence Ouverte 2.0"}
});
test("exact census-to-geography mapping, no artificial year",()=>{
  assert.deepEqual(Object.entries(IRIS_GEOGRAPHY).map(([k,v])=>[Number(k),v]),[[2006,2008],[2011,2013],[2016,2018],[2023,2025]]);
  assert.throws(()=>validateIrisImport(collection(),{...manifest(),census_year:2022}),/mismatch/);
  assert.throws(()=>validateIrisImport(collection(),{...manifest(),geography_year:2024}),/mismatch/);
});
test("explicit provenance, statistical float and separate geometry",()=>{
  const result=validateIrisImport(collection(),manifest(),{forPublication:true});
  assert.equal(result.features.length,1);
  assert.equal(result.features[0].properties.vacancy_percent,10.2);
  assert.equal(result.features[0].properties.source_kind,"recensement_insee_estimation");
  assert.equal(result.features[0].properties.housing_count,120.5);
  assert.equal(result.metadata.quality.declared_count_matches,true);
  assert.ok(!Object.hasOwn(result.features[0].properties,"building_id"));
});
test("missing values stay missing, never become zeros",()=>{
  const c=collection();c.features[0].properties.vacant_count=null;
  const result=validateIrisImport(c,manifest());
  assert.equal(result.features[0].properties.vacancy_percent,null);
  assert.equal(result.features[0].properties.status,"indisponible");
  assert.equal(result.metadata.quality.missing,1);
});
test("fail closed on address fields, duplicates, invalid count and region",()=>{
  const c=collection();c.features[0].properties.building_id="unsafe";
  assert.throws(()=>validateIrisImport(c,manifest()),/prohibited/);
  c.features[0].properties.building_id=undefined;
  assert.throws(()=>validateIrisImport(c,manifest()),/prohibited/);
  delete c.features[0].properties.building_id;
  c.features[0].properties.vacant_count=121;
  assert.throws(()=>validateIrisImport(c,manifest()),/numerator/);
  c.features[0].properties.vacant_count=12;
  c.features.push(point());
  assert.throws(()=>validateIrisImport(c,manifest()),/duplicate/);
  c.features.pop();
  c.features[0].properties.iris_code="130010101";
  assert.throws(()=>validateIrisImport(c,manifest()),/Paris IRIS/);
  c.features[0].properties.iris_code="751990101";
  assert.throws(()=>validateIrisImport(c,manifest()),/Paris IRIS/);
});
test("official IGN geoplateforme contours URL accepted with full provenance",()=>{
  const m=manifest();
  m.contours.url="https://data.geopf.fr/telechargement/download/CONTOURS-IRIS/CONTOURS-IRIS_3-0__GEOPARQUET_WGS84G_FRA_2025-01-01/contours_iris.parquet";
  const result=validateIrisImport(collection(),m,{forPublication:true});
  assert.equal(result.metadata.contours.url,m.contours.url);
});
test("strict coverage and audited sources required for output",()=>{
  const m=manifest();delete m.expected_iris_count;
  assert.throws(()=>validateIrisImport(collection(),m,{forPublication:true}),/declared expected IRIS count/);
  const p=manifest();p.expected_iris_count=2;
  assert.throws(()=>validateIrisImport(collection(),p),/incomplete/);
  const q=manifest();q.statistics.sha256="";
  assert.throws(()=>validateIrisImport(collection(),q),/statistics source/);
});

test("historical candidate can be inspected privately but never published prematurely",()=>{
  const m={...manifest(),census_year:2011,geography_year:2013};
  const inspected=validateIrisImport(collection(),m);
  assert.equal(inspected.features[0].properties.census_year,2011);
  assert.throws(()=>validateIrisImport(collection(),m,{forPublication:true}),
    /historical IRIS publication blocked/);
});
