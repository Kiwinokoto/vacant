// BDCOM 2023: only public arrondissement aggregates, never addresses or shop points.
export const MODE_LABELS=Object.freeze({
 share:"Part des locaux explicitement vacants (hors travaux)",
 vacant:"Nombre de locaux explicitement vacants (hors travaux)",
 in_works:"Nombre de locaux en travaux"
});
const EXPECTED={surveyed:83154,vacant:7495,in_works:1565,combined:9060};
export function validateBDCOM(data){
 if(data?.kind!=="bdcom_2023_aggregate_by_paris_arrondissement"||
 data?.license!=="ODbL"||data?.survey!=="2023-04"||
 data?.source!=="https://carto2.apur.org/apur/rest/services/BDCOM/bdcom2023/MapServer/1"||
 data.query_fields?.vacant!=="COUNT(OBJECTID) where codact='AA101'"||
 data.query_fields?.in_works!=="COUNT(OBJECTID) where codact='AA102'"||
 data.arrondissements?.length!==20)throw Error("Provenance BDCOM invalide");
 const sums={surveyed:0,vacant:0,in_works:0};
 const seen=new Set();
 for(const item of data.arrondissements){
   if(!Number.isInteger(item.arrondissement)||item.arrondissement<1||item.arrondissement>20||
     item.code!=="751"+String(item.arrondissement).padStart(2,"0")||
     seen.has(item.code)||Object.keys(item).some(k=>!["arrondissement","code","surveyed","vacant","in_works"].includes(k)))
     throw Error("Arrondissement ou champ individuel interdit");
   seen.add(item.code);
   if(!Number.isInteger(item.surveyed)||!Number.isInteger(item.vacant)||
     !Number.isInteger(item.in_works)||item.surveyed<=0||item.vacant<0||
     item.in_works<0||item.vacant+item.in_works>item.surveyed)
     throw Error("Données BDCOM invalides");
   sums.surveyed+=item.surveyed;sums.vacant+=item.vacant;sums.in_works+=item.in_works;
 }
 for(const [key,value] of Object.entries(EXPECTED)){
   if(value!==(key==="combined"?sums.vacant+sums.in_works:sums[key])||
     data.paris?.[key]!==value)throw Error("Sommes BDCOM incompatibles");
 }
 if(data.paris.reported_combined_in_apur_note!==9059)throw Error("Écart de publication BDCOM non tracé");
 return data;
}
export function rankBDCOM(data,mode="share"){
 validateBDCOM(data);
 if(!Object.hasOwn(MODE_LABELS,mode))throw Error("Classement BDCOM non reconnu");
 const rows=data.arrondissements.map(item=>({
  ...item,value:mode==="share"?100*item.vacant/item.surveyed:item[mode]
 }));
 return rows.sort((a,b)=>b.value-a.value||a.arrondissement-b.arrondissement);
}
