import { SOURCE, normalizeBatch } from "./record.mjs";
import { renderParisTimeline } from "./timeline.mjs";
import { statForYear, validateArrondissementSeries, buildArrondissementPopup } from "./arrondissement-history.mjs";
import { validateIrisImport } from "./iris-contract.mjs";
import { colorForIRIS, isReliableIRIS } from "./iris-colors.mjs";
import { summarizeIrisVacancy2023 } from "./iris-insights.mjs";
import { viewDescriptor } from "./view-state.mjs";
import { labEnabled } from "./apur-lab-contract.mjs";

renderParisTimeline();

const status = document.querySelector("#status");
const button = document.querySelector("#load");
const irisToggle = document.querySelector("#iris-toggle");
const irisStatus = document.querySelector("#iris-status");
const irisInsights = document.querySelector("#iris-insights");
const arrondToggle = document.querySelector("#arrond-toggle");
const arrondStatus = document.querySelector("#arrond-status");
let selectedYear = 2023;
function showMapMode(layer){
  const copy=viewDescriptor(layer,selectedYear);
  document.querySelector("#map-title").textContent=copy.title;
  document.querySelector("#map-subtitle").textContent=copy.subtitle;
}

if (typeof window.L === "undefined") {
  status.textContent = "Impossible de charger Leaflet : vérifiez le réseau et le CDN.";
  button.disabled = true;
  irisToggle.disabled = true;
  arrondToggle.disabled = true;
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
  const arrondissementPolygons = L.geoJSON(null, {
    style: feature => ({
      color:"#33424c", weight:1.2, fillOpacity:0.73,
      fillColor:colorForIRIS(statForYear(feature.properties, selectedYear))
    }),
    onEachFeature:(feature,layer)=>layer.bindPopup(()=>buildArrondissementPopup(feature,selectedYear))
  });
  let historyLoaded=false;
  let irisLoaded=false;
  let savedStreetView=null;
  function saveStreetView(){
    if(!savedStreetView) savedStreetView={center:map.getCenter(),zoom:map.getZoom()};
  }
  function restoreStreetView(){
    if(savedStreetView) {
      map.setView(savedStreetView.center,savedStreetView.zoom);
      savedStreetView=null;
    }
  }
  function updateHistoryView(){
    arrondissementPolygons.setStyle(feature=>({
      color:"#33424c",weight:1.2,fillOpacity:0.73,
      fillColor:colorForIRIS(statForYear(feature.properties,selectedYear))
    }));
    arrondStatus.textContent="Recensement "+selectedYear+" · 20 arrondissements. "+
      "Statistiques calculées sur les IRIS de l'époque ; limites d'arrondissement affichées sur le fond IGN 2025. "+
      "Aucun taux de vacance attribué à un immeuble ou à un IRIS d'une autre année.";
    showMapMode("arrondissement");
  }
  async function loadHistory(){
    if(historyLoaded)return;
    const response=await fetch("./data/arrond-history.geojson",{cache:"no-store"});
    if(!response.ok)throw new Error("fichier historique indisponible (HTTP "+response.status+")");
    const dataset=await response.json();
    validateArrondissementSeries(dataset);
    arrondissementPolygons.addData(dataset);
    historyLoaded=true;
  }
  document.addEventListener("vacant:census-year",event=>{
    selectedYear=event.detail.year;
    if(arrondToggle.checked && historyLoaded) updateHistoryView();
    // An old-year selection cannot be applied to contemporary IRIS polygons.
    if(irisToggle.checked && selectedYear!==2023){
      arrondToggle.checked=true;
      arrondToggle.dispatchEvent(new Event("change"));
    }
  });
  arrondToggle.addEventListener("change",async()=>{
    if(!arrondToggle.checked){
      map.removeLayer(arrondissementPolygons);
      if(!irisToggle.checked){
        volumes.addTo(map);
        restoreStreetView();
        button.disabled=false;
      }
      arrondStatus.textContent="Carte d'arrondissements désactivée. Les volumes bâtis décrivent uniquement l'état actuel.";
      if(!irisToggle.checked)showMapMode("building");
      return;
    }
    arrondToggle.disabled=true;
    button.disabled=true;
    arrondStatus.textContent="Vérification des recensements Insee 2006, 2011, 2016 et 2023…";
    try{
      await loadHistory();
      saveStreetView();
      irisToggle.checked=false;
      irisInsights.hidden=true;
      map.removeLayer(irisPolygons);
      map.removeLayer(volumes);
      arrondissementPolygons.addTo(map);
      map.fitBounds(arrondissementPolygons.getBounds().pad(0.025));
      updateHistoryView();
    }catch(error){
      arrondToggle.checked=false;
      if(irisToggle.checked && map.hasLayer(irisPolygons)){
        map.removeLayer(volumes);
        showMapMode("iris");
      }else{
        if(!map.hasLayer(volumes))volumes.addTo(map);
        restoreStreetView();
        button.disabled=false;
        showMapMode("building");
      }
      arrondStatus.textContent="Carte historique indisponible : "+error.message+". Aucune géométrie de substitution inventée.";
    }finally{
      arrondToggle.disabled=false;
    }
  });
  irisToggle.addEventListener("change",async()=>{
    if(!irisToggle.checked){
      irisInsights.hidden=true;
      if(map.hasLayer(irisPolygons))map.removeLayer(irisPolygons);
      if(!map.hasLayer(volumes) && !arrondToggle.checked)volumes.addTo(map);
      if(!arrondToggle.checked)restoreStreetView();
      button.disabled=false;
      irisStatus.textContent="Retour aux volumes bâtis actuels, au cadrage précédent.";
      if(!arrondToggle.checked)showMapMode("building");
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
        // Aggregate counts and the 9.9% weighted city baseline are checked
        // independently against the published Insee Paris LOG T1 totals.
        const insights=summarizeIrisVacancy2023(checked);
        document.querySelector("#iris-insights").textContent=
          "Lecture des quartiers 2023 : "+insights.atLeastFive+" des "+
          insights.visible+" IRIS à taux affichable sont à au moins 5 % de vacance ; "+
          insights.atLeastTwelve+" sont à au moins 12 %. "+
          insights.hidden+" autres IRIS restent grisés (moins de 50 logements). "+
          "Pour Paris entier : "+insights.parisRate.toLocaleString("fr-FR")+
          " % des logements, taux pondéré sur le parc total, pas moyenne des quartiers. "+
          "Les quartiers ne représentent ni des immeubles ni des logements localisés.";
        irisPolygons.addData(checked);
        irisLoaded=true;
      }
      saveStreetView();
      if(arrondToggle.checked){
        arrondToggle.checked=false;
        map.removeLayer(arrondissementPolygons);
      }
      if(map.hasLayer(volumes))map.removeLayer(volumes);
      irisPolygons.addTo(map);
      map.fitBounds(irisPolygons.getBounds().pad(0.025));
      let shown=0;
      irisPolygons.eachLayer(layer=>{if(isReliableIRIS(layer.feature.properties))shown++;});
      irisStatus.textContent="IRIS 2023 · 992 quartiers vérifiés · "+shown+
        " taux représentés. Gris : aucun logement ou moins de 50 logements. "+
        "Aucune information individuelle ni par bâtiment.";
      irisInsights.hidden=false;
      showMapMode("iris");
    }catch(error){
      irisInsights.hidden=true;
      irisToggle.checked=false;
      if(arrondToggle.checked && map.hasLayer(arrondissementPolygons)){
        map.removeLayer(volumes);
        showMapMode("arrondissement");
      }else{
        if(!map.hasLayer(volumes))volumes.addTo(map);
        restoreStreetView();
        button.disabled=false;
        showMapMode("building");
      }
      irisStatus.textContent="Couche IRIS non affichée : "+error.message+". Aucune donnée de secours fictive.";
    }finally{
      irisToggle.disabled=false;
    }
  });
  // The local-only Apur laboratory is an explicit opt-in and has no public fixture.
  if(labEnabled(window.location)){
    import("./apur-lab.mjs").then(({mountApurLab})=>mountApurLab({
      map,volumes,iris:irisPolygons,arrond:arrondissementPolygons,
      irisToggle,arrondToggle,button,status,showMapMode
    })).catch(error=>{ status.textContent="Laboratoire Apur indisponible : "+error.message; });
  }
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
