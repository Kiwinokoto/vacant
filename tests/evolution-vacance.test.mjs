import {test} from "node:test";
import assert from "node:assert/strict";
import {
 VACANCY_HISTORY,INSEE_SOURCE,validateVacancyHistory,selectHistoricYear,
 vacancyRatePct,comparableRecentChange
} from "../site/evolution-data.mjs";
test("Nine Insee LOG T1 Paris milestones only, never one point per year",()=>{
 assert.deepEqual(VACANCY_HISTORY.map(p=>p.year),[1968,1975,1982,1990,1999,2007,2012,2017,2023]);
 assert.equal(validateVacancyHistory(VACANCY_HISTORY),true);
 assert.throws(()=>selectHistoricYear(2013),/Unpublished/);
 assert.ok(VACANCY_HISTORY.every(p=>p.source===INSEE_SOURCE));
});
test("1968/1999 old censuses are explicitly distinct from rolling RP 2007 onward",()=>{
 assert.deepEqual(VACANCY_HISTORY.map(p=>p.series),[
  "denombrement","denombrement","denombrement","denombrement","denombrement",
  "rp","rp","rp","rp"]);
 assert.throws(()=>comparableRecentChange(selectHistoricYear(1999),selectHistoricYear(2007)),/Cannot present/);
});
test("2023 share and counts derived from audited Insee numerator and denominator",()=>{
 const p=selectHistoricYear(2023);
 assert.equal(p.vacant,139075);
 assert.equal(p.total,1402024);
 assert.equal(p.secondaryOccasional,138426);
 assert.equal(vacancyRatePct(p),9.9);
 assert.equal(vacancyRatePct(selectHistoricYear(1968)),3.3);
});
test("changes compare distinct recent RP observations not fabricated annual movement",()=>{
 const delta=comparableRecentChange(selectHistoricYear(2012),selectHistoricYear(2023));
 assert.equal(delta.vacantDelta,38376);
 assert.equal(delta.ratePoints,2.5);
 assert.throws(()=>comparableRecentChange(selectHistoricYear(2017),selectHistoricYear(2023-1)),/Cannot present|undefined/);
});
test("failed categories, missing source, or impossible census cannot pass validation",()=>{
 const broken=VACANCY_HISTORY.map((p,i)=>i===4?{...p,vacant:p.vacant+100}:p);
 assert.throws(()=>validateVacancyHistory(broken),/contract/);
 assert.throws(()=>validateVacancyHistory(VACANCY_HISTORY.map((p,i)=>i===5?{...p,series:"denombrement"}:p)),/contract/);
 assert.throws(()=>validateVacancyHistory(VACANCY_HISTORY.slice(1)),/Nine audited/);
});
