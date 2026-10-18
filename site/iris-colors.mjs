// Pure map rendering categories. Never infer vacancy at building level.
export function isReliableIRIS(p) {
  return p && Number.isFinite(p.vacancy_percent) && Number.isFinite(p.housing_count) &&
    p.housing_count >= 50 && p.status === "statistique_agregee";
}
// Use the UNROUNDED ratio for class boundaries when source counts are available.
// Popup vacancy_percent remains rounded for display; classification must not round first.
export function rawVacancyPercent(p){
  if (Number.isFinite(p?.vacant_count) && p.vacant_count>=0 &&
      Number.isFinite(p?.housing_count) && p.housing_count>0 &&
      p.vacant_count<=p.housing_count) return 100*p.vacant_count/p.housing_count;
  return p?.vacancy_percent;
}
export function colorForIRIS(p) {
  if (!isReliableIRIS(p)) return "#8997a3";
  const r=rawVacancyPercent(p);
  if (r<5) return "#74c3aa";
  if (r<8) return "#80a8cf";
  if (r<12) return "#e5c97c";
  if (r<20) return "#dd9875";
  return "#b8647c";
}
