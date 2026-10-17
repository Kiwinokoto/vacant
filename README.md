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

- [Audit des sources et droits](docs/sources.md)
- [Premiers états du bâti parisien IGN (éditions 2008/2011/2018), incompatibilités et comparaison locale](docs/ign-bdtopo-historic-20261017.md)
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
