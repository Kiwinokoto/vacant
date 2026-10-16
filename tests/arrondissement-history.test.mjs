import { test } from "node:test";
import assert from "node:assert/strict";
import { TIMELINE } from "../site/timeline.mjs";
import { statForYear, validateArrondissementSeries } from "../site/arrondissement-history.mjs";

function dataset() {
  return {
    type: "FeatureCollection",
    metadata: {
      kind: "vacant_housing_arrondissement_estimate",
      years: TIMELINE.map(x=>x.year),
      geometry: "2025 arrondissement display boundary",
    },
    features: Array.from({length:20},(_,i)=>({
      type:"Feature",
      geometry:{type:"Polygon",coordinates:[]},
      properties:{
        arrondissement_code:"751"+String(i+1).padStart(2,"0"),
        series:Object.fromEntries(TIMELINE.map(x=>[
          String(x.year),
          {housing_count:x.total/20,vacant_count:x.vacant/20,
           vacancy_percent:Math.round(1000*x.vacant/x.total)/10}
        ]))
      }
    }))
  };
}

test("validates a complete and consistent four-year arrondissement dataset",()=>{
  assert.doesNotThrow(()=>validateArrondissementSeries(dataset()));
});
test("rejects IRIS-vs-arrondissement confusion",()=>{
  const input=dataset();
  input.features[0].properties.arrondissement_code="751010101";
  assert.throws(()=>validateArrondissementSeries(input),/géométrie|code/);
});
test("rejects invented total, incompatible geography and missing regions",()=>{
  const bad=dataset();
  bad.features[1].properties.series["2006"].vacant_count+=500;
  assert.throws(()=>validateArrondissementSeries(bad),/incohérente|totaux/);
  const fewer=dataset();
  fewer.features.pop();
  assert.throws(()=>validateArrondissementSeries(fewer),/incomplet/);
  const wrong=dataset();
  wrong.metadata.geometry="IRIS 2008 mapped to 2025 boundaries";
  assert.throws(()=>validateArrondissementSeries(wrong),/incomplet/);
});
test("extracts only the explicitly requested census year",()=>{
  const props=dataset().features[0].properties;
  assert.equal(statForYear(props,2011).status,"statistique_agregee");
  assert.equal(statForYear(props,2011).housing_count,TIMELINE[1].total/20);
  assert.equal(statForYear(props,1999),null);
});
