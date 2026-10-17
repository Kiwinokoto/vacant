import {enabled,parseSnapshot,compareIds} from "./contract.mjs";
const status=document.querySelector("#status");
if(!enabled(location)){
 status.textContent="Accès au laboratoire refusé : servir sur localhost avec ?ign_lab=1.";
}else if(!window.L){
 status.textContent="Leaflet est indisponible. Vérifier le réseau.";
}else{
 const maps=["2011","2018"].map(id=>L.map("map-"+id,{preferCanvas:true}).setView([48.855,2.3747],16));
 for(const map of maps)L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{
  maxZoom:19,attribution:"© OpenStreetMap contributors"
 }).addTo(map);
 let syncing=false;
 for(const [i,map] of maps.entries())map.on("moveend",()=>{
  if(syncing)return;
  syncing=true;
  const next=maps[1-i];
  if(!next.getCenter().equals(map.getCenter())||next.getZoom()!==map.getZoom())
   next.setView(map.getCenter(),map.getZoom(),{animate:false});
  syncing=false;
 });
 const sources=[["2011-04-12","2011.geojson","#447ca5"],["2018-03-29","2018.geojson","#cf825d"]];
 async function load([edition,file,color]){
  const response=await fetch("./_local/"+file,{cache:"no-store"});
  if(!response.ok)throw Error(file+" : HTTP "+response.status);
  const bytes=await response.arrayBuffer();
  if(bytes.byteLength>6_000_000)throw Error(file+" trop volumineux pour ce laboratoire");
  const data=parseSnapshot(JSON.parse(new TextDecoder("utf8",{fatal:true}).decode(bytes)),edition);
  const layer=L.geoJSON(data,{style:()=>({color:"#294257",weight:.65,fillColor:color,fillOpacity:.65}),
   onEachFeature:(f,leaf)=>{
    const popup=document.createElement("div");
    const strong=document.createElement("strong");strong.textContent="Empreinte IGN · édition "+edition;
    const body=document.createElement("p");body.textContent="Classe : "+f.properties.kind+
     ". Hauteur : "+(f.properties.height_raw==null?"indisponible":f.properties.height_raw+" m")+
     ". Aucune preuve de construction, démolition ou vacance.";
    popup.append(strong,body);leaf.bindPopup(popup);
   }}).addTo(maps[sources.findIndex(s=>s[0]===edition)]);
  return {data,layer};
 }
 Promise.all(sources.map(load)).then(([a,b])=>{
  const counts=compareIds(a.data,b.data);
  document.querySelector("#metric-2011").textContent=counts.first+" polygones intersectant la zone d'étude";
  document.querySelector("#metric-2018").textContent=counts.second+" polygones intersectant la zone d'étude";
  status.textContent="Éditions contrôlées · "+counts.shared+" identifiants communs sur cette zone · "+
  counts.onlyFirst+" IDs seulement dans l'extrait 2011 · "+counts.onlySecond+" seulement en 2018. "+
  counts.warning+". Attention : les identifiants globaux des archives sont plus nombreux.";
 }).catch(e=>{status.textContent="Aucune couche appliquée : "+e.message+" — données historiques privées absentes ou refusées."});
}
