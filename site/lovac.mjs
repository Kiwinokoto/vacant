import {checkLovac,years} from "./lovac-public-contract.mjs";
import {COUNT_BINS,lovacColor,validateLovacGeography,districtLovac} from "./lovac-map-contract.mjs";
const fmt=new Intl.NumberFormat("fr-FR");
const $=id=>document.getElementById(id);
const status=$("lovac-status"),bars=$("lovac-bars");
let dataset=null,metric="vacant",geography=null,map=null,polygonLayer=null;
const mapStatus=$("lovac-map-status");
const selectedYear=()=>Number($("lovac-year").value);
function mapView(){
 if(!geography||!polygonLayer)return;
 const year=selectedYear(),date=dataset.years[year-2020].date_by_variable[metric];
 const title=metric==="vacant"?"Tous les logements vacants privés":"Vacance privée de plus de deux ans";
 $("lovac-map-title").textContent=title+" · LOVAC "+year+" · observation au "+date+" · nombres, pas des taux";
 polygonLayer.setStyle(f=>({color:"#253943",weight:1.2,fillOpacity:.82,fillColor:lovacColor(districtLovac(dataset,f.properties.arrondissement_code,year,metric).count,metric)}));
 polygonLayer.eachLayer(layer=>layer.bindPopup(()=>{
  const item=districtLovac(dataset,layer.feature.properties.arrondissement_code,year,metric);
  const wrapper=document.createElement("div");
  wrapper.append(cell("strong",item.arrondissement+"e arrondissement"));
  wrapper.append(cell("p",fmt.format(item.count)+" logements · "+title));
  wrapper.append(cell("p","Observation : "+date+" · millésime "+year));
  wrapper.append(cell("p","LOVAC, parc privé fiscal · agrégat territorial, pas de localisation de logements."));
  return wrapper;
 }));
 const legend=$("lovac-map-legend");legend.replaceChildren();
 for(const bin of COUNT_BINS[metric]){
  const row=cell("div","");row.className="lovac-legend-row";
  const swatch=cell("i","");swatch.style.backgroundColor=bin.color;
  row.append(swatch,cell("span",bin.label+" logements"));legend.append(row);
 }
 mapStatus.textContent="20 arrondissements · comptages publics, contours IGN 2025. Comparaisons temporelles limitées par les ruptures GMBI 2024 et 2025.";
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
 for(const district of dataset.arrondissements){
  const tr=document.createElement("tr"),data=district.series[String(year)];
  const head=cell("th",district.arrondissement+"e");head.scope="row";
  tr.append(head,cell("td",fmt.format(data.vacant)),cell("td",fmt.format(data.long)));
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
 draw();table();await loadMap();
}catch(e){
 status.textContent="LOVAC non affiché : "+e.message;
 $("lovac-year").disabled=true;
 $("metric-vacant").disabled=true;$("metric-long").disabled=true;
}