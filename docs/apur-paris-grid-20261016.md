# VACANT — découpage privé des emprises Apur à Paris (grille 500 m)

**Audit et recette du 16 octobre 2026. Recherche interne uniquement.**
GitHub source de vérité : `Kiwinokoto/vacant`, `main=72a9d06377541b7b266e0d8153e89a7ae19afb95` au départ/dernier contrôle. PR #17–21 non fusionnées et indépendantes. La production `1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0` reste inchangée.

## Source figée

Original officiel Apur `EMPRISE_BATIE_PARIS` : archive SHP ZIP **31 981 417 octets**, enregistrée en privé sur VPS :

`/srv/vacant/data/raw/apur/frozen-2026-10-16/EMPRISE_BATIE_PARIS.shp.zip`

SHA-256 : `f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11`, acquisition avec `manifest.json` privé vérifié. CRS du SHP : **EPSG:2154**, transformation WGS84 **EPSG:4326**. Source : https://opendata.apur.org/datasets/emprise-batie-paris ; licence ODbL 1.0.

**Millésime scientifique non confirmé.** Les dates de mise à jour du Géocatalogue, du ZIP et des objets sont divergentes : ne pas déclarer `février 2025` comme millésime unique. Demande de confirmation déjà envoyée à l'Apur le 16/10, surveillance Gmail existante.

## Production de la grille privée

Fichier ajouté : `scripts/build_apur_private_grid.py`. Aucune API réseau ni dépendance supplémentaire : bibliothèques `shapefile` / Shapely / Pyproj présentes dans le venv privé. Grille régulière de **500 m**, ancrée sur le référentiel Lambert-93. Chaque forme valide est assignée à **toutes les cellules dont elle intersecte une surface positive** : on conserve le **polygone entier**, sans découpage ni simplification. Si une emprise traverse des cellules, elle apparaît dans plusieurs fichiers et doit être **dédoublonnée par `OBJECTID` côté lecteur**. Aucun comptage de logements ou taux de vacance.

Exécution réalisée :

```sh
/srv/vacant/venv/bin/python scripts/build_apur_private_grid.py \
  /srv/vacant/data/raw/apur/frozen-2026-10-16/EMPRISE_BATIE_PARIS.shp.zip \
  /srv/vacant/data/raw/apur/frozen-2026-10-16/manifest.json \
  /srv/vacant/data/processed/apur/paris-grid-experiments/cells-500m-original \
  --cell-m 500
```

La destination doit être nouvelle sous un répertoire privé `0700`. Construction dans un dossier temporaire privé, publication atomique de la **sortie locale privée** (renommage du dossier final après réussite). Les fichiers de cellule sont `0600`, chacun avec son SHA-256, son compte et sa bbox WGS84 dans le manifeste. Aucune forme source ou sortie générée n'est versionnée dans GitHub, `site/` ou une release. L'extrait contient uniquement `object_id`, `period_code`, `height_m` (mètres), jamais un attribut de vacance.

### Bilan exhaustif

| Mesure | Résultat |
|---|---:|
| Emprises SHP lues | **128 206** |
| Géométries invalides GEOS exclues | **104** |
| `n_sq_eb` absent (après contrôle géométrique) | **13** |
| Emprises uniques conservées | **128 089** |
| Emprises placées dans plusieurs cellules | **9 860** |
| Occurrences totales dans les cellules | **138 381** |
| Cellules occupées de 500 mètres | **456** |
| Poids total GeoJSON | **91 515 440 octets** |
| Plus grande cellule | **796 937 octets** et **1 461 objets** |
| Hauteurs médianes valides (mètres) | **127 689** |
| Hauteurs absentes, zéro ou contradictoires avec min/max | **400** |
| Hauteurs médianes supérieures à 200 m | **3**, conservées sans plafond |

Les **117 exclusions** sont documentées et disjointes par politique de priorité : 104 mauvaises géométries, puis 13 identifiants métier absents. Aucune réparation automatique ni valeur substituée. Les périodes `c_perconst=NULL` deviennent « non datée », classe 99, clairement signalée ; les autres classes conservent leur sens documenté.

Mesures de génération sur VPS : **120,24 s**, pic de RAM **392 020 Ko**. Ce sont des chiffres locaux, pas des capacités d'hébergement public.

**Répertoire privé :** `/srv/vacant/data/processed/apur/paris-grid-experiments/cells-500m-original` (ni accessible par Nginx ni committé). Manifeste `manifest.json` **152 865 octets**, SHA-256 :

`bb02fe9ac9ef7919018118659e12ac533b098234250eba540c6975e7b273bb0c`.

Contrôle indépendant des **456 SHA-256 de cellules**, comptes, tailles, permissions privées, cardinalité, 128 089 ID distincts et 138 381 occurrences : **conforme**. Une emprise peut apparaître dans **quatre** cellules au maximum dans cet export ; toutes ses apparitions sont identiques.

## Lecteur local et recette navigateur

- `experiments/apur-grid/grid-client.mjs` : contrôle SHA du manifeste et des cellules, sélection géographique de bbox, limite **12 cellules**, **10 Mo** ou **5 000 occurrences** par demande ; liste blanche des attributs, vérifications d'intégrité, dédoublonnage `object_id`, refus des conflits et des fichiers malformés. Validation complète **avant** mutation de la carte.
- `experiments/apur-grid/index.html` : explorateur dédié uniquement à `localhost`, avec carte **en haut sur mobile**, périodes attribuées et hauteurs médianes, légendes, unités, popups et avertissements. Fond neutre, ressources Leaflet placées en local, aucun appel au service Apur ni à OSM.
- `experiments/apur-grid/.gitignore` : le répertoire `_local/` est exclu de Git. On y monte temporairement le manifeste, les cellules et Leaflet sur une machine autorisée. **Ne jamais servir le test sur 0.0.0.0**, publier le dossier, ni laisser une copie persistante sur le poste de recette.
- Dans ce laboratoire, charger manuellement la zone visible ; un changement de vue ne déclenche pas 456 téléchargements. En cas d'erreur ou de zone trop grande, la carte précédente est conservée avec message explicite.

Résultats Chromium, clone frais sur Linux Mint, serveur HTTP sur `127.0.0.1`, fixture privée copiée par SSH avec SHA-256 conforme :

| Vue | Emprises uniques | Occurrences dédoublonnées | Cellules / octets chargés | Latence locale observée |
|---|---:|---:|---:|---:|
| Desktop 1280×800 | **3 385** | 3 545 | 6 / 2 213 079 | **108 ms** |
| Mobile simulé 390×844 | **2 284** | 2 374 | 4 / 1 457 464 | **114 ms** |
| Petit mobile simulé 320×720 | **1 242** | 1 266 | 2 / 769 316 | **76 ms** |

Les chiffres sont issus d'un réseau **local** et ne sont **pas extrapolables** au réseau mobile, à une charge simultanée ou à un téléphone physique. Les captures ont été inspectées : carte mobile prioritaire, couleurs de périodes visibles, 12 classes périodes et 6 classes hauteurs, pas de débordement. En cas de **HTTP 503 simulé**, une nouvelle sélection est refusée et la couche précédente est conservée. Aucune requête externe de carte/données n'a été observée.

Tests sur branche : **35/35 Node**, **56/56 Python** (depuis clone GitHub propre), plus audit exhaustif de tous les fichiers et vraie recette Chromium. La grille n'est **pas encore branchée sur le site VACANT** ; ce travail est indépendant de la PR #21, qui reste limitée au laboratoire de 150 emprises.

## Publication et ODbL : points à respecter

Les sections [4.2 à 4.6 de l'ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/) précisent :
- Attribution publique et maintien des notices/source/licence ;
- base adaptée utilisée publiquement soumise aux conditions de partage à l'identique (ODbL ou compatible) ;
- mise à disposition de la base adaptée exploitable par machine **ou** de la méthode/différences permettant de la reconstruire, suivant la licence ;
- ne pas imposer de restriction technique incompatible à une redistribution.

Ces obligations **ne prohibent pas** le développement privé. La future publication doit offrir une réelle voie de récupération de la base adaptée, une notice ODbL visible et les détails de provenance, dates, exclusions et transformations. Cette synthèse n'est pas un avis juridique définitif. La réponse de l'Apur affinera la date métier et, si nécessaire, l'attribution.

## Suites, sans changer de production

1. Étudier le poids réseau et la mise en cache de cellules, les plafonds réels et la performance d'un téléphone physique ; envisager compression Brotli/gzip, GeoJSON simplifié **avec tolérance et audit** ou PMTiles.
2. Définir le contrat de distribution ODbL et de version du dérivé **avant publication** : manifeste public, attributs limités, chemin de récupération et protocole de mise à jour.
3. Relier la grille privée au mode laboratoire de la PR #21, avec recette de passage entre volumes Paris Data, périodes, hauteurs et statistiques IRIS/arrondissements.
4. À ce stade, aucune promotion `main` et aucun changement du site public `vacant.kiwinokoto.fr`.
