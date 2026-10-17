import {
  VACANCY_HISTORY, validateVacancyHistory, vacancyRatePct, vacancyFraction,
  comparableRecentChange, selectHistoricYear
} from "./evolution-data.mjs";

const NS="http://www.w3.org/2000/svg";
const fmt=new Intl.NumberFormat("fr-FR");
const rateFmt=new Intl.NumberFormat("fr-FR",{minimumFractionDigits:1,maximumFractionDigits:1});
const svg=document.querySelector("#evolution-chart");
const tbody=document.querySelector("#evolution-table");
const status=document.querySelector("#chart-status");
const recent=document.querySelector("#recent-change");
const modeRate=document.querySelector("#metric-rate");
const modeCount=document.querySelector("#metric-count");

function element(type,attrs={},label=""){
  const el=document.createElementNS(NS,type);
  for(const [key,value] of Object.entries(attrs))el.setAttribute(key,String(value));
  if(label)el.textContent=label;
  return el;
}
function draw(metric){
  const isRate=metric==="rate";
  for(const old of [...svg.children]){
    if(old.nodeName.toLowerCase()!=="title"&&old.nodeName.toLowerCase()!=="desc")old.remove();
  }
  const top=55,bottom=273,barMax=bottom-top,unitMax=isRate?12:160000;
  const latest=VACANCY_HISTORY.at(-1);
  const values=VACANCY_HISTORY.map(p=>isRate?vacancyRatePct(p):p.vacant);
  svg.append(element("line",{x1:54,y1:bottom,x2:900,y2:bottom,class:"axis"}));
  const mid=54+105*4.5;
  svg.append(element("line",{x1:mid,y1:32,x2:mid,y2:bottom+23,class:"break"}));
  svg.append(element("text",{x:mid,y:23,"text-anchor":"middle"},"Changement de méthode"));
  svg.append(element("text",{x:262,y:327,"text-anchor":"middle"},"Dénombrements anciens"));
  svg.append(element("text",{x:705,y:327,"text-anchor":"middle"},"Recensements rénovés"));
  for(let i=0;i<VACANCY_HISTORY.length;i++){
    const p=VACANCY_HISTORY[i],v=values[i],x=60+i*105;
    const height=Math.max(1,Math.round(v/unitMax*barMax)),y=bottom-height;
    const bar=element("rect",{x:x-19,y,width:38,height,rx:2,
      class:"bar"+(p.series==="denombrement"?" old":"")+(p.year===latest.year?" highlight":"")});
    bar.append(element("title",{},p.year+" : "+fmt.format(p.vacant)+" logements vacants sur "+
      fmt.format(p.total)+" ("+rateFmt.format(vacancyRatePct(p))+" %)"));
    svg.append(bar);
    svg.append(element("text",{x,y:Math.max(46,y-9),"text-anchor":"middle",class:"value"},
      isRate?rateFmt.format(v)+" %":Math.round(v/1000)+" k"));
    svg.append(element("text",{x,y:bottom+25,"text-anchor":"middle"},String(p.year)));
  }
  modeRate.setAttribute("aria-pressed",String(isRate));
  modeCount.setAttribute("aria-pressed",String(!isRate));
  status.textContent=isRate?
    "Taux = logements vacants / ensemble des logements, à Paris. Les chiffres exacts sont dans le tableau.":
    "Nombre estimé de logements vacants à Paris. Les barres ne représentent pas une année intermédiaire.";
}

try {
  validateVacancyHistory(VACANCY_HISTORY);
  tbody.replaceChildren();
  for(const p of VACANCY_HISTORY){
    const tr=document.createElement("tr");
    if(p.year===2007)tr.className="break-row";
    const cols=[
      String(p.year),fmt.format(p.vacant),fmt.format(p.total),
      rateFmt.format(vacancyRatePct(p))+" %",fmt.format(p.secondaryOccasional),
      p.series==="rp"?"Recensement rénové":"Dénombrement historique"
    ];
    for(const [i,label] of cols.entries()){
      const cell=document.createElement(i===0?"th":"td");
      if(i===0)cell.scope="row";
      cell.textContent=label;
      tr.append(cell);
    }
    tbody.append(tr);
  }
  const old=selectHistoricYear(2012),now=selectHistoricYear(2023);
  const delta=comparableRecentChange(old,now);
  recent.textContent="Entre les recensements rénovés de 2012 et 2023, "+
    fmt.format(delta.vacantDelta)+" logements vacants de plus et "+
    (delta.ratePoints>0?"+":"")+rateFmt.format(delta.ratePoints)+
    " points de taux. Variation statistique du parc, pas nombre de logements identifiés comme devenus vacants.";
  modeRate.addEventListener("click",()=>draw("rate"));
  modeCount.addEventListener("click",()=>draw("count"));
  draw("rate");
}catch(e){
  status.textContent="Données historiques non affichées : "+e.message;
  modeRate.disabled=true;modeCount.disabled=true;
}
