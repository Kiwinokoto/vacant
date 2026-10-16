/* Offline-only Apur laboratory. Uses ONLY a locally served, SHA-pinned private fixture. */
import { MAX_FEATURES, periodFor, validGeometry } from "./periods.mjs";

export const FIXTURE_SHA256 = "f3ea9035458c777a0424ab1e68874c20ea49e03ed3616df54157f416ef365340";
export const SOURCE_SHA256 = "f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11";
export const EXPECTED_FEATURES = 150;
export const MAX_FIXTURE_BYTES = 250_000;

function assert(condition, reason) {
  if (!condition) throw new Error("Extrait Apur refusé : " + reason);
}

export async function parseOfflineFixture(bytes, expectedSha = FIXTURE_SHA256) {
  assert(bytes instanceof ArrayBuffer && bytes.byteLength <= MAX_FIXTURE_BYTES && bytes.byteLength > 0,
    "taille incorrecte");
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  const hex = Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, "0")).join("");
  assert(hex === expectedSha, "empreinte SHA-256 incorrecte");
  const raw = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes));
  const meta = raw?.metadata;
  assert(raw?.type === "FeatureCollection" && Array.isArray(raw.features), "format non GeoJSON");
  assert(meta?.research_only === true && meta?.public_release_allowed === false &&
    meta?.not_vacancy_data === true && meta?.source_crs === "EPSG:2154" &&
    meta?.output_crs === "EPSG:4326" && meta?.license === "ODbL-1.0" &&
    meta?.source_archive_sha256 === SOURCE_SHA256 &&
    meta?.scientific_vintage === "not confirmed by Apur", "métadonnées de provenance");
  assert(meta?.matched_source_features === EXPECTED_FEATURES &&
    meta?.included_features === EXPECTED_FEATURES &&
    Object.keys(meta?.excluded || {}).length === 0 &&
    raw.features.length === EXPECTED_FEATURES &&
    raw.features.length <= MAX_FEATURES, "cardinalité ou exclusions inattendues");
  const ids = new Set(), counts = new Map(), features = [];
  for (const item of raw.features) {
    const properties = item?.properties;
    assert(properties && Object.keys(properties).length === 2 &&
      Object.hasOwn(properties, "object_id") && Object.hasOwn(properties, "period_code"),
      "champs non autorisés");
    assert(Number.isSafeInteger(properties.object_id) && !ids.has(properties.object_id),
      "identifiant invalide ou dupliqué");
    ids.add(properties.object_id);
    assert(validGeometry(item.geometry), "géométrie ou coordonnées non conformes");
    const period = periodFor(properties.period_code);
    counts.set(period.code, (counts.get(period.code) || 0) + 1);
    features.push({type:"Feature",properties: {object_id:properties.object_id,
      period_code:period.code},geometry:item.geometry});
  }
  assert(ids.size === EXPECTED_FEATURES, "identifiants manquants");
  return {collection:{type:"FeatureCollection",features},counts:Object.fromEntries(counts),sha256:hex};
}

export async function loadOfflineFixture(fetcher = fetch) {
  // A relative localhost-only URL. Never fall back to ArcGIS or another remote provider.
  const response = await fetcher("./_local/fixture.geojson", {cache:"no-store"});
  if (!response.ok) throw new Error("Extrait privé indisponible (HTTP " + response.status + ")");
  return parseOfflineFixture(await response.arrayBuffer());
}
