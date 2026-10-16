import {test} from "node:test";
import assert from "node:assert/strict";
import {colorForIRIS,isReliableIRIS} from "../site/iris-colors.mjs";
test("missing, zero and small denominators are neutral",()=>{
  for(const n of [0,5,49]) {
    const p={vacancy_percent:60,housing_count:n,status:"statistique_agregee"};
    assert.equal(isReliableIRIS(p),false);
    assert.equal(colorForIRIS(p),"#8997a3");
  }
  assert.equal(colorForIRIS({vacancy_percent:null,housing_count:200,status:"indisponible"}),"#8997a3");
});
test("statistical classes have distinct boundaries",()=>{
  const p=n=>({vacancy_percent:n,housing_count:600,status:"statistique_agregee"});
  for(const [a,b] of [[4.9,5],[7.9,8],[11.9,12],[19.9,20]]) assert.notEqual(colorForIRIS(p(a)),colorForIRIS(p(b)));
});
