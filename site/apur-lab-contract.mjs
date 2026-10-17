/* Apur: audited public derivative or localhost laboratory only. No live Apur API. */
export const SOURCE_SHA256="f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11";
export const PERIODS=Object.freeze([
  [1,"Avant 1800","#65583d"],[2,"1801–1850","#a48e48"],
  [3,"1851–1914","#c7a44f"],[5,"1915–1939","#d58753"],
  [6,"1940–1967","#d56d53"],[7,"1968–1975","#c55567"],
  [8,"1976–1981","#ad6687"],[9,"1982–1989","#917aab"],
  [10,"1990–1999","#7193bc"],[11,"2000–2007","#5eacb3"],
  [12,"2008 et après","#4c9d79"],[99,"Non datée","#9ba5aa"]
]);
export const HEIGHT_BANDS=Object.freeze([
  ["Moins de 10 m","#b2dfd0"],["10 à moins de 20 m","#6ebaaa"],
  ["20 à moins de 35 m","#e5c879"],["35 à moins de 60 m","#dd9875"],
  ["60 m et plus","#ad6487"],["Indisponible / incohérente","#95a0aa"]
]);
const periodMap=new Map(PERIODS.map(([id,label,color])=>[id,{label,color}]));
const MAX_BYTES=250000;
const EXPECTED_COUNT=150;
function fail(reason){throw new Error("Données Apur refusées : "+reason);}
export function labEnabled(loc){
  return loc.hostname==="vacant.kiwinokoto.fr" ||
    (["localhost","127.0.0.1","[::1]"].includes(loc.hostname) &&
    new URLSearchParams(loc.search).get("apur_lab")==="1");
}
export function periodStyle(code){
  const value=code == null?99:code;
  const mapped=periodMap.get(value);
  if(!mapped)fail("code de période inconnu");
  return mapped;
}
export function heightStyle(value){
  if(value==null)return {label:HEIGHT_BANDS[5][0],color:HEIGHT_BANDS[5][1]};
  if(typeof value!=="number"||!Number.isFinite(value)||value<=0)fail("hauteur invalide");
  const i=value<10?0:value<20?1:value<35?2:value<60?3:4;
  return {label:HEIGHT_BANDS[i][0],color:HEIGHT_BANDS[i][1]};
}
function ringValid(r){
  if(!Array.isArray(r)||r.length<4||r.length>5000)return false;
  if(!r.every(p=>Array.isArray(p)&&p.length>=2&&Number.isFinite(p[0])&&
    Number.isFinite(p[1])&&p[0]>2.15&&p[0]<2.51&&p[1]>48.75&&p[1]<49))return false;
  const a=r[0],b=r.at(-1);return a[0]===b[0]&&a[1]===b[1];
}
export function polygonValid(g){
  if(!g||!["Polygon","MultiPolygon"].includes(g.type))return false;
  const polygons=g.type==="Polygon"?[g.coordinates]:g.coordinates;
  return Array.isArray(polygons)&&polygons.length>0&&polygons.length<=25&&
    polygons.every(rings=>Array.isArray(rings)&&rings.length>0&&rings.length<=25&&rings.every(ringValid));
}
export async function parseSnapshot(buffer,expectedSha){
  if(!(buffer instanceof ArrayBuffer)||buffer.byteLength===0||buffer.byteLength>MAX_BYTES)fail("taille");
  if(!/^[a-f0-9]{64}$/.test(expectedSha))fail("empreinte non configurée");
  const bytes=await crypto.subtle.digest("SHA-256",buffer);
  const digest=Array.from(new Uint8Array(bytes),v=>v.toString(16).padStart(2,"0")).join("");
  if(digest!==expectedSha)fail("SHA-256 modifié");
  const data=JSON.parse(new TextDecoder("utf-8",{fatal:true}).decode(buffer));
  const meta=data?.metadata;
  if(data?.type!=="FeatureCollection"||!Array.isArray(data.features)||
    data.features.length!==EXPECTED_COUNT||meta?.included_features!==EXPECTED_COUNT||
    meta?.expected_features!==EXPECTED_COUNT||meta?.public_release_allowed!==false||
    meta?.research_only!==true||meta?.not_vacancy_data!==true||
    meta?.scientific_vintage!=="not confirmed by Apur"||
    meta?.source_archive_sha256!==SOURCE_SHA256||
    meta?.output_crs!=="EPSG:4326"||meta?.source_crs!=="EPSG:2154"||
    meta?.height_field!=="h_med"||meta?.height_unit!=="m"||
    meta?.license!=="ODbL-1.0")fail("schéma, cardinalité ou provenance");
  const seen=new Set();
  const features=data.features.map(f=>{
    const p=f?.properties;
    if(!p||Object.keys(p).length!==3||
      !Object.hasOwn(p,"object_id")||!Object.hasOwn(p,"period_code")||
      !Object.hasOwn(p,"height_m")||!Number.isSafeInteger(p.object_id)||
      seen.has(p.object_id)||!polygonValid(f.geometry))fail("ID, géométrie ou attribut");
    seen.add(p.object_id);
    periodStyle(p.period_code);
    heightStyle(p.height_m);
    return {type:"Feature",geometry:f.geometry,properties:{
      object_id:p.object_id,period_code:p.period_code,height_m:p.height_m
    }};
  });
  return {collection:{type:"FeatureCollection",features},metadata:meta,digest};
}
export async function fetchLocalSnapshot(expectedSha, fetcher=fetch){
  const response=await fetcher("./data/apur-lab.geojson",{cache:"no-store"});
  if(!response.ok)throw new Error("Extrait local indisponible : HTTP "+response.status);
  return parseSnapshot(await response.arrayBuffer(),expectedSha);
}
