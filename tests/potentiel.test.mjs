import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
const html=readFileSync(new URL("../site/potentiel.html",import.meta.url),"utf8");
const index=readFileSync(new URL("../site/index.html",import.meta.url),"utf8");
const lovac=readFileSync(new URL("../site/lovac.html",import.meta.url),"utf8");
const evolution=readFileSync(new URL("../site/evolution.html",import.meta.url),"utf8");
test("Each official aggregate has a separate perimeter and source",()=>{
 for(const s of ["139 075","1 402 024","105 785","1er janvier 2025","9 059","9 060","7 495","1 565","83 154","10,9 %","8p236_bdcom_2023.pdf","Ces chiffres ne s'additionnent pas"])assert.ok(html.includes(s),s);
});
test("Potential is not a measured immediately usable shelter count",()=>{
 for(const s of ["Nombre actuellement inconnu","état inconnu","sécurité","autorisations","Ni « habitable » ni « impropre »","aucun calcul de logements « disponibles »"])assert.ok(html.includes(s),s);
});
test("Nonresidential premises never silently become dwelling statistics",()=>{
 for(const s of ["Bureau inoccupé","Local commercial vacant","bureaux en étage","pas de décompte en nombre de bureaux"])assert.ok(html.includes(s),s);
});
test("The new page is navigable from VACANT's exploration pages",()=>{
 for(const page of [index,lovac,evolution])assert.ok(page.includes('href="./potentiel.html"'));
 assert.ok(html.includes('aria-current="page"'));
 assert.ok(html.includes('id="bdcom-sort"')&&html.includes('id="bdcom-rows"'));
 assert.ok(html.includes("bdcom.mjs"));
});

test("2026 preliminary Apur snapshot remains separate from the audited 2017–2023 API series",()=>{
 for(const fact of ["83 115 locaux","9 725 locaux vacants","1 402 en travaux","8 323 vacants hors travaux","11,7 % avec travaux","10,0 % hors travaux","83 284 locaux et 9 104 vacants","repère éditorial préliminaire","12p296_Commerces_Paris_tendances_enquete_2026.pdf"])assert.ok(html.includes(fact),fact);
 const sep=html.indexOf('id="bdcom-2026-heading"');
 const old=html.indexOf('id="bdcom-history-heading"');
 assert.ok(sep>0 && old>sep,"2026 editorial snapshot must precede and remain separate from historical API figures");
});

test("Definition separates Insee vacancy, secondary residences, fiscal long vacancy and mobilisable supply",()=>{
 for(const term of [
   'id="vacance-definition-title"',
   'Vacant ne signifie ni habitable ni mobilisable',
   'vacance de rotation (frictionnelle)',
   '138 426 (9,9 %)',
   '277 501 logements, soit 19,8 %',
   'pas classés vacants',
   '26 264 (situation au 01/01/2025)',
   'Logements immédiatement mobilisables',
   '<strong>Inconnu</strong>',
   'Pas de multiplication automatique par deux ou trois',
   '18 648 logements durablement vacants',
   '43 % étaient des logements',
   '44 % faisaient moins de 30 m²',
   'surface médiane 32 m²',
   'ne peut pas être appliquée mécaniquement à LOVAC 2026'
 ]) assert.ok(html.includes(term),term);
});
test("Latest Paris office offer is not portrayed as dwelling or durable physical vacancy",()=>{
 for(const term of [
   '1 578 000 m²','fin septembre 2026',
   'reactions-immostat-t3-2026',
   'pas surface physiquement inoccupée depuis longtemps',
   'sans évolution trimestrielle harmonisée établie'
 ])assert.ok(html.includes(term),term);
});
