import {test} from "node:test";
import assert from "node:assert/strict";
import {TIMELINE} from "../site/timeline.mjs";
import {compareArrondissement,compareColor,changeColor,CHANGE_PALETTES,
 summarizeArrondissementChanges,buildComparisonPopup} from "../site/arrondissement-compare.mjs";

function dataset(){
 return {type:"FeatureCollection",metadata:{kind:"vacant_housing_arrondissement_estimate"},
 features:Array.from({length:20},(_,i)=>({type:"Feature",properties:{
   arrondissement:i+1,arrondissement_code:"751"+String(i+1).padStart(2,"0"),
   series:Object.fromEntries(TIMELINE.map(y=>[y.year,{
     housing_count:y.total/20,
     vacant_count:y.vacant/20,
     vacancy_percent:Math.round(y.vacant/y.total*1000)/10
   }]))
 }}))};
}
test("comparison uses original counts and returns points, NOT relative percent",()=>{
 const feat=dataset().features[0].properties;
 const c=compareArrondissement(feat,2006,2023);
 assert.equal(c.vacantDelta,(139075-122667)/20);
 assert.ok(Math.abs(c.rateDeltaPoints-100*(139075/1402024-122667/1334814))<1e-10);
 assert.ok(c.rateDeltaPoints<1); // increase < 1 percentage POINT
 assert.throws(()=>compareArrondissement(feat,2023,2006),/ordre chronologique/);
 assert.throws(()=>compareArrondissement(feat,2006,2006),/ordre chronologique/);
 assert.throws(()=>compareArrondissement(feat,2007,2023),/ordre chronologique/);
});
test("Paris summary is an audited weighted difference, not average of arrondissement colors",()=>{
 const info=summarizeArrondissementChanges(dataset(),2011,2023);
 assert.ok(Math.abs(info.changedVacant-(139075-98698))<.001);
 assert.ok(Math.abs(info.changedRatePoints-100*(139075/1402024-98698/1356074))<1e-10);
 assert.equal(info.rows.length,20);
});
test("mismatched source totals or missing years abort the comparison",()=>{
 const d=dataset();
 d.features[0].properties.series["2011"].vacant_count+=99;
 assert.throws(()=>summarizeArrondissementChanges(d,2011,2023),/incompatibles/);
 const bad=dataset();bad.features[0].properties.series["2006"]=null;
 assert.throws(()=>summarizeArrondissementChanges(bad,2006,2023),/manquante/);
 assert.throws(()=>summarizeArrondissementChanges({features:[]},2006,2023),/vingt/);
});
test("diverging colors and ranges are explicit for points and count",()=>{
 assert.equal(CHANGE_PALETTES.points.length,5);
 assert.equal(CHANGE_PALETTES.count.length,5);
 for(const kind of ["points","count"]){
   const bands=CHANGE_PALETTES[kind];assert.notEqual(bands[0].color,bands[4].color);
 }
 assert.equal(changeColor(-4,"points"),"#347a97");
 assert.equal(changeColor(4,"points"),"#b76b65");
 assert.equal(changeColor(0,"points"),"#b3bbc0");
 assert.equal(changeColor(null,"points"),"#8997a3");
 assert.equal(changeColor(150,"count"),"#d7ab6a");
 assert.equal(compareColor(dataset().features[0].properties,2006,2023,"count"),"#d7ab6a");
});
test("popup uses DOM text nodes for published aggregates, never untrusted markup",()=>{
 const oldDocument=globalThis.document;
 const elems=[];
 globalThis.document={createElement(tag){
  const obj={tag,textContent:"",children:[],append(...children){this.children.push(...children)}};
  elems.push(obj);return obj;
 }};
 try{
  const f=dataset().features[0];f.properties.arrondissement="<img src=x onerror=alert(1)>";
  const pop=buildComparisonPopup(f,2006,2023);
  assert.equal(pop.tag,"div");
  assert.ok(pop.children[0].textContent.startsWith("<img"));
  assert.ok(pop.children.some(p=>p.textContent.includes("points de pourcentage")));
  assert.ok(pop.children.some(p=>p.textContent.includes("aucun logement vacant")));
  assert.ok(elems.every(x=>!Object.hasOwn(x,"innerHTML")));
 }finally{globalThis.document=oldDocument}
});
