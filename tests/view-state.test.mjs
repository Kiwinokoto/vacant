import {test} from "node:test";
import assert from "node:assert/strict";
import {viewDescriptor} from "../site/view-state.mjs";

test("map title reflects current layer, never implying vacant buildings",()=>{
  const building=viewDescriptor("building");
  assert.match(building.title,/volumes bâtis actuels/);
  assert.match(building.subtitle,/aucun statut de vacance/);
  const iris=viewDescriptor("iris",2011);
  assert.match(iris.title,/2023/); // IRIS map is always 2023 even if a timeline click precedes it
  assert.match(iris.subtitle,/géographie 2025/);
});
test("historic map labels separate census year and geometry vintage",()=>{
  for(const [rp,geo] of [[2006,2008],[2011,2013],[2016,2018],[2023,2025]]){
    const v=viewDescriptor("arrondissement",rp);
    assert.match(v.title,new RegExp(String(rp)));
    assert.match(v.subtitle,new RegExp("géographie "+geo));
    assert.match(v.subtitle,/limites d'arrondissement IGN 2025/);
  }
  assert.throws(()=>viewDescriptor("arrondissement",2018),/unsupported/);
  assert.throws(()=>viewDescriptor("other"),/unknown/);
});
