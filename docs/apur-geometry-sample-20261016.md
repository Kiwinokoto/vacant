# Apur — contrôle géométrique borné du 16 octobre 2026

**Statut : étude uniquement, aucune nouvelle couche publiée.** GitHub `main` au départ : `72a9d06377541b7b266e0d8153e89a7ae19afb95`. Service examiné : https://carto2.apur.org/apur/rest/services/OPENDATA/EMPRISE_BATIE_PARIS/MapServer/0. Projection native déclarée EPSG:2154, interrogée en GeoJSON EPSG:4326 puis vérifiée géométriquement avec Shapely 2.1.2 et Pyproj 3.7.2. Lecture seule, 8 requêtes de moins de 8 Ko chacune, sans fichier de géométrie conservé.

## Provenance et droits

- Documentation : https://www.apur.org/fr/open-data-cartes/open-data/emprises-baties-paris-metropole-une-lecture-tissu-urbain (publication septembre 2024).
- Jeu : https://opendata.apur.org/datasets/emprise-batie-paris. Licence annoncée **ODbL**, attribution et partage à l'identique des bases dérivées à examiner.
- La date de la documentation **n'est pas** le millésime exact du service. Export officiel daté, métadonnées de version et SHA-256 **non encore établis**. Ne pas déclarer le millésime comme confirmé.

## Observation bornée

Strates (ordre OBJECTID, 8 objets maximum chacune) : début, offsets 40 000, 80 000, 120 000, première série sans `an_const`, première série `c_perconst=99`, première série hauteur nulle/à zéro, et tous les `h_med>200` (3). **59 polygones reçus et valides GEOS**, soit **56 OBJECTID distincts** (3 répétitions attendues entre strates) ; 0 MultiPolygon dans cet échantillon, 0 géométrie nulle et 0 hors de l'enveloppe prudente de Paris. Aires observées : 12,5 à 2 080,8 m². Ce choix raisonné **ne constitue pas un tirage aléatoire ni une preuve de qualité des 128 206 objets**. Réponses d'environ 4–8 Ko, latences observées de 0,17 à 1,94 s par requête ; ce n'est pas un benchmark navigateur/mobile.

### Valeurs exceptionnelles de h_med

| OBJECTID | n_sq_eb | h_med (m) | h_moy (m) | an_const | Surface emprise (m²) | Interprétation |
|---|---:|---:|---:|---:|---:|---|
| 127385 | 750102857 | 300 | 116,15 | 1889 | 1 540 | Secteur Tour Eiffel |
| 127981 | 750118957 | 215,70 | 216,90 | 1889 | 202,9 | Secteur Tour Eiffel |
| 127999 | 750092471 | 205,22 | 185,69 | 1973 | 2 080,8 | Secteur Tour Montparnasse |

Les trois polygones sont topologiquement valides et leurs emplacements/années sont plausibles. **Ne pas supprimer mécaniquement h_med>200** ; deux emprises distinctes autour de la Tour Eiffel montrent qu'une emprise n'est pas un bâtiment architectural indivisible. Pour l'objet 127385, `h_min` et `h_max` sont absents malgré `h_med=300`. L'identification est indicative et demande confrontation à une source officielle avant publication en tant que nom de monument.

### Autres anomalies

OBJECTID 5 : `h_med=1,3 m` mais `h_min=3,8 m`, `h_max=14 m`. Dans la strate des hauteurs nulles, sept des huit objets ont une médiane égale à zéro malgré un minimum positif. Cela empêche de considérer toutes les valeurs métriques comme cohérentes sans filtre et indicateur d'incertitude.

Les contrôles doivent distinguer hauteur absente, hauteur nulle, hauteur incohérente et hauteur atypique plausible, sans recalculer arbitrairement les données source.

## Critères avant toute couche

1. Conserver `c_perconst` en classes officielles, dont `99` = non datée ; obtenir le dictionnaire exact des périodes avant toute légende chronologique. Ne pas reconstituer une année précise ni un état historique à partir de la classe.
2. Pour les hauteurs `h_med` en mètres, préserver les manquants et identifier les incohérences de plage. Ne pas transformer `H_ET_MAX` Paris Data (étages) en mètres.
3. Tester avec export Apur daté et fichier SHA-256, topo GEOS complète, unicité d'ID, géographie, limites de l'API, droits ODbL et attributions. Préparer ensuite des tuiles ou une stratégie de requêtes limitées ; pas de chargement synchrone des 128 206 polygones dans Leaflet sur mobile.
4. Tester ensuite dans Chromium desktop et mobile, avec pagination, indisponibilité API et légende ; aucune couche Apur publique tant que ces contrôles ne sont pas passés.
5. **Aucune donnée de vacance Insee ne doit être assignée aux emprises Apur**. Ni fusion silencieuse avec les volumes Paris Data ni publication de géométries IGN historiques non autorisées.

Ce document enregistre une étude de **lecture seule** et non la recette d'une couche cartographique prête à être déployée.
