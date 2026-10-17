import {checkLovac,years} from "./lovac-public-contract.mjs";
const fmt=new Intl.NumberFormat("fr-FR");
const $=id=>document.getElementById(id);
const status=$("lovac-status"),bars=$("lovac-bars");
let dataset=null,metric="vacant";
function cell(tag,content){const e=document.createElement(tag);e.textContent=content;return e}
function draw(){
 const values=dataset.years.map(x=>x.paris[metric]);
 const maximum=Math.max(...values);
 bars.replaceChildren();
 for(let i=0;i<years.length;i++){
  const year=years[i],p=dataset.years[i],count=values[i];
  const col=cell("div","");
  col.className="lovac-column "+(year<2024?"old":year===2024?"transition":"new");
  col.append(cell("strong",fmt.format(count)));
  const bar=cell("div","");
  bar.className="lovac-bar";
  bar.style.height=Math.round(count/maximum*150)+"px";
  bar.title=fmt.format(count)+" logements, millésime "+year+
    ", observation "+p.date_by_variable[metric];
  col.append(bar,cell("small",String(year)));
  bars.append(col);
 }
 const title=metric==="vacant"?"Logements vacants privés":"Logements privés vacants depuis plus de deux ans";
 bars.setAttribute("aria-label",title+": "+values.map((n,i)=>years[i]+" = "+fmt.format(n)).join(", ")+
   ". Rupture GMBI à partir de 2024.");
 $("metric-vacant").setAttribute("aria-pressed",String(metric==="vacant"));
 $("metric-long").setAttribute("aria-pressed",String(metric==="long"));
 status.textContent=title+" · chiffres fiscaux par millésime de production, sans comparaison causale à travers la rupture GMBI.";
}
function table(){
 const year=Number($("lovac-year").value);
 const point=dataset.years[year-2020];
 const ref=point.date_by_variable;
 $("lovac-reference").textContent="Millésime LOVAC "+year+
  " · tous vacants : situation au "+ref.vacant+
  " ; longue durée : situation au "+ref.long+
  (ref.stock?" ; parc privé total : situation au "+ref.stock:" ; pas de dénominateur 2026 disponible.")+
  ". Ces dates ne coïncident pas toujours.";
 const body=$("lovac-districts");body.replaceChildren();
 for(const district of dataset.arrondissements){
  const tr=document.createElement("tr"),data=district.series[String(year)];
  const head=cell("th",district.arrondissement+"e");head.scope="row";
  tr.append(head,cell("td",fmt.format(data.vacant)),cell("td",fmt.format(data.long)));
  body.append(tr);
 }
}
try{
 const response=await fetch("./data/lovac-paris-open-2026.json",{cache:"no-store"});
 if(!response.ok)throw Error("Agrégats indisponibles (HTTP "+response.status+")");
 dataset=checkLovac(await response.json());
 for(const button of ["vacant","long"]){
  $("metric-"+button).addEventListener("click",()=>{metric=button;draw()});
 }
 $("lovac-year").addEventListener("change",table);
 draw();table();
}catch(e){
 status.textContent="LOVAC non affiché : "+e.message;
 $("lovac-year").disabled=true;
 $("metric-vacant").disabled=true;$("metric-long").disabled=true;
}