# VACANT — premiers états réels de bâtiments IGN, 2008 / 2011 / 2018

**Audit exploratoire du 17 octobre 2026. Aucune modification de la production.**

## Résultat scientifique

Trois archives d'éditions antérieures de **BD TOPO** pour le département **D075 Paris** ont été retrouvées sur le miroir `data.cquest.org`, téléchargées en lecture seule puis figées sur le VPS. Leur attribution est **© IGN**. Le catalogue officiel [BD TOPO Historique](https://www.data.gouv.fr/datasets/bd-topo-r-historique) indique une **Licence Ouverte v2.0** ; il reste prudent de confirmer les droits des fichiers précis issus de l'ancien miroir avant toute publication de dérivés, car il ne s'agit pas d'archives servies aujourd'hui directement par l'IGN.

Les archives sont des **photographies du référentiel BD TOPO à des dates déclarées**, et **pas des observations exhaustives de constructions et démolitions**. Les dates de réexport des fichiers ne sont pas celles de l'édition historique.

| Archive Paris | Taille | SHA-256 | Édition géographique selon métadonnées | Réexport / traitement du fichier |
|---|---:|---|---|---|
| [BDTOPO v2.0 / septembre 2008](https://data.cquest.org/ign/bdtopo/BDTOPO_2-0_2008-09/BDTOPO_2-0_TOUSTHEMES_SHP_LAMB93_D075_2008-09-14.7z) | 8 547 169 o | `64f4588c9ec8dbcce2c72ec7e7e24a142477996910fde80f24e81e2b13252d65` | 14/09/2008 | 23/05/2019 |
| [BDTOPO v2.0 / avril 2011](https://data.cquest.org/ign/bdtopo/BDTOPO_2-0_2011-04/BDTOPO_2-0_TOUSTHEMES_SHP_LAMB93_D075_2011-04-12.7z) | 15 647 070 o | `5926330d42fd290b1008f266b5082a95e73c765ec06027fcc45b7721ea00a3ad` | 12/04/2011 | 05/10/2021 |
| [BDTOPO v2.2 / mars 2018](https://data.cquest.org/ign/bdtopo/BDTOPO_2-2_2018-03-29/BDTOPO_2-2_TOUSTHEMES_SHP_LAMB93_D075_2018-03-29.7z) | 15 442 618 o | `0bf421c0e7092c8dfe343e6506ec605c92d88a1f78d19a0b075bafca641d88b9` | 29/03/2018 | 14/04/2018 |

Ces archives comportent les fichiers **Shapefile** `BATI_INDIFFERENCIE`, `BATI_INDUSTRIEL`, `BATI_REMARQUABLE`, la projection **Lambert-93 EPSG:2154**, des ID `BATIMENT...`, une valeur `HAUTEUR` et des métadonnées XML. L'année de construction **n'est pas une variable démontrée ici**. Le fichier 2008 présente notamment un nombre d'objets incomparablement plus faible.

## Contrôles des populations d'objets

| Classe SHP | 2008 | 2011 | 2018 |
|---|---:|---:|---:|
| `BATI_INDIFFERENCIE` | 23 695 | 115 140 | 113 623 |
| `BATI_INDUSTRIEL` | 1 271 | 1 471 | 2 057 |
| `BATI_REMARQUABLE` | 772 | 819 | 1 092 |
| **Total ID uniques** | **25 738** | **117 430** | **116 772** |

Les polygones couvrent les coordonnées de Paris, mais le **saut de cardinalité 2008 → 2011 ne doit pas être traité comme 91 692 constructions nouvelles**. La couverture et/ou les méthodes de saisie de 2008 sont à examiner plus avant. Aucun graphique de « bâtiments apparus » ne doit tirer cette conclusion.

| Paires de fichiers | ID communs | % des ID de la première édition | % des ID de la seconde |
|---|---:|---:|---:|
| 2008 ↔ 2011 | **1 557** | **6,05 %** | **1,33 %** |
| 2011 ↔ 2018 | **113 634** | **96,77 %** | **97,31 %** |
| 2008 ↔ 2018 | **1 266** | **4,92 %** | **1,08 %** |

**Décision : 2011 et 2018 méritent une comparaison exploratoire ; 2008 est exclu de tout calcul direct d'évolution à ce stade.** Les ID communs ne prouvent toutefois pas la permanence physique d'un bâtiment, pas plus que des ID différents ne prouvent une démolition : le référentiel et les noms de classes peuvent évoluer.

### Test de stabilité géométrique (échantillon déterministe de 1 %)

Filtre reproductible : `crc32(ID) % 100 == 0`, **sans tirage aléatoire**. Dans le couple 2011–2018 :

- 1 172 objets retenus en 2011 ; 1 166 en 2018 ;
- 1 128 ID communs ; **1 120 polygones aux listes de coordonnées exactement identiques** et **8 différents** ;
- parmi les ID communs, **14 changements de classe** et **72 changements de valeur `HAUTEUR`**.

Il est impossible de distinguer à ce stade une **correction cartographique**, un **changement réel** et une **reclassification** à partir de ces seules différences. Les hauteurs BD TOPO ne sont pas les hauteurs médianes des emprises Apur : pas de jointure automatique.

## Concordance géométrique exhaustive 2011 ↔ 2018 (audit complémentaire)

**Réalisé le 17/10/2026 sur les mêmes archives SHP privées et les identifiants complets.** Nouveau script reproductible `scripts/compare_ign_geometry.py` : vérification des SHA-256 source et métadonnées, lecture des trois classes de bâti, empreinte BLAKE2b des coordonnées exactes Lambert-93 et indices des anneaux ; calcul GEOS du recouvrement par `intersection / union` uniquement lorsque **le même ID** présente des coordonnées différentes.

| Mesure documentaire | Résultat |
|---|---:|
| Objets BD TOPO dans l'édition 2011 | 117 430 |
| Objets dans l'édition 2018 | 116 772 |
| **Identifiants communs** | **113 634** |
| Identifiants présents uniquement dans l'édition 2011 | **3 796** |
| Identifiants présents uniquement dans l'édition 2018 | **3 138** |
| **Coordonnées géométriques exactement identiques**, ID commun | **112 567** |
| **Coordonnées différentes**, ID commun | **1 067** |
| Classe cartographique différente, ID commun | 1 442 |
| Attribut hauteur différent, ID commun | 8 815 |

Les deux dernières lignes portent sur **l'attribut de l'objet BD TOPO** et ne sont pas nécessairement incluses dans les 1 067 corrections de géométrie ; elles peuvent se superposer ou être indépendantes.

Pour les **1 067** formes modifiées correspondant à un ID commun, comparaison exacte de surface dans la projection Lambert-93 :

- **recouvrement médian (IoU) : 0,908579** ;
- **353** présentent **au moins 99 %** de recouvrement (formes quasi identiques malgré modification de sommets) ;
- **176** présentent **moins de 50 %** de recouvrement (changements importants ou situations complexes) ;
- aucune forme invalide/union vide/erreur GEOS sur cette sous-population.

**Interprétation impérative :** les 3 796 et 3 138 identifiants propres à une édition ne sont pas « des destructions » et « des constructions ». De même, une correction de contour, d'angle, de classe ou de valeur de hauteur peut être **une révision du référentiel sans modification physique du bâti**. Aucun taux de vacance n'est inféré. Les rapprochements d'objets distincts (scissions, fusions, remplacement d'identifiants, n:m) restent à étudier **spatialement** avant une série de transformations historiques.

Le rapport détaillé agrégé, sans coordonnées ni identifiants, est conservé uniquement sur le VPS à `/srv/vacant/data/processed/ign/bdtopo-historic-audit-20261017/audit-spatial-2011-2018-verified-private.json`. Les fichiers SHP ne sont ni joints ni publiés. Exécution reproductible :

```sh
/srv/vacant/venv/bin/python scripts/compare_ign_geometry.py \
  --archive-dir /srv/vacant/data/raw/ign/bdtopo-historical-20261017 \
  --unpacked-dir /srv/vacant/data/processed/ign/bdtopo-historic-audit-20261017 \
  --output /srv/vacant/data/processed/ign/bdtopo-historic-audit-20261017/nouveau-rapport-private.json
```

La commande exige un **nouveau nom de sortie**, sans écrasement, et refuse une archive dont le SHA diffère. Les tests synthétiques `tests/test_compare_ign_geometry.py` couvrent l'identité des coordonnées, les modifications et les ratios de recouvrement. **Ne pas diffuser cette couche comme une animation d'événements bâtis réels** sans étude complémentaire des objets non appariés.

## Essai de cartographie locale 2011 ↔ 2018

Trois petites collections GeoJSON ont été dérivées **privément** d'une même zone WGS84 `[2.373,48.854,2.376,48.856]`, transformation EPSG:2154 vers WGS84, **sans découper ni inventer de contours**. Résultats sur les trois classes :

- **2008 : 22** polygones. SHA-256 du fichier privé `6c67a2b6f09f06e3f603e04748736bc2a53be0e987f4574780218a5ac2d2556a`.
- **2011 : 96** polygones. SHA `3cfec60c0c834436e8355b93a1af2cc71008cad539eb8faf3c81b7d4528a324d`.
- **2018 : 97** polygones. SHA `0b2ecfff9e35db228fddfa5f614b32f762ef98b05f8aae2d098ece9b8dfde7f3`.

Le comparateur **`experiments/ign-history/index.html?ign_lab=1`** est réservé à localhost, avec les fichiers sous `experiments/ign-history/_local/2011.geojson` et `2018.geojson`, ignorés par Git. Deux cartes synchronisées, côté à côté sur ordinateur ; empilées sur écran étroit. Il utilise Leaflet Canvas, et **n'est jamais embarqué dans la release statique `site/`**.

Recette Chromium sur Ubuntu avec vraies petites géométries : desktop **1280×800** et mobile simulé **390×844**, **deux Canvas cartographiques présents**, 96/97 objets chargés et 96 ID communs, aucun débordement ni erreur JavaScript. Le mode sans `?ign_lab=1` est refusé. Le premier test comptait à tort les éléments SVG, or l'application utilise Canvas ; le contrôle corrigé est réussi. Les fichiers privés de recette doivent être nettoyés.

## Reproduction et stockage

- Archives originales figées (0700/0600) sous `/srv/vacant/data/raw/ign/bdtopo-historical-20261017/`, avec `acquisition-manifest.json` et SHA.
- Sélection des composants `E_BATI` dans les 7z et métadonnées XML en environnement isolé, sans extraction libre de chemins inconnus, sous `/srv/vacant/data/processed/ign/bdtopo-historic-audit-20261017/<date>/`.
- Manifeste de comptage et comparaisons : `audit-manifest-geometry-private.json` dans le dossier parent.
- Script source : `scripts/audit_ign_historic_snapshots.py`. Il bloque les archives absentes ou altérées, les schémas et projections divergents, les ID dupliqués et les métadonnées incompatibles. Il calcule les populations, les intersections d'ID et l'échantillon géométrique déterministe.
- Tests : `tests/test_audit_ign_historic_snapshots.py` et `tests/ign-history-preview.test.mjs`. **Aucun SHP, ZIP/7z, GeoJSON ni extrait de coordonnées n'est suivi par Git.**

Commande d'audit local VPS (sans extraction ni téléchargement automatiques) :

```sh
/srv/vacant/venv/bin/python scripts/audit_ign_historic_snapshots.py \
  --archive-dir /srv/vacant/data/raw/ign/bdtopo-historical-20261017 \
  --unpacked-dir /srv/vacant/data/processed/ign/bdtopo-historic-audit-20261017 \
  --output /srv/vacant/data/processed/ign/bdtopo-historic-audit-20261017/nouvel-audit-prive.json
```

Utiliser un **nom d'output neuf** ; le script refuse l'écrasement. Python >=3.12, `pyshp` installé. Pour le déballage initial des archives 7z, `py7zr 1.0.0` a été installé **uniquement dans un dossier temporaire isolé**, jamais dans le runtime de production.

## Priorités suivantes

1. **Préciser la divergence de 2008** : couverture réelle par quartiers, densité, source de saisie, éventuel reconditionnement historique (les coordonnées couvrent Paris mais les bâtiments recensés sont nettement moins nombreux). Aucun comptage d'événements avant résolution.
2. Comparer les **livraisons de 2018-03 et 2018-09** pour vérifier les changements de géométrie et le format fractionné `.7z.001` ; conserver provenance et SHA de toute nouvelle source.
3. Mesurer les corrections 2011–2018 par emprise, avec une méthode de concordance spatiale contrôlée et suivi des scissions/fusions, **pas** seulement par ID.
4. Lorsque la compatibilité et les droits historiques seront vérifiés, envisager une **couche historique datée distincte** sur VACANT, toujours séparée de l'indicateur de vacance résidentielle IRIS. Pour l'instant **aucun déploiement**.
