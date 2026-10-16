/* VACANT | Apur period experiment: bounded, read-only, no persisted geometry. */
export const LAYER_URL = "https://carto2.apur.org/apur/rest/services/OPENDATA/EMPRISE_BATIE_PARIS/MapServer/0/query";
export const DOCUMENTATION_URL = "https://www.apur.org/open_data/EMPRISE_BATIE_OD.pdf";
export const MAX_FEATURES = 200;
export const MAX_RESPONSE_BYTES = 1_000_000;
export const PERIODS = Object.freeze([
  { code: 1, label: "Avant 1800", color: "#65583d" },
  { code: 2, label: "1801–1850", color: "#a48e48" },
  { code: 3, label: "1851–1914", color: "#c7a44f" },
  { code: 5, label: "1915–1939", color: "#d58753" },
  { code: 6, label: "1940–1967", color: "#d56d53" },
  { code: 7, label: "1968–1975", color: "#c55567" },
  { code: 8, label: "1976–1981", color: "#ad6687" },
  { code: 9, label: "1982–1989", color: "#917aab" },
  { code: 10, label: "1990–1999", color: "#7193bc" },
  { code: 11, label: "2000–2007", color: "#5eacb3" },
  { code: 12, label: "2008 et après", color: "#4c9d79" },
  { code: 99, label: "Non datée", color: "#9ba5aa" }
]);
const periodByCode = new Map(PERIODS.map(p => [p.code, p]));
export function periodFor(code) {
  if (code === null || code === undefined || code === 99) return periodByCode.get(99);
  if (!Number.isInteger(code) || !periodByCode.has(code)) {
    throw new Error("Code de période Apur inattendu : " + String(code));
  }
  return periodByCode.get(code);
}
export function makeQuery(bounds, countOnly = false) {
  const { west, south, east, north } = bounds;
  if (![west, south, east, north].every(Number.isFinite) ||
      west >= east || south >= north ||
      east - west > 0.006 || north - south > 0.004 ||
      west < 2.15 || east > 2.51 || south < 48.75 || north > 49.0) {
    throw new Error("Zone trop étendue ou hors Paris : rapprochez le zoom (quartier seulement).");
  }
  const geometry = JSON.stringify({
    xmin: west, ymin: south, xmax: east, ymax: north,
    spatialReference: { wkid: 4326 }
  });
  const options = {
    f: countOnly ? "json" : "geojson",
    where: "1=1",
    geometry,
    geometryType: "esriGeometryEnvelope",
    inSR: "4326",
    spatialRel: "esriSpatialRelIntersects"
  };
  if (countOnly) options.returnCountOnly = "true";
  else Object.assign(options, {
    outFields: "OBJECTID,n_sq_eb,c_perconst",
    outSR: "4326", returnGeometry: "true",
    orderByFields: "OBJECTID", resultOffset: "0",
    resultRecordCount: String(MAX_FEATURES)
  });
  return LAYER_URL + "?" + new URLSearchParams(options).toString();
}
function validRing(ring) {
  if (!Array.isArray(ring) || ring.length < 4 || ring.length > 3000) return false;
  for (const point of ring) {
    if (!Array.isArray(point) || point.length < 2 ||
        !Number.isFinite(point[0]) || !Number.isFinite(point[1]) ||
        point[0] < 2.15 || point[0] > 2.51 ||
        point[1] < 48.75 || point[1] > 49.0) return false;
  }
  const a = ring[0], b = ring[ring.length - 1];
  return a[0] === b[0] && a[1] === b[1];
}
export function validGeometry(geometry) {
  if (!geometry || !["Polygon", "MultiPolygon"].includes(geometry.type)) return false;
  const polygons = geometry.type === "Polygon" ? [geometry.coordinates] : geometry.coordinates;
  if (!Array.isArray(polygons) || !polygons.length || polygons.length > 40) return false;
  return polygons.every(rings =>
    Array.isArray(rings) && rings.length > 0 && rings.length <= 30 &&
    rings.every(validRing));
}
export function sanitizeCollection(raw, expectedCount) {
  if (!raw || raw.type !== "FeatureCollection" || !Array.isArray(raw.features) ||
      !Number.isInteger(expectedCount) || expectedCount < 0 || expectedCount > MAX_FEATURES ||
      raw.features.length !== expectedCount || raw.exceededTransferLimit === true) {
    throw new Error("Pagination ou cardinalité Apur incohérente ; aucune couche partielle affichée.");
  }
  const seen = new Set(), counts = new Map(), features = [];
  for (const feature of raw.features) {
    const p = feature && feature.properties;
    if (!p || !Number.isSafeInteger(p.OBJECTID) || seen.has(p.OBJECTID) ||
        !validGeometry(feature.geometry)) {
      throw new Error("Identifiant ou géométrie Apur invalide ; affichage refusé.");
    }
    seen.add(p.OBJECTID);
    const period = periodFor(p.c_perconst);
    const key = period.code;
    counts.set(key, (counts.get(key) || 0) + 1);
    // Whitelist only: no address, Paris Data volume or vacancy attributes.
    features.push({
      type: "Feature",
      geometry: feature.geometry,
      properties: { object_id: p.OBJECTID, period_code: key }
    });
  }
  return {
    collection: { type: "FeatureCollection", features },
    counts: Object.fromEntries(counts)
  };
}
async function responseJson(fetcher, url) {
  const response = await fetcher(url, { headers: { Accept: "application/json" }, cache: "no-store" });
  if (!response.ok) throw new Error("Service Apur HTTP " + response.status);
  const text = await response.text();
  if (new TextEncoder().encode(text).byteLength > MAX_RESPONSE_BYTES) {
    throw new Error("Réponse Apur trop volumineuse.");
  }
  const parsed = JSON.parse(text);
  if (!parsed || typeof parsed !== "object" || parsed.error) {
    throw new Error("Réponse d'API Apur invalide.");
  }
  return parsed;
}
export async function fetchBoundedPeriodLayer(bounds, fetcher = fetch) {
  const countPayload = await responseJson(fetcher, makeQuery(bounds, true));
  const count = countPayload.count;
  if (!Number.isInteger(count) || count < 0) {
    throw new Error("Nombre d'emprises non fiable.");
  }
  if (count > MAX_FEATURES) {
    throw new Error(count + " emprises dans cette zone (plafond " +
      MAX_FEATURES + "). Zoomez davantage, aucune couche partielle affichée.");
  }
  if (count === 0) return sanitizeCollection({ type: "FeatureCollection", features: [] }, 0);
  const geojson = await responseJson(fetcher, makeQuery(bounds, false));
  return sanitizeCollection(geojson, count);
}
