# VACANT — atlas de l'occupation et de la vacance immobilière

Projet public expérimental, **audit et démonstrateur 2D en cours**, sans déploiement public.

## Ce que nous savons et ce que nous ne savons pas

- Des géométries de **volumes bâtis existants** sont publiées par la Ville de Paris sous licence ODbL. La couche Paris Data renseigne le **nombre d'étages**, **pas la hauteur en mètres**.
- L'Apur dispose d'une couche de datation du bâti et d'informations de hauteur, à qualifier et apparier avant de les afficher à l'objet.
- **Départ temporel choisi : 2006** pour les statistiques territoriales IRIS (jalons 2006, 2011, 2016 et 2023 ; pas d'interpolation annuelle). Un aperçu de chiffres Insee réels pour Paris entier est intégré, mais **la carte de volumes ne représente pas la vacance**. 1968–1999 ne sert qu'au contexte agrégé ; LOVAC privé 2020–2026 est une série distincte.
- L'Insee publie des **statistiques de logements vacants à la maille IRIS**, pas une liste publique de logements vides.
- Les données ouvertes LOVAC concernent des **agrégats communaux**, avec deux ruptures : changement de source GMBI en 2023 (impact millésime LOVAC 2024) et nouvelle extraction fiscale en 2025.
- Le cadastre ancien et les cartes permettent une recherche historique ponctuelle, **pas une animation annuelle attestée depuis 1830**.

Chaque champ absent reste absent. Une statistique IRIS n'est **jamais** attribuée à un bâtiment ou un appartement.

## Démarrage local

Prérequis : un navigateur récent et Python 3 (pour servir les fichiers) ; aucune base de données ni installation npm.

1. Dans le dossier du dépôt, lancer : `python3 -m http.server 8000`
2. Ouvrir `http://localhost:8000/site/`.
3. Cliquer sur « Charger les volumes de la zone visible ». Une connexion réseau est nécessaire (Paris Data, tuiles OSM et bibliothèque Leaflet).
4. Consulter la mini-chronologie Insee **Paris entière** en sélectionnant exclusivement les années 2006, 2011, 2016 et 2023. Elle ne recolore pas les immeubles et ne prétend pas décrire les IRIS.
5. Cliquer sur les polygones pour consulter le nombre d'étages et la source. Le rendu ne représente **ni mètres ni logements vacants**.

L'API publique peut être momentanément indisponible, limitée en débit ou soumise au CORS : un message d'erreur est montré, **aucune donnée de secours fictive** n'est substituée. Les requêtes sont manuelles, géographiquement restreintes et plafonnées.

## Tests

Avec Node.js >= 20 : `node --test tests/*.test.mjs` (ou `npm test`). Pas de paquet à installer.

Le test concerne les contrats, les géométries et les règles de provenance. **Il ne constitue pas une validation réseau** des schémas de Paris Data en production.

## Préparation rigoureuse des futures couches IRIS (non affichées)

`site/iris-contract.mjs` valide des **agrégats territoriaux** IRIS *déjà préparés* (GeoJSON avec les champs `iris_code`, `housing_count`, `vacant_count`). Le préparateur du format Insee 2023 n'est **pas** encore implémenté : il faut d'abord confirmer les modalités officielles exactes, les fichiers et les géographies des contours.

Le validateur et la commande sont disponibles, mais **aucun fichier de statistiques ou contours IRIS réel n'a été intégré à l'atlas**. Avec Node.js >=20 :

```sh
node scripts/validate-iris.mjs /chemin/iris-2023-prepares.geojson /chemin/manifest.json
# Ajouter /chemin/sortie.geojson en troisième argument seulement après audit :
node scripts/validate-iris.mjs /chemin/iris-2023-prepares.geojson /chemin/manifest.json /chemin/sortie.geojson
```

Le manifeste exigé comprend : `census_year`, `geography_year`, `zone="Paris"`, `geography="IRIS"`, `metric="vacant_housing_rp"`, `extracted_at` (AAAA-MM-JJ), `statistics` et `contours` (URL officielle, licence ouverte 2.0, SHA-256 du fichier d'origine) et, pour une sortie, `expected_iris_count`. **Ce dernier doit être déduit indépendamment de l'inventaire officiel des contours** et non égalisé arbitrairement au nombre de lignes préparées. Le script refuse d'écraser une sortie existante et s'arrête sur toute incohérence.

Voir [le protocole temporel](docs/chronologie.md) et [le contrat géographique](docs/architecture.md). Les jeux de tests utilisent uniquement des fixtures synthétiques internes, jamais mises sur la carte.

## Sources Insee : collecte privée

Le script `scripts/collect_insee.py` télécharge, **uniquement avec `--execute`**, les archives officielles RP2006, RP2011, RP2016, RP2023 et le dictionnaire de correspondance RP2023. Il archive les fichiers immuables et leurs empreintes SHA-256. **Le VPS n'a pas été accessible et aucun fichier réel n'y a encore été stocké.** Voir [la procédure, les URLs et les limites](docs/acquisition.md).

## Documentation

- [Audit des sources et droits](docs/sources.md)
- [Modèle de données, architecture et validations](docs/architecture.md)
- [Décision chronologique 2006–2023, preuves et limites](docs/chronologie.md)
- [Passation / limites et suite](docs/handoff.md)
- [Collecte Insee et stockage privé](docs/acquisition.md)
- [Règles de collaboration](AGENTS.md)

## Principes non négociables

Pas de fichiers LOVAC individuels, pas d'adresse « vacante » inférée, pas d'âge/hauteur fictif, pas d'histoire présentée comme observation, pas de déploiement sans autorisation. ODbL et Licence Ouverte impliquent une attribution correcte, et ODbL peut imposer le partage à l'identique d'une base dérivée. Le code de ce dépôt ne prétend pas accorder de droits sur les données tierces.
