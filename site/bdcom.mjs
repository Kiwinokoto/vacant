import {validateBDCOM,rankBDCOM,MODE_LABELS} from "./bdcom-contract.mjs";
const $=id=>document.getElementById(id);
const fmt=new Intl.NumberFormat("fr-FR");
const pc=n=>n.toLocaleString("fr-FR",{minimumFractionDigits:1,maximumFractionDigits:1})+" %";
const field=$("bdcom-sort"),status=$("bdcom-status"),tbody=$("bdcom-rows");
const cell=(tag,text)=>{const el=document.createElement(tag);el.textContent=text;return el};
function redraw(d){
 const mode=field.value;
 const rows=rankBDCOM(d,mode);
 tbody.replaceChildren();
 for(const item of rows){
  const tr=document.createElement("tr");
  const head=cell("th",item.arrondissement+"e");head.scope="row";
  tr.append(head,cell("td",fmt.format(item.surveyed)),cell("td",fmt.format(item.vacant)),
   cell("td",fmt.format(item.in_works)),cell("td",pc(100*item.vacant/item.surveyed)));
  tbody.append(tr);
 }
 status.textContent="20 arrondissements classés par "+MODE_LABELS[mode]+" ; "+
  "Paris : 7 495 vacants hors travaux, 1 565 en travaux, sur 83 154 locaux BDCOM étudiés. "+
  "Ces valeurs n'établissent aucun lieu immédiatement habitable.";
}
try{
 const res=await fetch("./data/bdcom-paris-arrond-2023.json",{cache:"no-store"});
 if(!res.ok)throw Error("agrégats BDCOM indisponibles (HTTP "+res.status+")");
 const data=validateBDCOM(await res.json());
 field.addEventListener("change",()=>redraw(data));
 redraw(data);
}catch(error){
 status.textContent="BDCOM indisponible : "+error.message+" ; aucune estimation de remplacement inventée.";
 tbody.replaceChildren();field.disabled=true;
}