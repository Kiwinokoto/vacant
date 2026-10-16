# VACANT — géométrie IRIS de 2013 : archive secondaire candidate

*Audit réalisé le 16 octobre 2026. Statut : recherche SIG privée, **non approuvée pour diffusion cartographique**.*

## Origine et limitations

- [Jeu data.gouv.fr « Contour des IRIS INSEE tout en un »](https://www.data.gouv.fr/datasets/contour-des-iris-insee-tout-en-un), publié le **28 avril 2015** par un compte tiers désormais supprimé.
- Archive exacte : https://www.data.gouv.fr/s/resources/contour-des-iris-insee-tout-en-un/20150428-161348/iris-2013-01-01.zip
- Présentation de l'éditeur : agrégation et reprojection en WGS84 d'anciens contours IGN/Insee ; revendique le découpage au **1er janvier 2013**. Il ne s'agit **pas** du fichier IGN original. La fiche data.gouv.fr indique « Licence Ouverte », revendication conservée comme telle sans étendre les droits.
- Original privé conservé sous \`/srv/vacant/data/raw/secondary/iris-2013-candidate/iris-2013-01-01.zip\` (364 944 694 octets), SHA-256 \`c6afee56f81b3a9d08316034f0f48259162276a3d7a0d11388c2472f2fd5d3a7\`.
- Provenance, date de collecte, licence déclarée, limites et SHA dans \`/srv/vacant/data/manifests/secondary-iris2013-reprojected-20261016.json\`.

## Audit réalisé sur la géométrie réelle

Archive ZIP valide, constituée d'un Shapefile \`.shp/.dbf/.shx/.prj\` en **WGS84**. Le jeu national contient 508 980 enregistrements, dont **9 920 parisiens**. Ceux-ci correspondent à **992 codes IRIS uniques**, présents **10 fois chacun**. Chacun présente exactement 3 variantes de coordonnées dues à des écarts infimes (différence symétrique de surface maximale ~0,000025 m² après transformation Lambert-93). La déduplication **n'est acceptée** que si les écarts restent sous 0,001 m², elle échoue si les formes diffèrent sensiblement.

Contrôles :
- 992 codes appariés exactement à la référence Insee IRIS géographie **2013** et aux 992 statistiques des logements RP **2011** ; types d'IRIS concordants.
- Aucune géométrie invalide (GEOS), union valide, chevauchement de la partition de Paris négligeable (écart d'aire calculée de 0 m² à la précision affichée).
- Contours 2013 candidats comparés séparément aux contours IGN 2025, avec CRS projeté **EPSG:2154** : recouvrement spatial par code (Intersection/Union) **médian 0,947**, minimum **0,6383**, 96 IRIS sur 992 sous **0,90**. Toutes les géométries 2013 diffèrent des géométries 2025 de façon mesurable. Les codes identiques ne justifient **aucune** projection des chiffres anciens sur les contours 2025.
- Le script vérifie l'empreinte SHA-256 de la source secondaire et du dérivé IGN 2025, ainsi que celle du fichier RP2011 Insee via \`build_arrondissement_history.py\`. Il refuse les changements non documentés des fichiers et les destinations publiques.

## Dérivé construit, strictement privé

\`/srv/vacant/data/processed/iris-2013-candidate/iris-2011-candidate.geojson\` : **992 polygones** / 1 240 568 octets, SHA-256 \`a1ea1c1cb78172d1b6725d55307026b0f3b5ae0094a8c130dbfd52d7c8b5a2b2\`. Une seule valeur agrégée par IRIS (parc, vacant, taux s'il y a au moins 50 logements), jamais un logement individuel. Métadonnées explicites : **recensement 2011, géographie revendiquée 2013, source tiers reprojetée, statut \`candidate_secondary_2013_not_approved_for_publication\`**.

Aucun ajout dans \`site/data\`, aucun changement de serveur ou de couche visible. Pour relancer l'audit depuis les originaux immuables (décompression éphémère sûre) :

\`\`\`sh
/srv/vacant/venv/bin/python scripts/audit_iris2013_candidate.py --data-root /srv/vacant/data
\`\`\`

Pour recréer le dérivé après validation et sous nouveau nom (refus d'écraser) :

\`\`\`sh
/srv/vacant/venv/bin/python scripts/audit_iris2013_candidate.py \
  --data-root /srv/vacant/data \
  --private-output /srv/vacant/data/processed/iris-2013-candidate/nouveau-derivé.geojson
\`\`\`

## Décision et prochaines étapes

**Conserver le dérivé hors production.** Sa cohérence interne et l'appariement RP2011 sont solides, mais l'édition géométrique IGN d'origine, la chaîne exacte de reprojection et l'identité de l'auteur de l'archive secondaire ne sont pas démontrées indépendamment.

Priorité : retrouver un **original IGN/Insee géographie 2013** vérifiable (éventuellement fonds 2013 auprès du support IGN), comparer sa géométrie à ce candidat, puis examiner la licence de rediffusion. Prévoir la même chaîne d'acquisition spécifique pour les millésimes géographiques **2008** (RP2006) et **2018** (RP2016) plutôt que de réutiliser 2013.

L'affichage en place de l'historique par **20 arrondissements** reste la solution officiellement validée sur le site, distincte de l'IRIS 2023 géographie 2025.
