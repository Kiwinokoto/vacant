// Pure map rendering categories. Never infer vacancy at building level.
export function isReliableIRIS(p) {
  return p && Number.isFinite(p.vacancy_percent) && Number.isFinite(p.housing_count) &&
    p.housing_count >= 50 && p.status === "statistique_agregee";
}
export function colorForIRIS(p) {
  if (!isReliableIRIS(p)) return "#8997a3";
  const r=p.vacancy_percent;
  if (r<5) return "#74c3aa";
  if (r<8) return "#80a8cf";
  if (r<12) return "#e5c97c";
  if (r<20) return "#dd9875";
  return "#b8647c";
}
