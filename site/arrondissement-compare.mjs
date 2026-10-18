// Insee vacancy estimates by ARRONDISSEMENT, never by building/modern IRIS.
// Reference-year statistics were aggregated from their original IRIS geographies.
import {TIMELINE} from "./timeline.mjs";

export const ARROND_YEARS=Object.freeze(TIMELINE.map(v=>v.year));
export const CHANGE_PALETTES=Object.freeze({
  points:Object.freeze([
    Object.freeze({max:-3,label:"Baisse d’au moins 3 points",color:"#347a97"}),
    Object.freeze({max:-1,label:"Baisse de 1 à moins de 3 points",color:"#70aeb7"}),
    Object.freeze({max:1,label:"Variation entre −1 et +1 point",color:"#b3bbc0"}),
    Object.freeze({max:3,label:"Hausse de 1 à moins de 3 points",color:"#d7ab6a"}),
    Object.freeze({max:Infinity,label:"Hausse d’au moins 3 points",color:"#b76b65"})
  ]),
  count:Object.freeze([
    Object.freeze({max:-500,label:"Baisse d’au moins 500 logements",color:"#347a97"}),
    Object.freeze({max:-100,label:"Baisse de 100 à moins de 500 logements",color:"#70aeb7"}),
    Object.freeze({max:100,label:"Variation entre −100 et +100 logements",color:"#b3bbc0"}),
    Object.freeze({max:500,label:"Hausse de 100 à moins de 500 logements",color:"#d7ab6a"}),
    Object.freeze({max:Infinity,label:"Hausse d’au moins 500 logements",color:"#b76b65"})
  ])
});
const round=(n,digits)=>Math.round(n*10**digits)/10**digits;
function checkYears(first,last){
  if(!ARROND_YEARS.includes(first)||!ARROND_YEARS.includes(last)||first>=last)
    throw new RangeError("Sélectionner deux recensements distincts dans l’ordre chronologique");
}
function checked(p,year){
  const s=p?.series?.[String(year)];
  if(!s||!Number.isFinite(s.housing_count)||s.housing_count<=0 ||
      !Number.isFinite(s.vacant_count)||s.vacant_count<0||s.vacant_count>s.housing_count)
    throw new Error("Statistique d’arrondissement manquante ou invalide");
  return s;
}
export function compareArrondissement(properties,first,last) {
  checkYears(first,last);
  const old=checked(properties,first),now=checked(properties,last);
  const oldRate=100*old.vacant_count/old.housing_count;
  const nowRate=100*now.vacant_count/now.housing_count;
  return Object.freeze({
    first,last,oldVacant:old.vacant_count,newVacant:now.vacant_count,
    oldHousing:old.housing_count,newHousing:now.housing_count,oldRate,nowRate,
    rateDeltaPoints:nowRate-oldRate,vacantDelta:now.vacant_count-old.vacant_count
  });
}
export function changeColor(value,metric="points"){
  if(!Number.isFinite(value)||!CHANGE_PALETTES[metric])return "#8997a3";
  return CHANGE_PALETTES[metric].find(item=>value<=item.max).color;
}
export function compareColor(properties,first,last,metric){
  const change=compareArrondissement(properties,first,last);
  return changeColor(metric==="count"?change.vacantDelta:change.rateDeltaPoints,metric);
}
export function summarizeArrondissementChanges(dataset,first,last){
  checkYears(first,last);
  if(dataset?.features?.length!==20 ||
      dataset?.metadata?.kind!=="vacant_housing_arrondissement_estimate")
    throw new Error("Comparaison autorisée sur vingt arrondissements validés uniquement");
  let beforeTotal=0,afterTotal=0,beforeHousing=0,afterHousing=0,increased=0,decreased=0;
  const rows=[];
  for(const feat of dataset.features){
    const c=compareArrondissement(feat.properties,first,last);
    beforeTotal+=c.oldVacant;afterTotal+=c.newVacant;
    beforeHousing+=c.oldHousing;afterHousing+=c.newHousing;
    if(c.rateDeltaPoints>0)increased++;else if(c.rateDeltaPoints<0)decreased++;
    rows.push(Object.freeze({arrondissement:feat.properties.arrondissement,code:feat.properties.arrondissement_code,...c}));
  }
  const old=TIMELINE.find(x=>x.year===first),now=TIMELINE.find(x=>x.year===last);
  if(Math.abs(beforeTotal-old.vacant)>1.1||Math.abs(afterTotal-now.vacant)>1.1||
     Math.abs(beforeHousing-old.total)>1.1||Math.abs(afterHousing-now.total)>1.1)
    throw new Error("Sommes d’arrondissements incompatibles avec les totaux Insee Paris");
  return Object.freeze({
    first,last,
    // Paris-wide reference is the independently published Insee total.
    // Per-arrondissement estimated counts can differ by ~1 when summed due to rounding.
    changedVacant:now.vacant-old.vacant,
    changedRatePoints:100*(now.vacant/now.total-old.vacant/old.total),
    increased,decreased,rows:Object.freeze(rows)
  });
}
const fmt=new Intl.NumberFormat("fr-FR",{maximumFractionDigits:0});
const signed=(x,digits)=>(x>0?"+":"")+round(x,digits).toLocaleString("fr-FR",{minimumFractionDigits:digits,maximumFractionDigits:digits});
export function buildComparisonPopup(feature,first,last) {
  const change=compareArrondissement(feature.properties,first,last);
  const root=document.createElement("div");root.className="popup";
  const title=document.createElement("strong");
  title.textContent=feature.properties.arrondissement+"e arrondissement · "+first+" → "+last;
  root.append(title);
  const geos={2006:2008,2011:2013,2016:2018,2023:2025};
  for(const line of [
    "Logements vacants estimés "+first+" : "+fmt.format(change.oldVacant)+" / "+fmt.format(change.oldHousing),
    "Logements vacants estimés "+last+" : "+fmt.format(change.newVacant)+" / "+fmt.format(change.newHousing),
    "Taux de vacance : "+round(change.oldRate,1).toLocaleString("fr-FR")+" % → "+round(change.nowRate,1).toLocaleString("fr-FR")+" %",
    "Variation du taux : "+signed(change.rateDeltaPoints,1)+" points de pourcentage",
    "Variation du nombre de logements vacants : "+signed(change.vacantDelta,0)+" logements",
    "Sources : recensements Insee ; agrégations des IRIS de géographies "+geos[first]+" et "+geos[last]+".",
    "Contours d’arrondissements IGN 2025 uniquement pour l’affichage.",
    "Cette évolution statistique ne localise aucun logement vacant ni construction."
  ]){
    const p=document.createElement("p");p.textContent=line;root.append(p);
  }
  return root;
}
