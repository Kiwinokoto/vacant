/* Local research-only Apur grid loader. No remote API or public data publication. */
export const SOURCE_SHA256 = "f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11";
const MAX_MANIFEST_BYTES = 1_000_000;
const MAX_CELLS = 12;
const MAX_TOTAL_TILE_BYTES = 10_000_000;
const MAX_PLACEMENTS = 5000;
const ID_RE = /^cell_[0-9]+_[0-9]+\.geojson$/;

function reject(reason) {
  throw new Error("Grille Apur non chargée : " + reason);
}
export async function verifiedJson(buffer, sha256, maxBytes) {
  if (!(buffer instanceof ArrayBuffer) || !buffer.byteLength ||
      buffer.byteLength > maxBytes || !/^[a-f0-9]{64}$/.test(sha256)) {
    reject("taille ou empreinte manquante");
  }
  const data = await crypto.subtle.digest("SHA-256", buffer);
  const hash = Array.from(new Uint8Array(data), x => x.toString(16).padStart(2,"0")).join("");
  if (hash !== sha256) reject("SHA-256 incorrect");
  return JSON.parse(new TextDecoder("utf-8",{fatal:true}).decode(buffer));
}
function validBBox(b){
  return Array.isArray(b) && b.length === 4 && b.every(Number.isFinite) &&
    b[0] >= 2.1 && b[2] <= 2.55 && b[1] >= 48.7 && b[3] <= 49.05 &&
    b[0] < b[2] && b[1] < b[3];
}
function overlap(a,b){
  return a[0] < b[2] && a[2] > b[0] && a[1] < b[3] && a[3] > b[1];
}
export function validateManifest(raw) {
  if (!raw || raw.research_only !== true || raw.public_release_allowed !== false ||
      raw.contains_vacancy_data !== false || raw.source_archive_sha256 !== SOURCE_SHA256 ||
      raw.source_crs !== "EPSG:2154" || raw.output_crs !== "EPSG:4326" ||
      raw.license !== "ODbL-1.0" || raw.scientific_vintage !== "not confirmed by Apur" ||
      raw.grid_cell_m !== 500 || raw.source_count !== 128206 ||
      !Number.isInteger(raw.unique_features) || raw.unique_features <= 0 ||
      !raw.cells || typeof raw.cells !== "object" || Array.isArray(raw.cells)) {
    reject("manifest privé et provenance incohérents");
  }
  const entries = Object.entries(raw.cells);
  if (!entries.length || entries.length > 3000 || raw.cell_count !== entries.length) {
    reject("nombre de cellules inattendu");
  }
  for (const [key, info] of entries) {
    if (!/^[0-9]+,[0-9]+$/.test(key) || !ID_RE.test(info?.file) ||
        !validBBox(info?.bbox_wgs84) ||
        !Number.isInteger(info.count) || info.count < 1 || info.count > 3000 ||
        !Number.isInteger(info.bytes) || info.bytes < 30 ||
        info.bytes > 5_000_000 || !/^[a-f0-9]{64}$/.test(info.sha256)) {
      reject("cellule malformée");
    }
    const [ix, iy] = key.split(",");
    if (info.file !== "cell_" + ix + "_" + iy + ".geojson") reject("nom de cellule incompatible");
  }
  return raw;
}
export function selectCells(manifest, viewBBox) {
  if (!validBBox(viewBBox)) reject("zone de carte incohérente");
  const selected = Object.entries(manifest.cells).filter(([,cell])=>
    overlap(cell.bbox_wgs84,viewBBox)).map(([key,cell])=>({key,...cell}));
  const bytes = selected.reduce((total,cell)=>total+cell.bytes,0);
  const placements = selected.reduce((total,cell)=>total+cell.count,0);
  if (selected.length > MAX_CELLS || bytes > MAX_TOTAL_TILE_BYTES ||
      placements > MAX_PLACEMENTS) {
    reject("zone trop large, zoomer davantage (plafonds cellules/volume/objets)");
  }
  return {selected, expectedBytes:bytes, expectedPlacements:placements};
}
function ringValid(r){
  if (!Array.isArray(r) || r.length < 4 || r.length > 20000) return false;
  if (!r.every(p=>Array.isArray(p) && p.length>=2 && Number.isFinite(p[0]) &&
    Number.isFinite(p[1]) && p[0]>2.1 && p[0]<2.55 && p[1]>48.7 && p[1]<49.05)) return false;
  return r[0][0]===r.at(-1)[0] && r[0][1]===r.at(-1)[1];
}
function geometryValid(g){
  if (!g || !["Polygon","MultiPolygon"].includes(g.type)) return false;
  const pieces = g.type === "Polygon" ? [g.coordinates] : g.coordinates;
  return Array.isArray(pieces) && pieces.length>0 && pieces.length<=100 &&
    pieces.every(rings=>Array.isArray(rings) && rings.length>0 &&
      rings.length<=100 && rings.every(ringValid));
}
function validateFeature(f){
  const p=f?.properties;
  if (f?.type!=="Feature" || !geometryValid(f.geometry) || !p ||
      Object.keys(p).length!==3 || !Object.hasOwn(p,"object_id") ||
      !Object.hasOwn(p,"period_code") || !Object.hasOwn(p,"height_m") ||
      !Number.isSafeInteger(p.object_id) ||
      ![1,2,3,5,6,7,8,9,10,11,12,99].includes(p.period_code) ||
      !(p.height_m===null || (typeof p.height_m==="number" &&
        Number.isFinite(p.height_m) && p.height_m>0))) {
    reject("attribut ou forme de géométrie inattendu");
  }
}
export async function loadVisibleGrid(manifest, viewBBox, fetcher=fetch) {
  const {selected, expectedBytes, expectedPlacements}=selectCells(manifest,viewBBox);
  const unique = new Map();
  let seen=0;
  for(const cell of selected){
    const response=await fetcher("./_local/"+cell.file,{cache:"no-store"});
    if(!response.ok)reject("HTTP "+response.status+" pour "+cell.file);
    const buffer=await response.arrayBuffer();
    if(buffer.byteLength!==cell.bytes)reject("taille erronée pour "+cell.file);
    const payload=await verifiedJson(buffer,cell.sha256,cell.bytes);
    if(payload?.type!=="FeatureCollection" ||
      !Array.isArray(payload.features) || payload.features.length!==cell.count) {
      reject("cardinalité de cellule inattendue");
    }
    seen+=payload.features.length;
    for(const feature of payload.features){
      validateFeature(feature);
      const oid=feature.properties.object_id;
      const old=unique.get(oid);
      if(old && JSON.stringify(old)!==JSON.stringify(feature)) {
        reject("géométrie conflictuelle entre cellules pour le même OBJECTID");
      }
      if(!old)unique.set(oid,feature);
    }
  }
  if(seen!==expectedPlacements || unique.size>MAX_PLACEMENTS){
    reject("grille tronquée");
  }
  return {collection:{type:"FeatureCollection",features:[...unique.values()]},
    cellsLoaded:selected.length, placements:seen, uniqueObjects:unique.size,
    expectedBytes};
}
export async function loadLocalManifest(pinnedSha,fetcher=fetch){
  const response=await fetcher("./_local/manifest.json",{cache:"no-store"});
  if(!response.ok)reject("manifest HTTP "+response.status);
  return validateManifest(await verifiedJson(await response.arrayBuffer(),
    pinnedSha,MAX_MANIFEST_BYTES));
}
