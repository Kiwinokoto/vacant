# VACANT — atlas de l'occupation et de la vacance immobilière

Projet public expérimental et atlas 2D **de données officielles**. Les originaux restent sur le VPS ; seul un fichier agrégé validé peut être exposé par le site statique.

## Ce que nous savons et ce que nous ne savons pas

- Des géométries de **volumes bâtis existants** sont publiées par la Ville de Paris sous licence ODbL. La couche Paris Data renseigne le **nombre d'étages**, **pas la hauteur en mètres**.
- L'Apur diffuse les **emprises bâties actuelles** et des périodes de construction attribuées et hauteurs médianes **en mètres** sous ODbL. VACANT prépare une base adaptée publique et une carte distincte des logements vacants : ce n'est ni une reconstruction historique certifiée ni une mesure de l'occupation.
- **Départ temporel choisi : 2006** pour les statistiques territoriales IRIS (jalons 2006, 2011, 2016 et 2023 ; pas d'interpolation annuelle). La chronologie agrégée Paris entier et une **couche indépendante IRIS 2023** (Insee 2023 + contours IGN 2025) sont intégrées ; les volumes bâtis ne représentent jamais des logements vacants. 1968–1999 ne sert qu'au contexte agrégé ; LOVAC privé 2020–2026 est une série distincte.
- L'Insee publie des **statistiques de logements vacants à la maille IRIS**, pas une liste publique de logements vides.
- Les données ouvertes LOVAC concernent des **agrégats communaux**, avec deux ruptures : changement de source GMBI en 2023 (impact millésime LOVAC 2024) et nouvelle extraction fiscale en 2025.
- Le cadastre ancien et les cartes permettent une recherche historique ponctuelle, **pas une animation annuelle attestée depuis 1830**.

Chaque champ absent reste absent. Une statistique IRIS n'est **jamais** attribuée à un bâtiment ou un appartement.

## Parcs des locaux recensés (PR #37)

Par édition BDCOM, nous avons identifié **83 720 locaux en 2017** (fiche d'origine Apur), **83 399 en 2020** (service de structure Apur, somme des 20 `localrdc`) et **83 154 en 2023** (service Apur). Le tableau de la page « Potentiel » indique ces univers d'enquête à côté des effectifs de vacants hors travaux et en travaux. **Ils ne suffisent pas à constituer un taux longitudinal scientifiquement harmonisé** : le décompte original 2017 (7 804 vacants) diffère de l'archive rétrospective (7 853), et la rétrospective Apur de 2023 recode peut-être les travaux 2020 (1 310 contre 1 517 en source 2020). Rien n'en démontre encore la cause. Voir [l'audit scientifique](docs/bdcom-historical-audit-20261017.md).

## Comparaison BDCOM 2017–2023 (PR #36)

En prolongement de #35, VACANT dispose de **trois comptages d'éditions réelles du référentiel Apur**, distinguant vacants hors travaux et locaux en travaux (2017 : 6 954 + 899 ; 2020 : 7 247 + 1 517 ; 2023 : 7 495 + 1 565). Une visualisation à barres et un tableau les présentent séparément dans `site/potentiel.html`. **Ni interpolation, ni taux de vacance historiquement harmonisé**, ni possibilité de conversion/accueil déduite de ces seuls effectifs.

**Fortes divergences documentaires** : la note Apur 2020 indique 8 760 vacants, la rétrospective de 2023 indique 8 560 pour cette même année, alors que la couche 2020 donne 8 764. La cause doit être clarifiée. [Audit complet 2017–2023](docs/bdcom-historical-audit-20261017.md).

## Premier audit BDCOM + bureaux (PR #35)

VACANT distingue les locaux des rez-de-chaussée BDCOM recensés en **2023** en deux catégories effectivement séparées dans l'API Apur : **7 495 vacants hors travaux** (code `AA101`) et **1 565 en travaux** (`AA102`) sur **83 154 locaux recensés**. Leur total **9 060** diffère d'une unité de la note publiée **9 059** ; divergence documentée, sans correction arbitraire. Un tableau classe les 20 arrondissements à partir d'agrégats seulement. **Aucune adresse ni détail de local ne figure dans le dépôt.**

Un ordre de grandeur de **1,5 million de m²** de bureaux immédiatement proposés est documenté pour **Paris intra-muros à fin juin 2026** (Colliers et Cushman & Wakefield), mais les données Colliers T1/T2 sont incompatibles en l'état : ne pas interpréter le saut de niveau comme une hausse effective. **Offre en m² ≠ habitabilité ≠ capacité d'accueil**, pas de logements déduits. Détails et liens : [audit scientifique BDCOM et bureaux](docs/bdcom-open-audit-20261017.md).

## Quel potentiel au-delà des logements habitables ?

VACANT étudie les logements vacants, mais **ne doit pas exclure les logements dégradés ni les bureaux/commerces inoccupés** du champ d'investigation. Il distingue explicitement **destination**, **occupation**, **état physique/risques** et **possibilité de mobilisation** (accueil temporaire, travaux, conversion pérenne). Aucun espace n'est automatiquement « habitable », « indisponible » ou « prêt à accueillir » faute d'expertise. Un bureau sans eau ou lumière reste un **potentiel à instruire**, jamais une solution de nuit directement recommandée sans vérifications de sécurité, hygiène et droits d'usage.

Nouvelle page de cadrage [espaces inoccupés et potentiel d'accueil](site/potentiel.html), avec les trois univers non sommables : logements Insee, logements privés LOVAC et locaux de RDC BDCOM Apur. [Méthode, sources et limites](docs/potentialite-locaux-20261017.md). Aucun nombre de logements/places convertibles n'est estimé à ce stade ; les bureaux en étage n'ont pas encore de mesure parisienne auditée.

## Priorité : comprendre la vacance résidentielle dans le temps

Deux rails, explicités et ordonnés dans le [backlog VACANT](ROADMAP.md) : **(V) vacance résidentielle et sa variation dans le temps en priorité**, et **(B) reconstruction documentée de l'évolution du bâti parisien en parallèle**.

- [Évolution Insee de la vacance à Paris de 1968 à 2023](site/evolution.html) : neuf recensements datés, taux **et nombres**, période de méthode distincte, tableau précis ; [provenance et précautions](docs/vacance-evolution-1968-2023.md).
- [Carte VACANT](site/index.html) : couche géographique IRIS **2023** et comparaison historique **par arrondissement 2006, 2011, 2016, 2023** ; les valeurs Paris entier ne sont pas attribuées aux bâtiments.
- Le tableau Insee indique **139 075 logements vacants / 1 402 024 au total en 2023 (9,9 %)**. Cela ne signifie ni 139 075 logements durablement abandonnés ni que chaque IRIS a le taux moyen parisien.
- Projet historique du bâti : [PR #28](https://github.com/Kiwinokoto/vacant/pull/28) en recherche ; les éditions IGN 2008/2011/2018 ne sont pas encore une série directement comparable. Pas de promotion de ces géométries par analogie avec le taux IRIS.

## Comparaison des arrondissements (V-03)

La carte `site/index.html` peut désormais comparer deux recensements **2006/2011/2016/2023**, seulement après activation de la couche des 20 arrondissements. Un sélecteur de dates colore la **variation en points de taux** ou la **variation du nombre estimé de logements vacants**, avec deux valeurs de départ/arrivée en popup, légende et classement. Les contours IGN **2025** ne servent que de support d'affichage : les valeurs proviennent des recensements aux géographies IRIS respectives, agrégés au niveau arrondissement. Voir [protocole de comparaison](docs/vacance-arrond-comparison-20261017.md).

La lecture de la [vacance de longue durée par arrondissement](docs/lovac-long-duration-20261017.md) distingue l'effectif de plus de deux ans et sa part **parmi les seuls logements privés fiscalement recensés comme vacants**. Ce ratio ne constitue pas le taux de vacance du parc : il est exclu en 2023 car les deux observations ont des dates différentes. Le code est en PR de développement, pas en production.

## Démarrage local

Prérequis : un navigateur récent et Python 3 (pour servir les fichiers) ; aucune base de données ni installation npm.

1. Dans le dossier du dépôt, lancer : `python3 -m http.server 8000`
2. Ouvrir `http://localhost:8000/site/`.
3. Cliquer sur « Charger les volumes de la zone visible ». Une connexion réseau est nécessaire (Paris Data, tuiles OSM et bibliothèque Leaflet).
4. Pour tester la couche des **992 IRIS 2023**, créer le dossier `site/data/`, puis y copier le fichier vérifié `/srv/vacant/data/processed/iris-2023/iris-2023.geojson`. Ce fichier n'est pas versionné en Git : sans lui, l'interface affiche une erreur explicite.
5. Activer « Vacance résidentielle · IRIS 2023 » pour voir les taux par quartier, indépendamment du bâti. Les taux sont volontairement grisés pour moins de 50 logements.
6. La mini-chronologie Insee **Paris entière** présente les recensements 2006, 2011, 2016 et 2023 sans interpolation. Elle ne recolore pas les immeubles et ne prétend pas décrire les IRIS.
7. Désactiver les IRIS pour revenir aux volumes bâtis et consulter leurs étages. Aucun chiffre de vacance n'est attribué aux immeubles.

L'API publique peut être momentanément indisponible, limitée en débit ou soumise au CORS : un message d'erreur est montré, **aucune donnée de secours fictive** n'est substituée. Les requêtes sont manuelles, géographiquement restreintes et plafonnées.

## Tests

Avec Node.js >= 20 : `node --test tests/*.test.mjs` (ou `npm test`). Pas de paquet à installer.

Le test concerne les contrats, les géométries et les règles de provenance. **Il ne constitue pas une validation réseau** des schémas de Paris Data en production.

## Construction reproductible de la couche IRIS 2023

`site/iris-contract.mjs` valide des **agrégats territoriaux** IRIS *déjà préparés* (GeoJSON avec les champs `iris_code`, `housing_count`, `vacant_count`). Le préparateur `scripts/build_iris_2023.py` assemble désormais les trois sources officielles pour l'année 2023 : Parquet Insee, référence IRIS Insee 2025 et GeoParquet IGN 2025. Il contrôle SHA-256, cardinalité et codes (992/992), totaux Paris publiés et topologie GEOS. Il produit une géométrie par IRIS, sans localisation de logements vides.

La couche réelle validée est stockée sur le VPS (`/srv/vacant/data/processed/iris-2023/iris-2023.geojson`, environ 823 Ko) et le site peut l'afficher sur activation. Les années 2006, 2011 et 2016 ne sont **pas encore cartographiées à l'IRIS**. Avec Node.js >=20 :

```sh
node scripts/validate-iris.mjs /chemin/iris-2023-prepares.geojson /chemin/manifest.json
# Ajouter /chemin/sortie.geojson en troisième argument seulement après audit :
node scripts/validate-iris.mjs /chemin/iris-2023-prepares.geojson /chemin/manifest.json /chemin/sortie.geojson
```

Le manifeste exigé comprend : `census_year`, `geography_year`, `zone="Paris"`, `geography="IRIS"`, `metric="vacant_housing_rp"`, `extracted_at` (AAAA-MM-JJ), `statistics` et `contours` (URL officielle, licence ouverte 2.0, SHA-256 du fichier d'origine) et, pour une sortie, `expected_iris_count`. **Ce dernier doit être déduit indépendamment de l'inventaire officiel des contours** et non égalisé arbitrairement au nombre de lignes préparées. Le script refuse d'écraser une sortie existante et s'arrête sur toute incohérence.

Voir [le protocole temporel](docs/chronologie.md) et [le contrat géographique](docs/architecture.md). Les jeux de tests utilisent uniquement des fixtures synthétiques internes, jamais mises sur la carte.

## Sources Insee : collecte privée

Le script `scripts/collect_insee.py` télécharge, **uniquement avec `--execute`**, les archives officielles RP2006, RP2011, RP2016, RP2023 et le dictionnaire de correspondance RP2023. Il archive les fichiers immuables et leurs empreintes SHA-256. **Sept fichiers officiels sont maintenant archivés sur le VPS**, avec manifestes et empreintes SHA-256 ; la carte dérivée 2023 a passé les contrôles Node et GEOS. Voir [la procédure, les URLs et les limites](docs/acquisition.md).

## Documentation

- [Backlog : vacance d'abord et reconstruction historique en parallèle](ROADMAP.md)
- [Vacance : évolution Paris 1968–2023, tableaux Insee et distinctions de méthode](docs/vacance-evolution-1968-2023.md)

- [Audit des sources et droits](docs/sources.md)
- [Modèle de données, architecture et validations](docs/architecture.md)
- [Décision chronologique 2006–2023, preuves et limites](docs/chronologie.md)
- [Passation / limites et suite](docs/handoff.md)
- [Collecte Insee et stockage privé](docs/acquisition.md)
- [Règles de collaboration](AGENTS.md)
- [Déploiement statique Traefik, sous contrôle AgentCTL](deploy/README.md)
- [Distribution libre du dérivé Apur sous ODbL 1.0 et contrôles SHA](docs/apur-odbl-public-dataset-20261017.md)

## Principes non négociables

Pas de fichiers LOVAC individuels, pas d'adresse « vacante » inférée, pas d'âge/hauteur fictif, pas d'histoire présentée comme observation, pas de déploiement sans autorisation. ODbL et Licence Ouverte impliquent une attribution correcte, et ODbL peut imposer le partage à l'identique d'une base dérivée. Le code de ce dépôt ne prétend pas accorder de droits sur les données tierces.

## Historique agrégé par arrondissement

VACANT compare les millésimes 2006, 2011, 2016 et 2023 à la maille des **20 arrondissements**. Le script scripts/build_arrondissement_history.py lit les tables Insee IRIS de géographie 2008/2013/2018 et le dérivé 2023 de géographie 2025 ; il vérifie SHA-256, cardinalité de 992 IRIS, valeurs et totaux Paris. Les données de chaque millésime sont **agrégées par arrondissement AVANT** toute géométrie. Seuls les contours des 20 arrondissements (dissolution IGN 2025) sont affichés, non les contours historiques des IRIS. Pas de données d'immeuble ou d'adresse.

Reconstruction sur le VPS : fournir au script --raw-root /srv/vacant/data/raw/insee, --iris-geojson /srv/vacant/data/processed/iris-2023/iris-2023.geojson, et --output /srv/vacant/data/processed/arrond-history/arrond-history.geojson. Copier uniquement ce dernier dérivé vérifié sous site/data/arrond-history.geojson dans une release ; aucun fichier brut.

## Audit des références géographiques historiques

L’audit des identifiants Insee 2008/2013/2018/2025 est décrit dans [docs/iris-historique.md](docs/iris-historique.md). Les 992 codes parisiens coïncident, mais **les géométries anciennes ne sont pas validées** : la comparaison historique reste par arrondissement, et les contours IRIS précis restent limités à 2023.

## Géographie IRIS candidate pour RP2011

La source secondaire 2013 reprojetée a fait l’objet d’un [audit SIG détaillé](docs/iris-2013-candidate.md). Un dérivé privé de 992 IRIS a été généré, mais n’est **pas publié**, car l’original IGN correspondant reste à obtenir et confirmer. Ne pas confondre cette piste avec les données validées par arrondissement sur le site.

## Double contrôle des contours IRIS historiques

Les différences entre géométries secondaires 2013, 2016 et IGN 2025 sont auditées dans [l'étude comparative](docs/iris-crosscheck.md). **Aucune ancienne géométrie fine n'a été certifiée ni diffusée** ; une [demande d'archives IGN](docs/demande-archives-ign.md) est préparée mais non envoyée.

## Corroboration Atlasanté des géométries historiques

L'[audit institutionnel 2014](docs/iris-2014-atlasante.md) retrouve les contours du candidat tiers dit 2013 pour les 992 IRIS de Paris avec un écart maximal de 0,000009 m². L'édition exacte de référence et la licence de rediffusion demeurent non confirmées ; aucun GeoJSON 2011 n'est accessible publiquement.

## Préparation des éditions historiques 2008 et 2018

L'[inventaire des éditions IGN](docs/iris-archive-readiness.md) distingue date de livraison et géographie réelle. Aucune nouvelle archive géométrique 2008/2018 ne peut encore être cartographiée à l'IRIS. Les candidats historiques restent privés ; leur publication est bloquée par le validateur tant que les droits et millésimes ne sont pas établis.

## Contrôle des hauteurs et périodes de construction Apur

Le [rapport préliminaire Apur](docs/apur-bati-audit.md) audite la complétude des attributs de 128 206 emprises et les unités réelles. Le script `scripts/audit_apur_emprises.py --live` n’interroge que des comptes et statistiques agrégés. Aucune géométrie n’a été publiée et aucun logement vacant n’est localisé par bâtiment.
