// Aggregated Apur BDCOM observations; refuses fake continuous rates or per-address data.
export const BDCOM_HISTORY_YEARS=Object.freeze([2017,2020,2023]);
export function checkBDCOMHistory(data){
 if(data?.schema!=="bdcom-paris-historical-comparison-v1"||data.geography!=="Paris intra-muros, BDCOM ground-floor premises"||
 data.count_unit!=="premises"||data.license!=="ODbL"||data.derived_only!==true||
 data.access_date!=="2026-10-17"||
 data.observations?.length!==3||!Array.isArray(data.cautions)||
 data.cautions.length<3||Object.keys(data.provenance||{}).sort().join(",")!=="2017,2020,2023")
 throw Error("Provenance historique BDCOM invalide");
 const expected={2017:[6954,899,7853],2020:[7247,1517,8764],2023:[7495,1565,9060]};
 const allowed=new Set(["year","vacant","in_works","combined","publication_rounded","publication_revised_2023","surveyed","surveyed_source","surveyed_basis","publication_original_vacant","publication_retro_2023_works"]);
 const denominators={2017:[83720,"https://www.apur.org/open_data/BDCOM_2017_OD.pdf"],2020:[83399,"https://carto2.apur.org/apur/rest/services/BDCOM/bdcom2020_structure/MapServer/0"],2023:[83154,"https://carto2.apur.org/apur/rest/services/BDCOM/bdcom2023/MapServer/1"]};
 for(let i=0;i<3;i++){
  const x=data.observations[i],y=BDCOM_HISTORY_YEARS[i],e=expected[y];
  if(x?.year!==y||Object.keys(x).some(k=>!allowed.has(k))||
   ![x.vacant,x.in_works,x.combined].every(n=>Number.isInteger(n)&&n>=0)||
   x.vacant+x.in_works!==x.combined||
   !Number.isInteger(x.surveyed)||x.surveyed<=x.combined||
   x.surveyed!==denominators[y][0]||x.surveyed_source!==denominators[y][1]||
   typeof x.surveyed_basis!=="string"||x.surveyed_basis.length<18||
   x.vacant!==e[0]||x.in_works!==e[1]||x.combined!==e[2]||
   !data.provenance[String(y)]?.url?.startsWith("https://carto2.apur.org/apur/rest/services/BDCOM/"))
   throw Error("Effectifs ou champs historiques BDCOM invalides");
 }
 if(data.observations[0].publication_rounded!==7850||
   data.observations[1].publication_rounded!==8760||
   data.observations[1].publication_revised_2023!==8560||
   data.observations[2].publication_rounded!==9059||
   data.observations[0].publication_original_vacant!==7804||
   data.observations[1].publication_retro_2023_works!==1310)
 throw Error("Divergences éditoriales non consignées");
 return data;
}
export function historyRows(data){
 return checkBDCOMHistory(data).observations.map(x=>({year:x.year,vacant:x.vacant,in_works:x.in_works,combined:x.combined,surveyed:x.surveyed}));
}
