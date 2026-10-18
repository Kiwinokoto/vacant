import {test} from "node:test";
import assert from "node:assert/strict";
import {summarizeIrisVacancy2023} from "../site/iris-insights.mjs";
import {colorForIRIS,rawVacancyPercent} from "../site/iris-colors.mjs";

const base=()=>({type:"FeatureCollection",metadata:{census_year:2023,geography_year:2025},
  features:Array.from({length:992},(_,i)=>({type:"Feature",properties:{
   iris_code:String(751000000+i),census_year:2023,geography_year:2025,
   housing_count:i===0?1402024:0,vacant_count:i===0?139075:0,
   vacancy_percent:i===0?9.9:null,status:"statistique_agregee"
  }}))
});
test("Paris weighted rate comes from numerator and denominator, not an average of IRIS percentages",()=>{
 const s=summarizeIrisVacancy2023(base());
 assert.equal(s.totalHousing,1402024);
 assert.equal(s.totalVacant,139075);
 assert.equal(s.parisRate,9.9);
 assert.equal(s.visible,1);
 assert.equal(s.hidden,991);
 assert.equal(s.atLeastFive,1);
 assert.equal(s.atLeastTwelve,0);
});
test("2023 and 2025 geometry vintage are mandatory",()=>{
 const x=base();x.metadata.geography_year=2013;
 assert.throws(()=>summarizeIrisVacancy2023(x),/Only validated/);
});
test("tampered totals and negative vacancy counts block the panel",()=>{
 const x=base();x.features[0].properties.vacant_count=1402025;
 assert.throws(()=>summarizeIrisVacancy2023(x),/Invalid IRIS/);
});
test("unrounded vacancy ratio determines colors near a class boundary",()=>{
 const p={housing_count:1000,vacant_count:49.6,vacancy_percent:5.0,status:"statistique_agregee"};
 assert.ok(rawVacancyPercent(p)<5);
 assert.equal(colorForIRIS(p),"#74c3aa");
 assert.equal(colorForIRIS({...p,vacant_count:50.1,vacancy_percent:5.0}),"#80a8cf");
});
