export const years=[2020,2021,2022,2023,2024,2025,2026];
export const labels={vacant:"Logements vacants du parc privé",long:"Vacants depuis plus de deux ans"};
const totals=[[122856,18648],[124555,19822],[129788,20380],[150072,21489],[142848,32091],[75774,36205],[105785,26264]];
export function checkLovac(x){
 if(x?.kind!=="lovac_public_private_housing_aggregates"||x.license!=="Licence Ouverte 2.0"||
 x.source_sha256?.["lovac-opendata-communes26.csv"]!=="b856568d4b69784d32f9fafaf7e1376047e45eed245fb114dd737d2d43826245"||
 x.arrondissements?.length!==20||x.years?.length!==7)throw Error("Source LOVAC non vérifiée");
 for(let i=0;i<7;i++){
  const y=years[i],rec=x.years[i];
  if(rec.production_year!==y||rec.paris.vacant!==totals[i][0]||rec.paris.long!==totals[i][1]||
    rec.date_by_variable.vacant!==(y===2023?"2023-01-01":String(y-1)+"-01-01")||
    rec.date_by_variable.long!==(y===2023?"2022-01-01":String(y-1)+"-01-01")||
    (y===2026&&"stock" in rec.paris))throw Error("LOVAC : totaux ou dates invalides");
  let v=0,l=0;
  for(let n=1;n<=20;n++){
   const a=x.arrondissements[n-1];
   if(a?.code!=="751"+String(n).padStart(2,"0"))throw Error("Arrondissement absent");
   const s=a.series[String(y)];
   if(!Number.isInteger(s?.vacant)||!Number.isInteger(s?.long)||
     s.long<0||s.vacant<s.long)throw Error("Statistique secrétisée ou invalide");
   v+=s.vacant;l+=s.long;
  }
  if(v!==rec.paris.vacant||l!==rec.paris.long)throw Error("Écart avec Paris département");
 }
 return x;
}
