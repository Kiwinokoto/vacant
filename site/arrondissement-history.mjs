// Historical arrondissement observations are not assignable to buildings or newer IRIS.
import { TIMELINE } from "./timeline.mjs";

export function statForYear(props, year) {
  const p=props.series?.[String(year)];
  return p ? {...p,status:"statistique_agregee"} : null;
}
export function validateArrondissementSeries(dataset) {
  const years=TIMELINE.map(x=>x.year);
  if(dataset?.type!=="FeatureCollection" ||
    dataset.metadata?.kind!=="vacant_housing_arrondissement_estimate" ||
    dataset.metadata?.geometry?.startsWith("2025 arrondissement display boundary")!==true ||
    JSON.stringify(dataset.metadata?.years)!==JSON.stringify(years) ||
    !Array.isArray(dataset.features) || dataset.features.length!==20) {
    throw new Error("historique incomplet ou métadonnées incompatibles");
  }
  const codes=new Set(), sums=Object.fromEntries(years.map(y=>[y,{housing:0,vacant:0}]));
  for(const f of dataset.features) {
    const p=f.properties, code=p?.arrondissement_code;
    if(!/^751(0[1-9]|1[0-9]|20)$/.test(code) || codes.has(code) ||
       (f.geometry?.type!=="Polygon" && f.geometry?.type!=="MultiPolygon")){
      throw new Error("code ou géométrie d'arrondissement invalide");
    }
    codes.add(code);
    for(const year of years) {
      const s=p.series?.[String(year)];
      if(!s || !Number.isFinite(s.housing_count) || !Number.isFinite(s.vacant_count) ||
         s.housing_count<0 || s.vacant_count<0 || s.vacant_count>s.housing_count ||
         (s.housing_count>=50 && (!Number.isFinite(s.vacancy_percent) ||
          Math.abs(s.vacancy_percent-100*s.vacant_count/s.housing_count)>0.06))){
        throw new Error("estimation historique incohérente");
      }
      sums[year].housing+=s.housing_count;
      sums[year].vacant+=s.vacant_count;
    }
  }
  for(const point of TIMELINE){
    if(Math.abs(sums[point.year].housing-point.total)>1.1 ||
       Math.abs(sums[point.year].vacant-point.vacant)>1.1)
      throw new Error("les totaux historiques ne correspondent pas aux tableaux Insee");
  }
}
export function buildArrondissementPopup(feature, year){
  const p=feature.properties, s=p.series[String(year)];
  const fmt=new Intl.NumberFormat("fr-FR",{maximumFractionDigits:0});
  const root=document.createElement("div"), title=document.createElement("strong");
  title.textContent=p.arrondissement+"e arrondissement · recensement "+year;
  root.append(title);
  for(const line of [
    "Logements estimés : "+fmt.format(s.housing_count),
    "Logements vacants estimés : "+fmt.format(s.vacant_count),
    "Taux de vacance de l'arrondissement : "+s.vacancy_percent.toLocaleString("fr-FR")+" %",
    "Statistiques Insee agrégées des IRIS géographie "+({2006:2008,2011:2013,2016:2018,2023:2025})[year],
    "Géométrie d'arrondissement : fond IGN 2025, non contours historiques d'IRIS",
    "Ne permet pas d'identifier l'occupation d'un immeuble."
  ]){
    const el=document.createElement("p");el.textContent=line;root.append(el);
  }
  return root;
}
