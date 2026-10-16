# VACANT — atlas de l'occupation et de la vacance immobilière

Projet public expérimental, **audit et démonstrateur 2D en cours**, sans déploiement public.

## Ce que nous savons et ce que nous ne savons pas

- Des géométries de **volumes bâtis existants** sont publiées par la Ville de Paris sous licence ODbL. La couche Paris Data renseigne le **nombre d'étages**, **pas la hauteur en mètres**.
- L'Apur dispose d'une couche de datation du bâti et d'informations de hauteur, à qualifier et apparier avant de les afficher à l'objet.
- L'Insee publie des **statistiques de logements vacants à la maille IRIS**, pas une liste publique de logements vides.
- Les données ouvertes LOVAC concernent des **agrégats communaux**, avec des ruptures de série majeures en 2023 et 2025.
- Le cadastre ancien et les cartes permettent une recherche historique ponctuelle, **pas une animation annuelle attestée depuis 1830**.

Chaque champ absent reste absent. Une statistique IRIS n'est **jamais** attribuée à un bâtiment ou un appartement.

## Démarrage local

Prérequis : un navigateur récent et Python 3 (pour servir les fichiers) ; aucune base de données ni installation npm.

1. Dans le dossier du dépôt, lancer : `python3 -m http.server 8000`
2. Ouvrir `http://localhost:8000/site/`.
3. Cliquer sur « Charger les volumes de la zone visible ». Une connexion réseau est nécessaire (Paris Data, tuiles OSM et bibliothèque Leaflet).
4. Cliquer sur les polygones pour consulter le nombre d'étages et la source. Le rendu ne représente **ni mètres ni logements vacants**.

L'API publique peut être momentanément indisponible, limitée en débit ou soumise au CORS : un message d'erreur est montré, **aucune donnée de secours fictive** n'est substituée. Les requêtes sont manuelles, géographiquement restreintes et plafonnées.

## Tests

Avec Node.js >= 20 : `node --test tests/*.test.mjs` (ou `npm test`). Pas de paquet à installer.

Le test concerne les contrats, les géométries et les règles de provenance. **Il ne constitue pas une validation réseau** des schémas de Paris Data en production.

## Documentation

- [Audit des sources et droits](docs/sources.md)
- [Modèle de données, architecture et validations](docs/architecture.md)
- [Passation / limites et suite](docs/handoff.md)
- [Règles de collaboration](AGENTS.md)

## Principes non négociables

Pas de fichiers LOVAC individuels, pas d'adresse « vacante » inférée, pas d'âge/hauteur fictif, pas d'histoire présentée comme observation, pas de déploiement sans autorisation. ODbL et Licence Ouverte impliquent une attribution correcte, et ODbL peut imposer le partage à l'identique d'une base dérivée. Le code de ce dépôt ne prétend pas accorder de droits sur les données tierces.
