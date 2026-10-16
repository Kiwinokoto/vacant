import { test } from "node:test";
import assert from "node:assert/strict";
import { isParisPolygon, normalizeRecord, normalizeBatch } from "../site/record.mjs";

// Synthetic contract-only fixtures: NEVER part of the public map.
const ring = [
  [2.375, 48.854], [2.3752, 48.854],
  [2.3752, 48.8542], [2.375, 48.854]
];
const valid = () => ({
  n_sq_vb: 777,
  n_ar: 11,
  h_et_max: 4,
  l_plan_h: "R+4",
  d_cre: "1899-09-01",
  d_maj: "2010-07-21",
  geom: {type: "Polygon", coordinates: [ring]}
});

test("valid contemporary polygon with explicit unknowns", () => {
  const feature = normalizeRecord(valid());
  assert.equal(feature.type, "Feature");
  assert.equal(feature.properties.floors_max, 4);
  assert.equal(feature.properties.height_m, null);
  assert.equal(feature.properties.construction_period, null);
  assert.equal(feature.properties.vacant_housing, null);
  assert.equal(feature.properties.source_id, "paris-volumesbatisparis");
  assert.equal(feature.properties.licence, "ODbL");
  assert.ok(!Object.hasOwn(feature.properties, "d_cre"));
});
test("geometry rejects wrong coordinate order and open rings", () => {
  assert.equal(isParisPolygon({type: "Polygon", coordinates: [
    [[48.854, 2.375], [48.855, 2.375], [48.855, 2.376], [48.854, 2.375]]
  ]}), false);
  assert.equal(isParisPolygon({type: "Polygon", coordinates: [
    [[2.375, 48.854], [2.376, 48.854], [2.376, 48.855], [2.375, 48.855]]
  ]}), false);
});
test("accepts valid multipolygon and rejects degenerate/no geometry", () => {
  assert.equal(isParisPolygon({type:"MultiPolygon",coordinates:[[ring]]}), true);
  assert.equal(isParisPolygon({type:"Polygon",coordinates:[[ring[0],ring[0],ring[0],ring[0]]]}),false);
  assert.equal(isParisPolygon({type:"Polygon", coordinates:[]}), false);
  assert.throws(() => normalizeRecord({n_sq_vb:4, n_ar:11}), /polygon/);
});
test("invalid arrondissement and unknown storeys never fabricated", () => {
  assert.throws(() => normalizeRecord({...valid(), n_ar:0}), /arrondissement/);
  const feature = normalizeRecord({...valid(), h_et_max: "", l_plan_h: null});
  assert.equal(feature.properties.floors_max, null);
  assert.equal(feature.properties.height_m, null);
});
test("deduplicates volume ids, reports bad geometry", () => {
  const invalid = {...valid(), n_sq_vb:999, geom:null};
  const result = normalizeBatch([valid(), valid(), invalid]);
  assert.equal(result.collection.features.length, 1);
  assert.equal(result.duplicates, 1);
  assert.equal(result.rejected, 1);
});
