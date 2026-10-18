import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
const html=readFileSync(new URL("../site/potentiel.html",import.meta.url),"utf8");
const index=readFileSync(new URL("../site/index.html",import.meta.url),"utf8");
const lovac=readFileSync(new URL("../site/lovac.html",import.meta.url),"utf8");
const evolution=readFileSync(new URL("../site/evolution.html",import.meta.url),"utf8");
test("Each official aggregate has a separate perimeter and source",()=>{
 for(const s of ["139 075","1 402 024","105 785","1er janvier 2025","9 059","83 154","10,9 %","8p236_bdcom_2023.pdf","Ces chiffres ne s'additionnent pas"])assert.ok(html.includes(s),s);
});
test("Potential is not a measured immediately usable shelter count",()=>{
 for(const s of ["Nombre actuellement inconnu","état inconnu","sécurité","autorisations","Ni « habitable » ni « impropre »","aucun calcul de logements « disponibles »"])assert.ok(html.includes(s),s);
});
test("Nonresidential premises never silently become dwelling statistics",()=>{
 for(const s of ["Bureau inoccupé","Local commercial vacant","bureaux en étage","Pas encore de décompte parisien comparable validé"])assert.ok(html.includes(s),s);
});
test("The new page is navigable from VACANT's exploration pages",()=>{
 for(const page of [index,lovac,evolution])assert.ok(page.includes('href="./potentiel.html"'));
 assert.ok(html.includes('aria-current="page"'));
});
