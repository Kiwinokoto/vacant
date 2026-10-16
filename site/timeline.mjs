// Public, aggregate Paris-wide census figures manually transcribed on 2026-10-16.
// Never join these citywide statistics to a building or IRIS feature.
const SOURCE_2022 = "https://www.insee.fr/fr/statistiques/8581193?geo=DEP-75";
const SOURCE_2023 = "https://www.insee.fr/fr/statistiques/2011101?geo=DEP-75";
export const TIMELINE = Object.freeze([
  Object.freeze({year:2006, total:1334814, primary:1131810, secondaryOccasional:80337, vacant:122667,source:SOURCE_2022,geography:"Paris (75), périmètre constant – tableau RP2022"}),
  Object.freeze({year:2011, total:1356074, primary:1165541, secondaryOccasional:91835, vacant:98698,source:SOURCE_2022,geography:"Paris (75), périmètre constant – tableau RP2022"}),
  Object.freeze({year:2016, total:1374377, primary:1140127, secondaryOccasional:119943, vacant:114306,source:SOURCE_2022,geography:"Paris (75), périmètre constant – tableau RP2022"}),
  Object.freeze({year:2023, total:1402024, primary:1124522, secondaryOccasional:138426, vacant:139075,source:SOURCE_2023,geography:"Paris (75), périmètre constant – tableau RP2023 harmonisé"})
]);

export function validateTimeline(rows) {
  if (!Array.isArray(rows) || rows.length < 2) throw new Error("timeline needs at least two audited observations");
  const seen = new Set();
  for (let i = 0; i < rows.length; i++) {
    const v = rows[i];
    if (!Number.isInteger(v.year) || seen.has(v.year) || (i > 0 && v.year - rows[i-1].year < 5)) {
      throw new Error("duplicated, unordered or too-close census years");
    }
    seen.add(v.year);
    if (["total","primary","secondaryOccasional","vacant"].some(k=>!Number.isInteger(v[k]) || v[k]<0) ||
      v.total === 0 || Math.abs(v.primary+v.secondaryOccasional+v.vacant-v.total)>1) {
      throw new Error("invalid aggregate or category total");
    }
    if (!v.source?.startsWith("https://www.insee.fr/")) throw new Error("source missing");
  }
  return true;
}

export function vacancyRate(point) {
  return Math.round(1000 * point.vacant / point.total) / 10;
}

export function selectYear(year) {
  const point = TIMELINE.find(p=>p.year===year);
  if (!point) throw new RangeError("undocumented year");
  return point;
}

export function renderParisTimeline() {
  validateTimeline(TIMELINE);
  const area = document.querySelector("#timeline-years");
  const rate = document.querySelector("#timeline-rate");
  const count = document.querySelector("#timeline-count");
  const other = document.querySelector("#timeline-other");
  const coverage = document.querySelector("#timeline-coverage");
  const source = document.querySelector("#timeline-source");
  const fill = document.querySelector("#timeline-fill");
  const format = new Intl.NumberFormat("fr-FR");
  const buttons = [];
  function update(point) {
    rate.textContent = format.format(vacancyRate(point)) + " %";
    count.textContent = format.format(point.vacant);
    other.textContent = format.format(point.secondaryOccasional) +
      " résidences secondaires et logements occasionnels (catégorie distincte). Parc total : " +
      format.format(point.total) + " logements.";
    coverage.textContent = "Recensement " + point.year + " · " + point.geography +
      ". Aucune donnée d'occupation par bâtiment.";
    source.href = point.source;
    fill.style.width = vacancyRate(point) + "%";
    for (const {button, year} of buttons) button.setAttribute("aria-pressed", String(point.year===year));
    document.dispatchEvent(new CustomEvent("vacant:census-year", {detail:{year:point.year}}));
  }
  for (const point of TIMELINE) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = String(point.year);
    button.setAttribute("aria-pressed","false");
    button.setAttribute("aria-label","Afficher les statistiques pour " + point.year);
    button.addEventListener("click",()=>update(point));
    area.append(button);
    buttons.push({year:point.year,button});
  }
  update(TIMELINE[TIMELINE.length-1]);
}
