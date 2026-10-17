// LOVAC public commune-level aggregates only: no per-address inference.
// A share among vacant private dwellings is NOT a private-stock vacancy rate.
export const SHARE_BINS=Object.freeze([
 {max:20,color:"#dae6e7",label:"Jusqu’à 20 %"},
 {max:25,color:"#a8d0d1",label:"Plus de 20 à 25 %"},
 {max:30,color:"#72aeb5",label:"Plus de 25 à 30 %"},
 {max:35,color:"#327d91",label:"Plus de 30 à 35 %"},
 {max:Infinity,color:"#154c66",label:"Plus de 35 %"}
]);
export function referenceForShare(data,year){
 const p=data?.years?.find(x=>x.production_year===year);
 const dates=p?.date_by_variable;
 if(!p||!/^\d{4}-\d{2}-\d{2}$/.test(dates?.vacant||"")||
   dates.vacant!==dates.long)
  throw Error("Proportion indisponible : dates de référence LOVAC incompatibles (notamment en 2023)");
 return dates.vacant;
}
export function shareLongColor(percent){
 if(!Number.isFinite(percent)||percent<0||percent>100)
   throw Error("Part de vacance longue invalide");
 return SHARE_BINS.find(x=>percent<=x.max).color;
}
export function longTermSnapshot(data,year,mode="share-long"){
 if(!["share-long","long","vacant"].includes(mode)||!Number.isInteger(year))
   throw Error("Indicateur territorial LOVAC invalide");
 const p=data?.years?.find(x=>x.production_year===year);
 if(!p||data?.arrondissements?.length!==20)throw Error("Millésime LOVAC indisponible");
 // Ratios require the SAME observation date for numerator and denominator.
 const date=mode==="share-long"?referenceForShare(data,year):p.date_by_variable[mode];
 const rows=data.arrondissements.map(d=>{
  const s=d.series?.[String(year)];
  if(!Number.isInteger(s?.vacant)||!Number.isInteger(s?.long)||s.vacant<0||s.long<0||s.long>s.vacant)
    throw Error("Agrégat LOVAC incompatible");
  if(mode==="share-long"&&s.vacant===0)throw Error("Part indéfinie : aucun vacant dans un arrondissement");
  return {
   arrondissement:d.arrondissement,code:d.code,vacant:s.vacant,long:s.long,
   value:mode==="share-long"?100*s.long/s.vacant:s[mode]
  };
 });
 if(!Number.isInteger(p.paris?.long)||!Number.isInteger(p.paris?.vacant)||
    p.paris.long<0||p.paris.vacant<p.paris.long||
    rows.reduce((n,x)=>n+x.long,0)!==p.paris.long||
    rows.reduce((n,x)=>n+x.vacant,0)!==p.paris.vacant)
  throw Error("Sommes départementales LOVAC incohérentes");
 const paris=mode==="share-long"
  ? (p.paris.vacant===0?null:100*p.paris.long/p.paris.vacant)
  : p.paris[mode];
 if(paris===null)throw Error("Part parisienne indéfinie");
 return {year,date,mode,paris,parisVacant:p.paris.vacant,parisLong:p.paris.long,
  rows:rows.sort((a,b)=>b.value-a.value||a.arrondissement-b.arrondissement)};
}
