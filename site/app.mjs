import { SOURCE, normalizeBatch } from "./record.mjs";
import { renderParisTimeline } from "./timeline.mjs";
import { validateIrisImport } from "./iris-contract.mjs";
import { colorForIRIS, isReliableIRIS } from "./iris-colors.mjs";

renderParisTimeline();

const status = document.querySelector("#status");
const button = document.querySelector("#load");
const irisToggle = document.querySelector("#iris-toggle");
const irisStatus = document.querySelector("#iris-status");

if (typeof window.L === "undefined") {
  status.textContent = "Impossible de charger Leaflet : vérifiez le réseau et le CDN.";
  button.disabled = true;
  irisToggle.disabled = true;
} else {
  const map = L.map("map", { preferCanvas: true }).setView([48.855, 2.3747], 17);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "© OpenStreetMap contributors"
  }).addTo(map);
  const volumes = L.geoJSON(null, {
    style: feature => ({
      color: "#1b3742", weight: 0.7, fillOpacity: 0.8,
      fillColor: colorForFloors(feature.properties.floors_max)
    }),
    onEachFeature: (feature, layer) => layer.bindPopup(() => buildPopup(feature))
  }).addTo(map);

  const irisPolygons = L.geoJSON(null, {
    style: feature => ({
      color:"#33424c",weight:0.7,fillOpacity:0.76,
      fillColor:colorForIRIS(feature.properties)
    }),
    onEachFeature:(feature,layer)=>layer.bindPopup(()=>buildIRISPopup(feature))
  });
  let irisLoaded=false;
  irisToggle.addEventListener("change",async()=>{
    if(!irisToggle.checked){
      if(map.hasLayer(irisPolygons))map.removeLayer(irisPolygons);
      if(!map.hasLayer(volumes))volumes.addTo(map);
      button.disabled=false;
      irisStatus.textContent="Retour aux volumes bâtis actuels. Zoomez sur une rue pour les charger.";
      return;
    }
    irisToggle.disabled=true;
    button.disabled=true;
    irisStatus.textContent="Chargement des quartiers Insee 2023 et contours IGN 2025…";
    try{
      if(!irisLoaded){
        const response=await fetch("./data/iris-2023.geojson",{cache:"no-store"});
        if(!response.ok)throw new Error("fichier IRIS indisponible (HTTP "+response.status+")");
        const payload=await response.json();
        const checked=validateIrisImport(payload,payload.metadata,{forPublication:true});
        if(checked.features.length!==992)throw new Error("cardinalité IRIS inattendue");
        irisPolygons.addData(checked);
        irisLoaded=true;
      }
      if(map.hasLayer(volumes))map.removeLayer(volumes);
      irisPolygons.addTo(map);
      map.fitBounds(irisPolygons.getBounds().pad(0.025));
      let shown=0;
      irisPolygons.eachLayer(layer=>{if(isReliableIRIS(layer.feature.properties))shown++;});
      irisStatus.textContent="IRIS 2023 · 992 quartiers vérifiés · "+shown+
        " taux représentés. Gris : aucun logement ou moins de 50 logements. "+
        "Aucune information individuelle ni par bâtiment.";
    }catch(error){
      irisToggle.checked=false;
      if(!map.hasLayer(volumes))volumes.addTo(map);
      button.disabled=false;
      irisStatus.textContent="Couche IRIS non affichée : "+error.message+". Aucune donnée de secours fictive.";
    }finally{
      irisToggle.disabled=false;
    }
  });
  let busy = false;
  button.addEventListener("click", async () => {
    if (busy) return;
    busy = true;
    button.disabled = true;
    volumes.clearLayers(); // no stale overlay while reading another view
    status.textContent = "Chargement de données publiques réelles…";
    try {
      const b = map.getBounds();
      if (!b.isValid() || (b.getNorth() - b.getSouth()) > 0.018 ||
          (b.getEast() - b.getWest()) > 0.025) {
        throw new Error("Zone trop large : zoomez vers un quartier avant de charger.");
      }
      const raw = [];
      let total = null;
      // Manual request only, hard capped: never silently claim exhaustive coverage.
      for (let offset = 0; offset < 800; offset += 100) {
        const where = "in_bbox(geom_x_y," +
          [b.getSouth(), b.getWest(), b.getNorth(), b.getEast()].map(n => n.toFixed(6)).join(",") + ")";
        const params = new URLSearchParams({ limit: "100", offset: String(offset), where, order_by: "n_sq_vb" });
        const response = await fetch(SOURCE.api + "?" + params.toString(), {
          headers: { "Accept": "application/json" }
        });
        if (!response.ok) throw new Error("API Paris Data : HTTP " + response.status);
        const payload = await response.json();
        if (!Array.isArray(payload.results)) throw new Error("Schéma API inattendu (results absent).");
        if (Number.isFinite(payload.total_count)) total = payload.total_count;
        raw.push(...payload.results);
        if (payload.results.length < 100 || (total !== null && raw.length >= total)) break;
      }
      const normalized = normalizeBatch(raw);
      volumes.addData(normalized.collection);
      const truncated = total === null ? "Exhaustivité non vérifiée." :
        total > raw.length ? "ATTENTION : données tronquées (" + raw.length + "/" + total + ")." : "Pagination terminée.";
      status.textContent = normalized.collection.features.length +
        " volumes cartographiques visibles · " + normalized.rejected +
        " rejetés (géométrie / attributs) · " + normalized.duplicates +
        " doublons. " + truncated + " Lecture " + new Date().toLocaleString("fr-FR") +
        ". Données de bâtiments existants, pas de vacance.";
    } catch (error) {
      status.textContent = "Aucune couche affichée : " + error.message +
        " Vérifier réseau/CORS et la documentation API. Aucune donnée inventée.";
    } finally {
      busy = false;
      button.disabled = false;
    }
  });
}

function colorForFloors(floors) {
  if (floors === null) return "#8997a3";
  if (floors === 0) return "#b6dbbe";
  if (floors <= 3) return "#74bba7";
  if (floors <= 8) return "#e1c77b";
  return "#d98166";
}

function buildPopup(feature) {
  // All provider-controlled values go through textContent, never raw HTML.
  const root = document.createElement("div");
  root.className = "popup";
  const title = document.createElement("strong");
  title.textContent = "Volume bâti #" + feature.id;
  root.append(title);
  const lines = [
    "Arrondissement : " + feature.properties.arrondissement,
    "Nombre maximal d'étages : " +
      (feature.properties.floors_max === null ? "indisponible" : feature.properties.floors_max),
    "Hauteur en mètres : indisponible",
    "Période de construction : indisponible",
    "Vacance : aucune information à cette adresse",
    "Source : " + SOURCE.name + " · " + SOURCE.licence
  ];
  for (const line of lines) {
    const p = document.createElement("p");
    p.textContent = line;
    root.append(p);
  }
  const link = document.createElement("a");
  link.textContent = "Ouvrir la source officielle";
  link.href = SOURCE.url;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  root.append(link);
  return root;
}


function buildIRISPopup(feature){
  const p=feature.properties;
  const fmt=new Intl.NumberFormat("fr-FR",{maximumFractionDigits:0});
  const root=document.createElement("div");
  root.className="popup";
  const title=document.createElement("strong");
  title.textContent="Quartier IRIS "+p.iris_code+" · recensement 2023";
  root.append(title);
  const lines=[
    "Total de logements estimé : "+fmt.format(p.housing_count),
    "Logements vacants estimés : "+fmt.format(p.vacant_count),
    isReliableIRIS(p)?"Taux de vacance : "+p.vacancy_percent.toLocaleString("fr-FR")+" %":
      "Taux masqué : parc de moins de 50 logements ou dénominateur nul",
    "Contours IGN : géographie 2025",
    "Aucune information sur l'occupation d'un bâtiment ou d'une adresse"
  ];
  for(const line of lines){
    const paragraph=document.createElement("p");
    paragraph.textContent=line;
    root.append(paragraph);
  }
  const link=document.createElement("a");
  link.href="https://www.insee.fr/fr/statistiques/9061333";
  link.target="_blank";
  link.rel="noopener noreferrer";
  link.textContent="Source Insee RP2023";
  root.append(link);
  return root;
}
