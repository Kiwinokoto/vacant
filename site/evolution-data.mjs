// INSEE LOG T1: Paris (75), official housing-category counts, geography as in RP2023.
// Historical enumeration 1968–1999 and rolling census (RP) 2007–2023 MUST be labelled separately.
// NOT annual observations; not IRIS and not a register of individually vacant dwellings.
export const INSEE_SOURCE = "https://www.insee.fr/fr/statistiques/2011101?geo=DEP-75";
export const VACANCY_HISTORY = Object.freeze([
  [1968,1221954,1152953,28102,40899,"denombrement"],
  [1975,1238732,1113295,37580,87857,"denombrement"],
  [1982,1279730,1114400,53369,111961,"denombrement"],
  [1990,1304428,1095090,91777,117561,"denombrement"],
  [1999,1323464,1111721,75725,136018,"denombrement"],
  [2007,1336209,1139192,80931,116087,"rp"],
  [2012,1357081,1159105,97276,100699,"rp"],
  [2017,1382779,1141623,124073,117082,"rp"],
  [2023,1402024,1124522,138426,139075,"rp"],
].map(([year,total,primary,secondaryOccasional,vacant,series])=>
  Object.freeze({year,total,primary,secondaryOccasional,vacant,series,source:INSEE_SOURCE})));

export function validateVacancyHistory(rows) {
  if(!Array.isArray(rows)||rows.length!==9) throw new Error("Nine audited census milestones required");
  const years=[1968,1975,1982,1990,1999,2007,2012,2017,2023];
  for(const [i,r] of rows.entries()){
    if(r.year!==years[i] || !["denombrement","rp"].includes(r.series) ||
      r.series!==(r.year<2000?"denombrement":"rp") ||
      ["total","primary","secondaryOccasional","vacant"].some(k=>!Number.isInteger(r[k])||r[k]<0) ||
      r.total<1 || r.vacant>r.total ||
      Math.abs(r.primary+r.secondaryOccasional+r.vacant-r.total)>1 ||
      r.source!==INSEE_SOURCE)throw new Error("Census year/category/provenance contract broken");
  }
  return true;
}

export const vacancyFraction = p=>p.vacant/p.total;
export function vacancyRatePct(p){
  return Math.round(vacancyFraction(p)*1000)/10;
}
export function selectHistoricYear(year){
  const found=VACANCY_HISTORY.find(p=>p.year===year);
  if(!found)throw new RangeError("Unpublished historic census year");
  return found;
}
export function comparableRecentChange(first,second) {
  // RP statistical comparison needs >= 5 census years; RP2019–2023 Covid requires >= 6.
  if(first.series!=="rp"||second.series!=="rp"||
      second.year-first.year<5 ||
      (second.year===2023 && second.year-first.year<6)){
    throw new RangeError("Cannot present a comparable RP trend across old methods or close years");
  }
  return Object.freeze({
    vacantDelta:second.vacant-first.vacant,
    ratePoints:Math.round((vacancyFraction(second)-vacancyFraction(first))*10000)/100
  });
}
