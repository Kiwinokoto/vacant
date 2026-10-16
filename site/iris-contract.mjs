// STRICT INTERNAL IMPORT CONTRACT. No real IRIS data are bundled yet.
// IRIS polygons represent geographic aggregates, never vacant addresses/buildings.
import { isParisPolygon } from "./record.mjs";

export const IRIS_GEOGRAPHY = Object.freeze({2006:2008, 2011:2013, 2016:2018, 2023:2025});

export function validateIrisImport(collection, manifest, {forPublication=false}={}) {
  if (!manifest || typeof manifest !== "object") throw new Error("missing provenance manifest");
  const year = manifest.census_year;
  const geographyYear = IRIS_GEOGRAPHY[year];
  if (!Number.isInteger(year) || !geographyYear || manifest.geography_year !== geographyYear) {
    throw new Error("census year and IRIS geography year mismatch");
  }
  if (manifest.zone !== "Paris" || manifest.geography !== "IRIS" ||
      manifest.metric !== "vacant_housing_rp") {
    throw new Error("wrong geography, territory or statistic");
  }
  if (typeof manifest.extracted_at !== "string" ||
      !/^\d{4}-\d{2}-\d{2}$/.test(manifest.extracted_at) ||
      !Number.isFinite(Date.parse(manifest.extracted_at+"T00:00:00Z"))) {
    throw new Error("date of extraction required");
  }
  const inputs = [manifest.statistics, manifest.contours];
  const domains = [
    /^https:\/\/(?:www\.insee\.fr|api\.insee\.fr)\//,
    /^https:\/\/(?:(?:www\.)?data\.gouv\.fr|geoservices\.ign\.fr)\//
  ];
  for (let i = 0; i < inputs.length; i++) {
    const input = inputs[i];
    if (!input || typeof input.url !== "string" || !domains[i].test(input.url) ||
        !/^[a-f0-9]{64}$/.test(input.sha256 ?? "") ||
        input.licence !== "Licence Ouverte 2.0") {
      throw new Error("invalid "+(i===0?"statistics":"contours")+" source, licence or SHA-256");
    }
  }
  if (!collection || collection.type !== "FeatureCollection" ||
      !Array.isArray(collection.features) || collection.features.length === 0) {
    throw new Error("empty or invalid GeoJSON collection");
  }

  const seen = new Set();
  const features = [];
  let missing = 0;
  for (const feature of collection.features) {
    const p = feature?.properties;
    if (feature?.type !== "Feature" || !p || typeof p !== "object" ||
        !isParisPolygon(feature.geometry)) throw new Error("invalid IRIS feature/geometry");
    // Paris municipal arrondissement IRIS are nine-character INSEE codes, starting 751.
    const code = p.iris_code;
    if (typeof code !== "string" || !/^751(?:0[1-9]|1\d|20)\d{4}$/.test(code) || seen.has(code)) {
      throw new Error("invalid or duplicate Paris IRIS code");
    }
    seen.add(code);
    // The contract prohibits allocating address-level status into IRIS exports.
    if (["building_id","address","owner","vacant_address","apartment_id","parcel_id"].some(k => Object.hasOwn(p,k))) {
      throw new Error("address/building-level information prohibited");
    }
    if (!Object.hasOwn(p,"housing_count") || !Object.hasOwn(p,"vacant_count")) {
      throw new Error("missing required measure columns");
    }
    const housing = p.housing_count, vacant = p.vacant_count;
    const absent = housing === null || vacant === null;
    if ((housing !== null && (!Number.isFinite(housing) || housing < 0)) ||
        (vacant !== null && (!Number.isFinite(vacant) || vacant < 0)) ||
        (!absent && vacant > housing)) {
      throw new Error("invalid numerator/denominator");
    }
    if (absent) missing++;
    const rate = absent || housing === 0 ? null : Math.round(1000 * vacant / housing) / 10;
    features.push({
      type: "Feature",
      id: code,
      geometry: feature.geometry,
      properties: {
        iris_code: code, census_year: year, geography_year: geographyYear,
        housing_count: housing, vacant_count: vacant,
        vacancy_percent: rate,
        status: absent || housing === 0 ? "indisponible" : "statistique_agregee",
        source_kind: "recensement_insee_estimation",
        // Attribution and both input SHA-256 checksums are in the collection manifest.
      }
    });
  }
  const expected = manifest.expected_iris_count;
  if (expected !== undefined && (!Number.isInteger(expected) || expected < 1 ||
      expected !== seen.size)) throw new Error("incomplete IRIS geographic coverage");
  if (forPublication && expected === undefined) throw new Error("publication requires declared expected IRIS count");
  const quality = {count: features.length, missing, percent_missing:Math.round(missing / features.length * 1000)/10,
    geography_year: geographyYear, census_year: year, declared_count_matches:expected !== undefined};
  return { type:"FeatureCollection", features, metadata:{...manifest, quality} };
}
