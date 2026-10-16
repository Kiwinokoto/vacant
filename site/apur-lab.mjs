import {labEnabled, PERIODS, HEIGHT_BANDS, periodStyle, heightStyle,
  fetchLocalSnapshot} from "./apur-lab-contract.mjs";

export const APUR_LAB_FIXTURE_SHA256="ba14be71c3cb58afcae935bcdc3f775f63ad043d12ecb20f42bdf2da759afaf9";

export function mountApurLab({map,volumes,iris,arrond,irisToggle,arrondToggle,button,
  status,showMapMode}){
  if(!labEnabled(window.location))return;
  const section=document.querySelector("#apur-local");
  const mode=document.querySelector("#apur-mode");
  const message=document.querySelector("#apur-lab-status");
  const legend=document.querySelector("#apur-lab-legend");
  if(!section||!mode||!message||!legend)throw new Error("Apur lab controls missing");
  section.hidden=false;
  const volumeIndicator=document.querySelector("#volumes-indicator");
  if(volumeIndicator){
    volumeIndicator.checked=map.hasLayer(volumes);
    volumes.on("add",()=>{volumeIndicator.checked=true;});
    volumes.on("remove",()=>{volumeIndicator.checked=false;});
  }
  const overlay=L.geoJSON(null,{
    style:feature=>({color:"#243944",weight:0.65,fillOpacity:0.8,
      fillColor:(mode.value==="height"?heightStyle(feature.properties.height_m):
        periodStyle(feature.properties.period_code)).color}),
    onEachFeature:(feature,layer)=>layer.bindPopup(()=>{
      const body=document.createElement("div");
      const title=document.createElement("strong");
      title.textContent="Emprise Apur n° "+feature.properties.object_id;
      body.append(title);
      for(const value of [
        "Période attribuée : "+periodStyle(feature.properties.period_code).label,
        "Hauteur médiane : "+(feature.properties.height_m==null?
          "indisponible ou incohérente":feature.properties.height_m.toLocaleString("fr-FR")+" m"),
        "Une emprise peut couvrir plusieurs bâtiments ; millésime scientifique non confirmé.",
        "Aucune information de vacance par bâtiment."
      ]){
        const paragraph=document.createElement("p");paragraph.textContent=value;body.append(paragraph);
      }
      return body;
    })
  });
  let loaded=null,active=false,token=0,originalView=null;
  function writeLegend(name){
    legend.replaceChildren();
    const entries=name==="height"?HEIGHT_BANDS:PERIODS.map(([code,label,color])=>[label,color]);
    for(const [label,color] of entries){
      const cell=document.createElement("span");
      const swatch=document.createElement("i");
      swatch.style.backgroundColor=color;
      const text=document.createElement("span");text.textContent=label;
      cell.append(swatch,text);legend.append(cell);
    }
  }
  function dismiss({forOtherLayer=false}={}){
    token++;
    if(map.hasLayer(overlay))map.removeLayer(overlay);
    if(active && !forOtherLayer){
      if(!map.hasLayer(volumes))volumes.addTo(map);
      if(originalView)map.setView(originalView.center,originalView.zoom);
      button.disabled=false;
      showMapMode("building");
      status.textContent="Retour aux volumes actuels ; aucune donnée Apur publiée.";
    }
    active=false;originalView=null;
    mode.value="off";
    legend.replaceChildren();
    message.textContent="Laboratoire désactivé. Aucun jeu de données Apur chargé depuis Internet.";
  }
  // Existing IRIS/arrondissement change handlers run after capture phase.
  for(const toggle of [irisToggle,arrondToggle]){
    toggle.addEventListener("change",()=>{
      if(toggle.checked && (active||mode.value!=="off"))dismiss({forOtherLayer:true});
    },true);
  }
  mode.addEventListener("change",async()=>{
    const selected=mode.value;
    const current=++token;
    if(selected==="off"){
      dismiss();
      return;
    }
    mode.disabled=true;
    message.textContent="Vérification SHA-256 du dérivé Apur privé, sans accès à l'API…";
    try{
      if(!loaded)loaded=await fetchLocalSnapshot(APUR_LAB_FIXTURE_SHA256);
      if(current!==token||mode.value!==selected)return;
      // All file validation is complete before any map or toggle change.
      if(!active)originalView={center:map.getCenter(),zoom:map.getZoom()};
      irisToggle.checked=false;
      arrondToggle.checked=false;
      if(map.hasLayer(iris))map.removeLayer(iris);
      if(map.hasLayer(arrond))map.removeLayer(arrond);
      if(map.hasLayer(volumes))map.removeLayer(volumes);
      if(!active){
        overlay.addData(loaded.collection);
        overlay.addTo(map);
        map.fitBounds(overlay.getBounds().pad(0.08));
      }
      active=true;
      button.disabled=true;
      overlay.setStyle(feature=>({color:"#243944",weight:0.65,fillOpacity:0.8,
        fillColor:(selected==="height"?heightStyle(feature.properties.height_m):
          periodStyle(feature.properties.period_code)).color}));
      writeLegend(selected);
      const available=loaded.collection.features.filter(f=>f.properties.height_m!==null).length;
      const title=selected==="height"?"Hauteurs médianes · emprises Apur":
        "Périodes attribuées · emprises Apur";
      document.querySelector("#map-title").textContent=title+" (laboratoire local)";
      document.querySelector("#map-subtitle").textContent=selected==="height"?
        "Apur · hauteur h_med en mètres, 150 emprises actuelles · millésime non confirmé":
        "Apur · périodes attribuées aux emprises actuelles · millésime non confirmé";
      status.textContent="150 emprises du dérivé local SHA-256 validé. "+
        "Aucun taux de vacance associé aux polygones.";
      message.textContent=(selected==="height"?available+" hauteurs exploitables sur 150 emprises. ":
        "150 emprises avec période de construction attribuée. ")+
        "Apur · ODbL. Archive extraite le 16/10/2026, millésime métier non confirmé.";
    }catch(error){
      // Preserve existing map on invalid or absent candidate; reset only the select.
      mode.value=active?(selected==="height"?"period":"height"):"off";
      message.textContent="Aucune nouvelle couche appliquée : "+error.message;
    }finally{
      mode.disabled=false;
    }
  });
}
