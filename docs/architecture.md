# Architecture et contrat de données (v0.1)

## Portée de la première passe

**Sans serveur applicatif** : fichiers HTML/CSS/JS, Leaflet (bibliothèque client OSS figée à 1.9.4) et tuiles OSM pour contexte. Requête manuelle vers l'API Paris Data pour une **petite emprise visible**, jamais vers LOVAC détail. L'interface n'affiche qu'une couche 2D de **volumes bâtis contemporains**, colorés par nombre d'étages ; sa disponibilité dépend d'un réseau et d'API tiers.

**Pourquoi pas la 3D ?** Les volumes Paris Data ne contiennent pas de mètres de hauteur attestés dans H_ET_MAX. Une extrusion mètres nécessitera BD TOPO/Apur + mapping contrôlé. Un volume schématique à l'étage n'est pas une mesure physique.

## Entités futures (contrat indépendant des APIs)

- source : source_id, organisme, url, titre, licence, droits_export, attribution, date_consultation, date_extraction, schema_version, sha256_fichier.
- couche : layer_id, couche_type (volume|batiment|iris|commune|archives), source_id, millesime, zone, CRS, valid_from, valid_to, date_document, methode, confiance, couverture, limites.
- observation_bati : volume_id, building_id **nullable**, polygon (WGS84), floors_max **nullable**, height_m **nullable**, construction_period_start/end **nullable**, construction_date_precision, source_id, quality_flags. Ce sont des **volumes**, ne pas supposer 1:1 avec un bâtiment.
- observation_logement_agregee : zone_type (IRIS|commune), zone_id, geography_version, metric (vacant|secondary_occasional|total_housing|private_long_term_vacant), numerator **nullable**, denominator **nullable**, year, source_id, champ, confidence. Interdit de joindre au bâtiment comme statut.
- document_historique : document_id, cote, institution, date_releve, qualite_georeferencement, scan_rights, transformation, attribution ; date_releve != date_construction.
- correspondance_bati : source_A/id_A, source_B/id_B, methode, intersection_ratio, review_status. Tout n:m ou douteux demeure **non apparié** par défaut.

**Statuts de preuve** : OBSERVATION_ADMINISTRATIVE, STATISTIQUE_AGREGEE, ESTIMATION, RECONSTRUCTION_DOCUMENTEE, INDISPONIBLE. Les deux dates (date de l'objet et date du document / référentiel) restent distinctes. Ne jamais créer une observation ancienne d'un bâtiment à partir de sa seule année de construction.

## Chronologie statistique indépendante de la carte

- `site/timeline.mjs` intègre **quatre lignes agrégées pour Paris entier**, transcrites depuis les tableaux officiels INSEE RP2022 (2006/2011/2016) et RP2023 (2023). Le code n'effectue **aucune** attribution statistique à un immeuble ou IRIS.
- La sélection 2006 / 2011 / 2016 / 2023 est *discrète* et indique deux périmètres distincts (résidences secondaires et logements occasionnels != logements vacants). Aucune année intermédiaire ni « interpolation ».
- RP2023 est un autre schéma harmonisé et sera validé au format brut avant un vrai affichage IRIS. L'annotation « niveau Paris » empêche une confusion avec la carte.
- Vérifications arithmétiques (sommes à une unité près en raison de l'arrondi statistique) et min. cinq ans d'intervalle entre jalons. Voir [chronologie](chronologie.md).

## Actuellement implémenté

Dans site/record.mjs, une réponse API doit satisfaire :
- un identifiant non vide ; arrondissement 1..20 ; Polygon/MultiPolygon valide dans une enveloppe prudente de Paris (filtre d'erreurs de coordonnées seulement, pas un test du périmètre exact) ;
- coordonnées [longitude, latitude], anneaux fermés de >= 4 points, valeurs finies ;
- floors_max issu **uniquement** de h_et_max ; height_m, construction_period et vacancy **toujours null** ;
- n_sq_vb dédoublonné ; données brutes non nécessaires exclues de l'UI ; sources affichées.

**Invariants tests** : géographie WGS84, invalides rejetés, valeurs manquantes préservées, duplication contrôlée, année de fiche non transcrite en date de construction, aucune vacance assignée.

## Fréquence, URL, performance

- Source live : https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/volumesbatisparis/records
- Clause ODSQL : in_bbox(geom_x_y, lat_sud, lon_ouest, lat_nord, lon_est), c'est un **filtre par point représentatif**, pas découpage géométrique exact.
- Pagination limit=100, tri stable `n_sq_vb`, plafond 800 volumes et avertissement si total_count > nombre chargé. Cette pagination côté API doit être testée en conditions réelles (niveaux CORS, capacités, doublons inter-pages).
- Chargement exclusivement à l'action utilisateur, cache inexistant pour éviter fausse fraîcheur ; contrôles de débit à effectuer sur terrain.
- Atlas entier : étape ultérieure (GPKG/GeoJSON sérialisés tuilés sous licence compatible, ingestion reproductible, qualité par couche et manifeste, éventuellement PMTiles). Pas de base ni cluster prématuré.
- Tuiles : OSM standard en usage d'exploration ponctuelle avec attribution ; **ne pas** s'en servir pour gros trafic sans fournisseur conforme à la politique de tuiles OSM.

## Plan de validation du démonstrateur enrichi

1. Confirmer par extraction Apur les périodes/hauteurs, unités et jointures, produire rapport de couverture et licences des dérivés ODbL.
2. Extraire Insee RP2023 en géographie 2025 + contour compatible ; vérifier comparabilité et publier les seuls agrégats IRIS (avec éventuels secrets/valeurs manquantes).
3. Afficher les IRIS comme **polygones** indépendants des bâtiments avec légende « estimation recensement, 2023 » et popover de métadonnées. Jamais appliquer un taux d'IRIS à une emprise de bâtiment.
4. Pour LOVAC agrégé, afficher **Paris commune** séparément, et les deux ruptures de série avec avertissement.
5. Un curseur temporel n'est activé qu'avec millésimes comparables et une couche réellement historique. Construire un protocole d'incertitude des géoréférencements avant 1900.
