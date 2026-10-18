import {checkLovac,years} from "./lovac-public-contract.mjs";
import {COUNT_BINS,lovacColor,validateLovacGeography,districtLovac} from "./lovac-map-contract.mjs";
import {SHARE_BINS,shareLongColor,longTermSnapshot,referenceForShare} from "./lovac-long-analysis.mjs";
const fmt=new Intl.NumberFormat("fr-FR");
const $=id=>document.getElementById(id);
const status=$("lovac-status"),bars=$("lovac-bars");
let dataset=null,metric="vacant",geography=null,map=null,polygonLayer=null;
const mapStatus=$("lovac-map-status");
const selectedYear=()=>Number($("lovac-year").value);
const mapMode=()=> $("lovac-map-view").value;
const modeLabel=mode=>mode==="share-long"?"Part de longue durée parmi les logements privés vacants":mode==="long"?"Vacants privés depuis plus de deux ans":"Tous les logements privés vacants";
const numberLabel=(n,mode)=>mode==="share-long"
 ?n.toLocaleString("fr-FR",{minimumFractionDigits:1,maximumFractionDigits:1})+" %"
 :fmt.format(n)+" logements";
function mapView(){
 if(!dataset)return;
 const year=selectedYear(),mode=mapMode();
 const legend=$("lovac-map-legend"),ranking=$("lovac-ranking"),summary=$("lovac-snapshot-summary");
 legend.replaceChildren();ranking.replaceChildren();
 let snapshot;
 try{snapshot=longTermSnapshot(dataset,year,mode)}
 catch(error){
  const warning="LOVAC "+year+" : "+error.message+". Choisissez « nombre » pour ce millésime.";
  $("lovac-map-title").textContent=warning;
  summary.textContent=warning;
  mapStatus.textContent=warning;
  if(polygonLayer){
   polygonLayer.setStyle({color:"#253943",weight:1.2,fillOpacity:.35,fillColor:"#8997a3"});
   polygonLayer.eachLayer(layer=>layer.unbindPopup());
  }
  return;
 }
 const title=modeLabel(mode);
 $("lovac-map-title").textContent=title+" · LOVAC "+year+" · observation au "+snapshot.date;
 summary.textContent="Paris : "+fmt.format(snapshot.parisLong)+" vacants privés de plus de deux ans sur "+
  fmt.format(snapshot.parisVacant)+" vacants privés au "+snapshot.date+" ; indicateur choisi : "+
  numberLabel(snapshot.paris,mode)+". "+
  (mode==="share-long"?"Proportion pondérée par les logements, jamais moyenne des vingt proportions.":"Effectif territorial, non rapporté au parc total.");
 const bins=mode==="share-long"?SHARE_BINS:COUNT_BINS[mode];
 for(const bin of bins){
  const row=cell("div","");row.className="lovac-legend-row";
  const swatch=cell("i","");swatch.style.backgroundColor=bin.color;
  row.append(swatch,cell("span",bin.label+(mode==="share-long"?"":" logements")));
  legend.append(row);
 }
 for(const item of snapshot.rows){
  const li=cell("li",item.arrondissement+"e : "+numberLabel(item.value,mode));
  if(mode==="share-long")li.title=fmt.format(item.long)+" / "+fmt.format(item.vacant)+" vacants privés";
  ranking.append(li);
 }
 if(polygonLayer){
  const byCode=new Map(snapshot.rows.map(item=>[item.code,item]));
  polygonLayer.setStyle(f=>({
   color:"#253943",weight:1.2,fillOpacity:.82,
   fillColor:mode==="share-long"
    ?shareLongColor(byCode.get(f.properties.arrondissement_code).value)
    :lovacColor(byCode.get(f.properties.arrondissement_code).value,mode)
  }));
  polygonLayer.eachLayer(layer=>layer.bindPopup(()=>{
   const item=byCode.get(layer.feature.properties.arrondissement_code);
   const wrapper=cell("div","");
   wrapper.append(cell("strong",item.arrondissement+"e arrondissement"));
   wrapper.append(cell("p",title+" : "+numberLabel(item.value,mode)));
   wrapper.append(cell("p","Longue durée : "+fmt.format(item.long)+" ; tous vacants privés : "+fmt.format(item.vacant)));
   wrapper.append(cell("p","Date commune de l'indicateur : "+snapshot.date+" · millésime "+year));
   wrapper.append(cell("p","Agrégat territorial fiscal : ni adresse, ni taux du parc immobilier."));
   return wrapper;
  }));
 }
 mapStatus.textContent="20 arrondissements · contours IGN 2025, données LOVAC publiques. "+
  "Lecture d'un seul millésime ; ruptures de méthode GMBI 2024–2025.";
}
async function loadMap(){
 try{
  if(typeof window.L==="undefined")throw Error("Bibliothèque cartographique indisponible");
  const response=await fetch("./data/arrond-history.geojson",{cache:"no-store"});
  if(!response.ok)throw Error("Contours des arrondissements indisponibles (HTTP "+response.status+")");
  const candidate=await response.json();validateLovacGeography(candidate,dataset);geography=candidate;
  map=L.map("lovac-map",{scrollWheelZoom:false}).setView([48.8566,2.3522],12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:18,attribution:"© OpenStreetMap contributors"}).addTo(map);
  polygonLayer=L.geoJSON(geography).addTo(map);
  map.fitBounds(polygonLayer.getBounds().pad(.025));mapView();
 }catch(e){mapStatus.textContent="Carte indisponible : "+e.message+". Le tableau LOVAC reste consultable.";}
}

function cell(tag,content){const e=document.createElement(tag);e.textContent=content;return e}
function draw(){
 const values=dataset.years.map(x=>x.paris[metric]);
 const maximum=Math.max(...values);
 bars.replaceChildren();
 for(let i=0;i<years.length;i++){
  const year=years[i],p=dataset.years[i],count=values[i];
  const col=cell("div","");
  col.className="lovac-column "+(year<2024?"old":year===2024?"transition":"new");
  col.append(cell("strong",fmt.format(count)));
  const bar=cell("div","");
  bar.className="lovac-bar";
  bar.style.height=Math.round(count/maximum*150)+"px";
  bar.title=fmt.format(count)+" logements, millésime "+year+
    ", observation "+p.date_by_variable[metric];
  col.append(bar,cell("small",String(year)));
  bars.append(col);
 }
 const title=metric==="vacant"?"Logements vacants privés":"Logements privés vacants depuis plus de deux ans";
 bars.setAttribute("aria-label",title+": "+values.map((n,i)=>years[i]+" = "+fmt.format(n)).join(", ")+
   ". Rupture GMBI à partir de 2024.");
 $("metric-vacant").setAttribute("aria-pressed",String(metric==="vacant"));
 $("metric-long").setAttribute("aria-pressed",String(metric==="long"));
 status.textContent=title+" · chiffres fiscaux par millésime de production, sans comparaison causale à travers la rupture GMBI.";
 mapView();
}
function table(){
 const year=Number($("lovac-year").value);
 const point=dataset.years[year-2020];
 const ref=point.date_by_variable;
 $("lovac-reference").textContent="Millésime LOVAC "+year+
  " · tous vacants : situation au "+ref.vacant+
  " ; longue durée : situation au "+ref.long+
  (ref.stock?" ; parc privé total : situation au "+ref.stock:" ; pas de dénominateur 2026 disponible.")+
  ". Ces dates ne coïncident pas toujours.";
 const body=$("lovac-districts");body.replaceChildren();
 let shareAvailable=true;
 try{referenceForShare(dataset,year)}catch{shareAvailable=false}
 for(const district of dataset.arrondissements){
  const tr=document.createElement("tr"),data=district.series[String(year)];
  const head=cell("th",district.arrondissement+"e");head.scope="row";
  tr.append(head,cell("td",fmt.format(data.vacant)),cell("td",fmt.format(data.long)),
   cell("td",shareAvailable&&data.vacant>0?(100*data.long/data.vacant).toLocaleString("fr-FR",{minimumFractionDigits:1,maximumFractionDigits:1})+" %":"—"));
  body.append(tr);
 }
 mapView();
}
try{
 const response=await fetch("./data/lovac-paris-open-2026.json",{cache:"no-store"});
 if(!response.ok)throw Error("Agrégats indisponibles (HTTP "+response.status+")");
 dataset=checkLovac(await response.json());
 for(const button of ["vacant","long"]){
  $("metric-"+button).addEventListener("click",()=>{metric=button;draw()});
 }
 $("lovac-year").addEventListener("change",table);
 $("lovac-map-view").addEventListener("change",mapView);
 draw();table();await loadMap();
}catch(e){
 status.textContent="LOVAC non affiché : "+e.message;
 $("lovac-year").disabled=true;
 $("metric-vacant").disabled=true;$("metric-long").disabled=true;
}