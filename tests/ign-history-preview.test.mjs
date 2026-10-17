import test from "node:test";
import assert from "node:assert/strict";
import {enabled,parseSnapshot,compareIds,YEARS} from "../experiments/ign-history/contract.mjs";
const poly={type:"Polygon",coordinates:[[[2.373,48.854],[2.374,48.854],[2.374,48.855],[2.373,48.855],[2.373,48.854]]]};
const snapshot=(year,id="BATIMENT0000000000155000")=>({type:"FeatureCollection",metadata:{
 private_research_only:true,not_a_historical_presence_assertion:true,edition:year,source_crs:"EPSG:2154",output_crs:"EPSG:4326"
},features:[{type:"Feature",geometry:poly,properties:{feature_id:id,kind:"INDIFFERENCIE",date_edition:year,height_raw:15}}]});
test("historical maps work on localhost only with deliberate opt-in",()=>{
 assert.equal(enabled({hostname:"vacant.kiwinokoto.fr",search:"?ign_lab=1"}),false);
 assert.equal(enabled({hostname:"localhost",search:"?ign_lab=1"}),true);
 assert.equal(enabled({hostname:"localhost",search:""}),false);
});
test("only pinned 2011 and 2018 research editions are accepted",()=>{
 assert.deepEqual(YEARS,["2011-04-12","2018-03-29"]);
 assert.equal(parseSnapshot(snapshot("2011-04-12"),"2011-04-12").features.length,1);
 assert.throws(()=>parseSnapshot(snapshot("2008-09-14"),"2008-09-14"),/provenance/);
});
test("rejects unsupported historical interpretation and invalid coordinates",()=>{
 const data=snapshot("2018-03-29");
 assert.throws(()=>parseSnapshot({...data,metadata:{...data.metadata,not_a_historical_presence_assertion:false}},"2018-03-29"),/provenance/);
 data.features[0].geometry.coordinates[0][1]=[999,999];
 assert.throws(()=>parseSnapshot(data,"2018-03-29"),/anneau/);
});
test("ID difference does not claim physical construction/demolition",()=>{
 const a=snapshot("2011-04-12"),b=snapshot("2018-03-29","BATIMENT0000000000155001");
 const x=compareIds(a,b);
 assert.equal(x.shared,0);
 assert.equal(x.onlyFirst,1);
 assert.equal(x.onlySecond,1);
 assert.match(x.warning,/preuve de démolition/);
});
