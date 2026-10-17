import {isReliableIRIS,rawVacancyPercent} from "./iris-colors.mjs";

// Area count != housing stock count. NEVER average neighbourhood rates for Paris.
export function summarizeIrisVacancy2023(collection){
  if(collection?.type!=="FeatureCollection" || collection.features?.length!==992 ||
      collection.metadata?.census_year!==2023 ||
      collection.metadata?.geography_year!==2025)
    throw new Error("Only validated 2023 Paris IRIS geography can be summarized");
  const bands=[0,0,0,0,0,0];
  let totalHousing=0,totalVacant=0,visibleHousing=0;
  for(const f of collection.features){
    const p=f?.properties;
    if(!p||!Number.isFinite(p.housing_count)||!Number.isFinite(p.vacant_count)||
        p.housing_count<0||p.vacant_count<0||p.vacant_count>p.housing_count||
        p.census_year!==2023||p.geography_year!==2025){
      throw new Error("Invalid IRIS statistic");
    }
    totalHousing+=p.housing_count;
    totalVacant+=p.vacant_count;
    if(!isReliableIRIS(p)){bands[5]++;continue;}
    visibleHousing+=p.housing_count;
    const rate=rawVacancyPercent(p);
    const band=rate<5?0:rate<8?1:rate<12?2:rate<20?3:4;
    bands[band]++;
  }
  if(Math.abs(totalHousing-1402024)>2||Math.abs(totalVacant-139075)>2)
    throw new Error("IRIS totals disagree with independently published Paris 2023 census");
  return Object.freeze({
    bands:Object.freeze(bands),
    visible:992-bands[5],hidden:bands[5],
    atLeastFive:bands[1]+bands[2]+bands[3]+bands[4],
    atLeastTwelve:bands[3]+bands[4],
    totalHousing,totalVacant,
    parisRate:Math.round(totalVacant/totalHousing*1000)/10,
    note:"Nombre de quartiers IRIS, pas proportion de surface ni statut d'immeuble."
  });
}
