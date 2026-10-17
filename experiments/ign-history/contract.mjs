/* Historical building comparison: private, offline research only. */
export const YEARS=Object.freeze(["2011-04-12","2018-03-29"]);
const TYPES=new Set(["INDIFFERENCIE","INDUSTRIEL","REMARQUABLE"]);
export function enabled(loc){
 return ["localhost","127.0.0.1","[::1]"].includes(loc.hostname) &&
   new URLSearchParams(loc.search).get("ign_lab")==="1";
}
function validRing(r){
 return Array.isArray(r)&&r.length>=4&&r.length<=30000&&
  r.every(p=>Array.isArray(p)&&p.length>=2&&
   Number.isFinite(p[0])&&Number.isFinite(p[1])&&
   p[0]>2.1&&p[0]<2.55&&p[1]>48.7&&p[1]<49.05) &&
  r[0][0]===r.at(-1)[0]&&r[0][1]===r.at(-1)[1];
}
export function parseSnapshot(raw,edition) {
 if(!YEARS.includes(edition) || raw?.type!=="FeatureCollection" ||
    !Array.isArray(raw.features) || raw.features.length>2000 ||
    raw.metadata?.private_research_only!==true ||
    raw.metadata?.not_a_historical_presence_assertion!==true ||
    raw.metadata?.edition!==edition ||
    raw.metadata?.source_crs!=="EPSG:2154" ||
    raw.metadata?.output_crs!=="EPSG:4326"){
  throw new Error("Source privée IGN : provenance ou géographie incorrecte");
 }
 const ids=new Set();
 for(const f of raw.features){
  const p=f?.properties,g=f?.geometry;
  if(f?.type!=="Feature"||!TYPES.has(p?.kind)||
    typeof p?.feature_id!=="string"||!/^BATIMENT[0-9]{10,25}$/.test(p.feature_id)||
    p.date_edition!==edition ||
    (p.height_raw!==null &&
      (typeof p.height_raw!=="number"||!Number.isFinite(p.height_raw)||p.height_raw<0))||
    !g||!(g.type==="Polygon"||g.type==="MultiPolygon")){
   throw new Error("IGN : attribut ou géométrie inconnu");
  }
  const polys=g.type==="Polygon"?[g.coordinates]:g.coordinates;
  if(!Array.isArray(polys)||!polys.length||polys.length>100||
    !polys.every(polygon=>Array.isArray(polygon)&&polygon.length>0&&polygon.length<=100&&polygon.every(validRing)))
   throw new Error("IGN : anneau invalide");
  if(ids.has(p.feature_id))throw new Error("IGN : ID dupliqué");
  ids.add(p.feature_id);
 }
 return raw;
}
export function compareIds(a,b){
 const x=new Set(a.features.map(f=>f.properties.feature_id));
 const y=new Set(b.features.map(f=>f.properties.feature_id));
 let shared=0;for(const id of x)if(y.has(id))shared++;
 return {first:x.size,second:y.size,shared,
   onlyFirst:x.size-shared,onlySecond:y.size-shared,
   warning:"ID absent d'une édition ≠ preuve de démolition/construction"};
}
