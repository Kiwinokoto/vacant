import { test } from "node:test";
import assert from "node:assert/strict";
import { TIMELINE, validateTimeline, vacancyRate, selectYear } from "../site/timeline.mjs";

test("only documented RP milestones; comparable gaps", () => {
  assert.deepEqual(TIMELINE.map(p=>p.year),[2006,2011,2016,2023]);
  assert.equal(validateTimeline(TIMELINE),true);
  assert.throws(()=>selectYear(2019),/undocumented/);
});
test("2006–2023 Insee citywide source remains traceable", () => {
  for (const point of TIMELINE) {
    assert.ok(point.source.startsWith("https://www.insee.fr/"));
    assert.match(point.geography,/Paris \(75\)/);
    assert.equal(Object.hasOwn(point,"iris"),false);
    assert.equal(Object.hasOwn(point,"building_id"),false);
  }
  assert.equal(selectYear(2023).vacant,139075);
  assert.equal(selectYear(2023).secondaryOccasional,138426);
  assert.equal(selectYear(2006).total,1334814);
});
test("rates computed from original denominators, distinct secondary homes",()=>{
  assert.equal(vacancyRate(selectYear(2006)),9.2);
  assert.equal(vacancyRate(selectYear(2011)),7.3);
  assert.equal(vacancyRate(selectYear(2016)),8.3);
  assert.equal(vacancyRate(selectYear(2023)),9.9);
});
test("reject fake interpolated years and inconsistent categories",()=>{
  assert.throws(()=>validateTimeline([...TIMELINE.slice(0,1),{...TIMELINE[1],year:2008},...TIMELINE.slice(2)]),/too-close/);
  assert.throws(()=>validateTimeline(TIMELINE.map((p,i)=>i===1?{...p,vacant:p.vacant+30}:p)),/category total/);
});
