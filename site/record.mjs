// Contract for Paris Data Volumes bâtis, 2026-10 review.
// A "volume" is NOT a whole building. H_ET_MAX is storeys, not metres.
export const SOURCE = Object.freeze({
  id: "paris-volumesbatisparis",
  name: "Ville de Paris — Volumes bâtis",
  url: "https://opendata.paris.fr/explore/dataset/volumesbatisparis/",
  api: "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/volumesbatisparis/records",
  licence: "ODbL",
  kind: "contemporary-survey"
});

const MIN_LON = 2.19;
const MAX_LON = 2.50;
const MIN_LAT = 48.78;
const MAX_LAT = 48.93;

// Broad *sanity* envelope, NOT the administrative perimeter of Paris.
export function isParisCoordinate(point) {
  return Array.isArray(point) && point.length >= 2 &&
    Number.isFinite(point[0]) && Number.isFinite(point[1]) &&
    point[0] >= MIN_LON && point[0] <= MAX_LON &&
    point[1] >= MIN_LAT && point[1] <= MAX_LAT;
}

function isRing(ring) {
  if (!Array.isArray(ring) || ring.length < 4 || !ring.every(isParisCoordinate)) return false;
  const first = ring[0], last = ring[ring.length - 1];
  if (first[0] !== last[0] || first[1] !== last[1]) return false;
  // Structural screen only; GEOS validation of topology remains required for bulk imports.
  const distinct = new Set(ring.slice(0, -1).map(point => point[0] + "," + point[1]));
  if (distinct.size < 3) return false;
  let twiceArea = 0;
  for (let i = 0; i < ring.length - 1; i++) {
    twiceArea += ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1];
  }
  return Math.abs(twiceArea) > 1e-12;
}

export function isParisPolygon(geometry) {
  if (!geometry || typeof geometry !== "object") return false;
  if (geometry.type === "Polygon") {
    return Array.isArray(geometry.coordinates) &&
      geometry.coordinates.length > 0 &&
      geometry.coordinates.every(isRing);
  }
  if (geometry.type === "MultiPolygon") {
    return Array.isArray(geometry.coordinates) && geometry.coordinates.length > 0 &&
      geometry.coordinates.every(polygon =>
        Array.isArray(polygon) && polygon.length > 0 && polygon.every(isRing));
  }
  return false;
}

export function normalizeRecord(record) {
  if (!record || !isParisPolygon(record.geom)) {
    throw new Error("invalid or out-of-Paris polygon");
  }
  const id = record.n_sq_vb;
  const arrondissement = Number(record.n_ar);
  if (id === null || id === undefined || String(id).trim() === "" ||
      !Number.isInteger(arrondissement) || arrondissement < 1 || arrondissement > 20) {
    throw new Error("invalid identifier or arrondissement");
  }
  const rawFloors = record.h_et_max;
  let floors = null;
  if (rawFloors !== null && rawFloors !== undefined && rawFloors !== "") {
    const parsed = Number(rawFloors);
    if (Number.isFinite(parsed) && parsed >= 0 && parsed <= 100) floors = parsed;
  }
  return {
    type: "Feature",
    id: String(id),
    geometry: record.geom,
    properties: {
      volume_id: String(id),
      arrondissement,
      floors_max: floors,
      floor_description: typeof record.l_plan_h === "string" ? record.l_plan_h : null,
      // This dataset has no audited corresponding evidence for these properties.
      height_m: null,
      construction_period: null,
      vacant_housing: null,
      source_id: SOURCE.id,
      source_url: SOURCE.url,
      licence: SOURCE.licence,
      evidence: "référentiel actuel / non historique"
    }
  };
}

export function normalizeBatch(records) {
  if (!Array.isArray(records)) throw new Error("expected record array");
  const seen = new Set(), features = [];
  let rejected = 0, duplicates = 0;
  for (const record of records) {
    try {
      const feature = normalizeRecord(record);
      if (seen.has(feature.id)) { duplicates++; continue; }
      seen.add(feature.id);
      features.push(feature);
    } catch (_) { rejected++; }
  }
  return {
    collection: { type: "FeatureCollection", features },
    rejected,
    duplicates
  };
}
