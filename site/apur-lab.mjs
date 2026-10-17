import {labEnabled, PERIODS, HEIGHT_BANDS, periodStyle, heightStyle,
  fetchLocalSnapshot} from "./apur-lab-contract.mjs";
import {loadLocalManifest, loadVisibleGrid} from "./apur-grid-client.mjs";

export const APUR_LAB_FIXTURE_SHA256="ba14be71c3cb58afcae935bcdc3f775f63ad043d12ecb20f42bdf2da759afaf9";
export const APUR_GRID_MANIFEST_SHA256="bb02fe9ac9ef7919018118659e12ac533b098234250eba540c6975e7b273bb0c";
const GRID_PATH="./data/apur-grid/";
const isGrid=mode=>mode==="grid-period"||mode==="grid-height";
const isHeight=mode=>mode==="height"||mode==="grid-height";

export function mountApurLab({map,volumes,iris,arrond,irisToggle,arrondToggle,button,
  status,showMapMode}){
  if(!labEnabled(window.location))return;
  const section=document.querySelector("#apur-local");
  const mode=document.querySelector("#apur-mode");
  const message=document.querySelector("#apur-lab-status");
  const legend=document.querySelector("#apur-lab-legend");
  const reload=document.querySelector("#apur-grid-reload");
  if(!section||!mode||!message||!legend||!reload)throw new Error("Apur lab controls missing");
  section.hidden=false;
  const volumeIndicator=document.querySelector("#volumes-indicator");
  if(volumeIndicator){
    volumeIndicator.checked=map.hasLayer(volumes);
    volumes.on("add",()=>{volumeIndicator.checked=true;});
    volumes.on("remove",()=>{volumeIndicator.checked=false;});
  }

  const overlay=L.geoJSON(null,{
    style:feature=>({color:"#243944",weight:0.65,fillOpacity:0.8,
      fillColor:(isHeight(mode.value)?heightStyle(feature.properties.height_m):
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
        "Emprise actuelle pouvant recouvrir plusieurs bâtiments ; millésime scientifique non confirmé.",
        "Aucune information de vacance par bâtiment."
      ]){
        const paragraph=document.createElement("p");
        paragraph.textContent=value;
        body.append(paragraph);
      }
      return body;
    })
  });

  let small=null,gridManifest=null,gridCache=null;
  let active=false,source=null,token=0,originalView=null,lastMode="off",busy=false,gridDirty=false;
  function writeLegend(selected){
    legend.replaceChildren();
    const entries=isHeight(selected)?HEIGHT_BANDS:PERIODS.map(([code,label,color])=>[label,color]);
    for(const [label,color] of entries){
      const cell=document.createElement("span");
      const swatch=document.createElement("i");
      swatch.style.backgroundColor=color;
      const text=document.createElement("span");
      text.textContent=label;
      cell.append(swatch,text);
      legend.append(cell);
    }
  }
  function viewBounds(){
    const bounds=map.getBounds();
    if(!bounds.isValid())throw new Error("Vue cartographique invalide");
    return [bounds.getWest(),bounds.getSouth(),bounds.getEast(),bounds.getNorth()];
  }
  function bboxKey(b){return b.map(v=>v.toFixed(7)).join(",");}
  function updateTitles(selected,amount){
    document.querySelector("#map-title").textContent=
      (isHeight(selected)?"Hauteurs médianes":"Périodes de construction attribuées")+
      " · Apur (laboratoire privé)";
    document.querySelector("#map-subtitle").textContent=
      "Emprises actuelles Apur · "+(isHeight(selected)?"h_med en mètres":"périodes attribuées")+
      " · "+amount.toLocaleString("fr-FR")+" emprises uniques visibles · millésime non confirmé · aucune vacance";
  }
  function dismiss({forOtherLayer=false}={}){
    token++;
    if(map.hasLayer(overlay))map.removeLayer(overlay);
    if(active&&!forOtherLayer){
      if(!map.hasLayer(volumes))volumes.addTo(map);
      if(originalView)map.setView(originalView.center,originalView.zoom);
      button.disabled=false;
      showMapMode("building");
      status.textContent="Retour aux volumes actuels ; aucune donnée Apur publiée.";
    }
    active=false;source=null;originalView=null;lastMode="off";gridDirty=false;
    mode.value="off";
    reload.hidden=true;reload.disabled=false;
    legend.replaceChildren();
    message.textContent="Laboratoire désactivé. Aucun jeu de données Apur récupéré sur Internet.";
  }

  // On change, the existing IRIS/arrondissement handlers take ownership of the map.
  for(const toggle of [irisToggle,arrondToggle]){
    toggle.addEventListener("change",()=>{
      if(toggle.checked && (active||mode.value!=="off"))dismiss({forOtherLayer:true});
    },true);
  }
  map.on("moveend",()=>{
    if(active&&isGrid(lastMode)&&!busy){
      gridDirty=true;
      message.textContent="Cadrage modifié : la sélection précédente reste affichée. "+
        "Cliquer sur « Recharger les cellules visibles » pour cette nouvelle zone.";
    }
  });

  async function apply(selected,{refresh=false}={}){
    if(busy)return;
    const current=++token;
    busy=true;
    mode.disabled=true;
    reload.disabled=true;
    message.textContent="Vérification de la source Apur figée, sans API externe…";
    try{
      let next,kind,detail="";
      if(isGrid(selected)){
        if(!gridManifest)gridManifest=await loadLocalManifest(
          APUR_GRID_MANIFEST_SHA256,fetch,GRID_PATH);
        const bbox=viewBounds(),key=bboxKey(bbox);
        // The two color modes share a verified selection; only an explicit reload refetches.
        if(!refresh&&gridCache&&(source==="grid"||gridCache.key===key)){
          next=gridCache.result;
        }else{
          next=await loadVisibleGrid(gridManifest,bbox,fetch,GRID_PATH);
          if(bboxKey(viewBounds())!==key)throw new Error("Cadrage modifié pendant le chargement : recharger");
          gridCache={key,result:next};
        }
        if(next.uniqueObjects===0)throw new Error("Aucune emprise dans la zone visible");
        kind="grid";
        detail=next.cellsLoaded+" cellules, "+next.placements.toLocaleString("fr-FR")+
          " occurrences vérifiées et dédoublonnées, "+next.expectedBytes.toLocaleString("fr-FR")+" octets";
      }else{
        if(!small)small=await fetchLocalSnapshot(APUR_LAB_FIXTURE_SHA256);
        next={collection:small.collection,uniqueObjects:small.collection.features.length};
        kind="small";
        detail="extrait privé de 150 emprises SHA-256 vérifié";
      }
      if(token!==current||mode.value!==selected)return;
      // Nothing changes in the map until all requested features passed integrity checks.
      if(!active)originalView={center:map.getCenter(),zoom:map.getZoom()};
      irisToggle.checked=false;
      arrondToggle.checked=false;
      map.removeLayer(iris);
      map.removeLayer(arrond);
      map.removeLayer(volumes);
      if(source!==kind || (kind==="grid" && refresh) ||
          (kind==="grid" && gridCache?.key!==overlay._apurKey)){
        overlay.clearLayers();
        overlay.addData(next.collection);
        overlay._apurKey=kind==="grid"?gridCache.key:null;
      }
      if(!map.hasLayer(overlay))overlay.addTo(map);
      if(kind==="grid" && (refresh || source!=="grid"))gridDirty=false;
      active=true;source=kind;lastMode=selected;
      button.disabled=true;
      reload.hidden=kind!=="grid";
      if(kind==="small")map.fitBounds(overlay.getBounds().pad(0.08));
      overlay.setStyle(feature=>({color:"#243944",weight:0.65,fillOpacity:0.8,
        fillColor:(isHeight(selected)?heightStyle(feature.properties.height_m):
          periodStyle(feature.properties.period_code)).color}));
      writeLegend(selected);
      updateTitles(selected,next.uniqueObjects);
      status.textContent=next.uniqueObjects.toLocaleString("fr-FR")+
        " emprises Apur affichées, sans indicateur de vacance par bâtiment.";
      const heights=next.collection.features.filter(f=>f.properties.height_m!=null).length;
      message.textContent=next.uniqueObjects.toLocaleString("fr-FR")+
        " emprises uniques · "+(isHeight(selected)?heights.toLocaleString("fr-FR")+" hauteurs disponibles · ":"")+
        detail+". © Apur · ODbL · extraction du 16/10/2026, millésime métier non confirmé."+
        (kind==="grid"&&gridDirty?" Cadrage modifié : recharger les cellules visibles.":"");
    }catch(error){
      // Keep the previous overlay and controls on any missing/altered/stale cell.
      mode.value=lastMode;
      reload.hidden=!isGrid(lastMode);
      message.textContent="Aucune nouvelle couche appliquée : "+error.message+
        ". La couche précédente est conservée.";
    }finally{
      busy=false;
      mode.disabled=false;
      reload.disabled=false;
    }
  }

  mode.addEventListener("change",()=>{
    const selected=mode.value;
    if(selected==="off")dismiss();
    else apply(selected);
  });
  reload.addEventListener("click",()=>{
    if(isGrid(lastMode) && mode.value===lastMode)apply(lastMode,{refresh:true});
  });
}
