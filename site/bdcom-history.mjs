import {historyRows} from "./bdcom-history-contract.mjs";
const fmt=new Intl.NumberFormat("fr-FR");
const root=document.getElementById("bdcom-history-bars");
const tbody=document.getElementById("bdcom-history-rows");
const status=document.getElementById("bdcom-history-status");
const node=(tag,text)=>{const el=document.createElement(tag);el.textContent=text;return el;};
try {
 const response=await fetch("./data/bdcom-paris-history-2017-2023.json",{cache:"no-store"});
 if(!response.ok)throw Error("HTTP "+response.status);
 const rows=historyRows(await response.json());
 const ceiling=Math.max(...rows.map(x=>x.combined));
 root.replaceChildren();tbody.replaceChildren();
 for(const entry of rows){
  const line=node("div","");line.className="bdcom-history-line";
  line.append(node("strong",String(entry.year)));
  const chart=node("div","");chart.className="bdcom-history-bar";
  const a=node("span","");a.className="bdcom-history-vacant";
  const b=node("span","");b.className="bdcom-history-works";
  a.style.width=(entry.vacant/ceiling*100).toFixed(5)+"%";
  b.style.width=(entry.in_works/ceiling*100).toFixed(5)+"%";
  chart.append(a,b);
  line.append(chart,node("strong",fmt.format(entry.combined)));root.append(line);
  const tr=document.createElement("tr");
  for(const [i,value] of [entry.year,entry.vacant,entry.in_works,entry.combined].entries())tr.append(node("td",i===0?String(value):fmt.format(value)));
  tbody.append(tr);
 }
 status.textContent="Trois éditions recensées : 2017, 2020, 2023 · effectifs et non taux harmonisés · sources Apur.";
}catch(error){
 status.textContent="Comparaison BDCOM indisponible : "+error.message+". Aucune interpolation ni estimation de remplacement.";
 root.replaceChildren();tbody.replaceChildren();
}
