# VACANT — publication de la base adaptée Apur sous ODbL 1.0

**17 octobre 2026 — dossier de préparation contrôlée.** Ne pas considérer ce document seul comme une preuve de déploiement. GitHub est la source du code, les archives originales restent sur VPS privé.

## Licences et attribution

Source de la base d'origine : **© Atelier parisien d'urbanisme (Apur)**, [EMPRISE_BATIE_PARIS](https://opendata.apur.org/datasets/emprise-batie-paris), sous [Open Database License 1.0](https://opendatacommons.org/licenses/odbl/1-0/). Les conditions et limitations de l'Apur sont précisées dans sa [page de présentation](https://www.apur.org/fr/open-data-cartes/open-data/emprises-baties-paris-metropole-une-lecture-tissu-urbain) et le résumé de licence associé. 

La **base dérivée publiée est elle-même distribuée sous ODbL 1.0** : téléchargement sans inscription de toutes les emprises retenues (format GeoJSON lisible par machine), fichier de provenance/attribution, et manifeste vérifiant chaque fichier SHA-256. Les dispositions pertinentes incluent les sections **4.2, 4.3, 4.4 et 4.6** (notices, attribution, partage à l'identique et accès à une base dérivée). Les droits éventuellement indépendants sur des contenus particuliers doivent être examinés séparément. Ceci n'est pas un avis juridique.

En cas de publication de VACANT, fournir les ressources sous :
- `/data/apur-grid/manifest.json` : manifeste public, attribution, licence, géographie, qualité, SHA-256 de **chacune des 456 cellules**.
- `/data/apur-grid/cell_<x>_<y>.geojson` : toutes les **456** cellules géographiques lisibles par machine ; une emprise traversant plusieurs cellules est répétée et identifiée par `object_id`.
- `/data/apur-grid/apur-paris-grid-500m-2026-10-16-odbl.zip` : **archive complète téléchargeable**, incluant les 456 cellules, le manifeste et la notice.
- `/data/apur-grid/NOTICE.md` : source officielle, attribution, adresse de la licence, transformations, restrictions scientifiques.

Le code `scripts/build_apur_private_grid.py` et `scripts/package_apur_public.py` documente la transformation, avec dépendances Shapely, Pyproj et pyshp.

## Contrat scientifique (sans inventer un millésime)

Original archivé le **16 octobre 2026** : archive SHP `EMPRISE_BATIE_PARIS.shp.zip`, **31 981 417 octets**, SHA-256 `f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11`. Le **millésime scientifique exact reste à confirmer**. Une date de modification du service ou de l'objet ne prouve pas la date de construction.

| Étape | Valeur vérifiée |
|---|---:|
| Emprises source | 128 206 |
| Invalides topologiques GEOS exclues | 104 |
| Identifiants métier manquants exclus | 13 |
| Emprises uniques dérivées | 128 089 |
| Cellules de 500 m (Lambert-93) | 456 |
| Placements, doublons de cellules compris | 138 381 |
| Projection de sortie | EPSG:4326 (WGS84) |
| Attributs d'une emprise | `object_id`, `period_code`, `height_m` |
| Géométries | Non simplifiées, non corrigées, non découpées ; dupliquées par cellule si nécessaire |

`height_m` est la hauteur médiane `h_med` de l'Apur **en mètres**, jamais le nombre d'étages `H_ET_MAX` des volumes Paris Data. `period_code` est une période attribuée **à une emprise contemporaine**, pas la preuve qu'un bâtiment était présent à une date historique précise. **Aucun statut individuel de vacance, de logement ou de propriétaire** n'est contenu ou inféré dans cette base.

## Publication contrôlée

Le seul canal autorisé pour ajouter la base à une release statique est **`scripts/stage_reviewed_release.py`**, après revue du code et des droits, avec les drapeaux `--execute --publish-apur` et quatre arguments explicites :

- `--apur-private-dir` : copie privée vérifiée des cellules, **en dehors de toute racine web** ;
- `--apur-private-manifest-sha256` : `bb02fe9ac9ef7919018118659e12ac533b098234250eba540c6975e7b273bb0c` ;
- `--apur-public-manifest-sha256` : `2b0683c33e236b906163c73786133f300182ccc4f00c70485bbcf1e84eb75711` ;
- `--apur-public-zip-sha256` : `9bef60651f2b0f20158392157ffe2e0a6757257a57757532348384e4521e9e24`.

Ce mécanisme refuse une archive privée altérée, une cellule changée, un fichier inattendu ou une release déjà existante. Sans l'option **`--publish-apur`**, aucune cellule Apur n'est ajoutée à la release. Les données publiques IRIS/arrondissements demeurent soumises à leurs propres SHA-256.

La préparation a été réellement validée sur un checkout GitHub avec les données complètes : **459 fichiers** dans `site/data/apur-grid/` (456 cellules, 1 manifeste, 1 notice, 1 ZIP), dossier et fichier en lecture pour Nginx. La base complète reste **hors GitHub**.

## Recette navigateur HTTPS

La branche de préparation a été testée en **HTTPS** sous le nom `vacant.kiwinokoto.fr` redirigé localement dans Chromium (certificat éphémère), sur desktop **1280×800** et mobile simulé **390×844**. Les **2 284 objets uniques du secteur visible**, quatre cellules, étaient vérifiés SHA-256, les légendes périodes (12 classes) et hauteurs (6 classes) s'affichaient, le changement de coloration ne provoquait **aucune requête supplémentaire**. Pas d'erreur JavaScript, débordement horizontal ou requête externe vers l'API Apur. L'aperçu ancien privé de 150 emprises est masqué sur le domaine public.

**Cette recette n'est pas une mesure de débit 4G ni une validation d'un déploiement public.** Une fois la nouvelle release activée, contrôler les URL réellement publiées, les réponses 200, le Content-Encoding et le certificat, et disposer d'une procédure de retour arrière vers la précédente release.

## Principe de fusion

Les PR **#23 → #24 → #25** sont empilées, cette passe est une quatrième PR empilée après #25. Les merges ne doivent pas écraser l'ascendance de six branches Apur originales et doivent être exécutés **uniquement après validation de chaque tête GitHub**. Pas de direct push main, pas d'opération destructive. La publication dépend d'une activation explicite de la nouvelle release statique sous lease AgentCTL, avec tests de santé et rollback possible.
