// Territorial counts only. Never apply LOVAC values to buildings or addresses.
export const COUNT_BINS=Object.freeze({
 vacant:[{max:2500,color:"#dae6e7",label:"0 à 2 500"},{max:5000,color:"#a8d0d1",label:"2 501 à 5 000"},{max:8000,color:"#72aeb5",label:"5 001 à 8 000"},{max:12000,color:"#327d91",label:"8 001 à 12 000"},{max:Infinity,color:"#154c66",label:"Plus de 12 000"}],
 long:[{max:500,color:"#dae6e7",label:"0 à 500"},{max:1000,color:"#a8d0d1",label:"501 à 1 000"},{max:1500,color:"#72aeb5",label:"1 001 à 1 500"},{max:2500,color:"#327d91",label:"1 501 à 2 500"},{max:Infinity,color:"#154c66",label:"Plus de 2 500"}]
});
export function lovacColor(count,metric){
 if(!Number.isInteger(count)||count<0||!COUNT_BINS[metric])throw Error("Comptage LOVAC invalide");
 return COUNT_BINS[metric].find(bin=>count<=bin.max).color;
}
export function validateLovacGeography(geo,lovac){
 if(geo?.type!=="FeatureCollection"||geo.features?.length!==20||
    geo.metadata?.geometry?.startsWith("2025 arrondissement display boundary")!==true)
   throw Error("Contours IGN 2025 des arrondissements non validés");
 const known=new Set(lovac.arrondissements.map(d=>d.code)),seen=new Set();
 for(const f of geo.features){
   const code=f?.properties?.arrondissement_code;
   if(!known.has(code)||seen.has(code)||!["Polygon","MultiPolygon"].includes(f.geometry?.type))
     throw Error("Correspondance géographique LOVAC invalide");
   seen.add(code);
 }
 return true;
}
export function districtLovac(lovac,code,year,metric){
 if(!COUNT_BINS[metric]||!Number.isInteger(year)||year<2020||year>2026)throw Error("Sélection LOVAC invalide");
 const d=lovac.arrondissements.find(x=>x.code===code);
 if(!d)throw Error("Arrondissement non reconnu");
 const count=d.series[String(year)]?.[metric];
 lovacColor(count,metric);
 return {code,arrondissement:d.arrondissement,count};
}
