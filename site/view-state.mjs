// Labels reflect what the *map* actually shows, not the latest citywide RP value.
const GEOGRAPHIES = Object.freeze({2006:2008,2011:2013,2016:2018,2023:2025});
export function viewDescriptor(layer,year=2023){
  if(layer==="building")return {
    title:"Carte des volumes bâtis actuels",
    subtitle:"Ville de Paris · étages (pas une hauteur en mètres) · aucun statut de vacance",
  };
  if(layer==="iris")return {
    title:"Vacance résidentielle · IRIS 2023",
    subtitle:"Insee RP2023 · contours IGN, géographie 2025 · estimations par quartier",
  };
  if(layer==="arrondissement"){
    if(!Object.hasOwn(GEOGRAPHIES,year))throw new RangeError("unsupported historical census year");
    return {
      title:"Vacance résidentielle · arrondissements · "+year,
      subtitle:"Insee RP"+year+" (IRIS géographie "+GEOGRAPHIES[year]+") · limites d'arrondissement IGN 2025",
    };
  }
  throw new RangeError("unknown map layer");
}
