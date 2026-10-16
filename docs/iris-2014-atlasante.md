# VACANT — recoupement institutionnel Atlasanté « IGN – Métropole – IRIS 2014 »

Audit du 16 octobre 2026. **État : preuve géométrique forte, droits et millésime exact de l'édition 2013 à confirmer avant publication.**

## Source obtenue

- Catalogue institutionnel [Atlasanté – IGN Métropole IRIS 2014](https://catalogue.atlasante.fr/geonetwork/srv/api/records/1ad2743a-da7b-4f10-bab0-0bc016b5c7bb), [flux officiel Atom](https://catalogue.atlasante.fr/rss/atomfeed/atomdataset/1ad2743a-da7b-4f10-bab0-0bc016b5c7bb).
- ZIP de 16 411 555 octets téléchargé depuis le lien Atom le 16/10/2026 : archive SQL PostGIS EPSG:2154 (101 Mo non compressés) et métadonnées ISO 19139 embarquées. Stockage **privé** : `/srv/vacant/data/raw/secondary/iris-2014-atlasante/source.zip`.
- SHA-256 `5cefdde58d228b3f8643d01ef61c80c10bf4ce30a30e78b61e2dc48fdf9acf27`. Manifeste complet hors webroot : `/srv/vacant/data/manifests/iris-2014-atlasante-20261016.json`.
- La métadonnée porte **« IGN – Métropole – IRIS 2014 »**, avec une date de *publication de notice* 16/09/2013 et une révision 29/04/2015 : ces dates **ne sont pas une preuve automatique** de l'édition géométrique officielle 2013.
- La notice mentionne des **conditions d'utilisation IGN/Insee spécifiques**. Ne pas assimiler cette diffusion à la licence actuelle du portail IGN sans confirmation explicite.

## Preuves géométriques

Lecture en flux du SQL comme **texte non exécutable**, seules les insertions de la table attendue sont autorisées. Hex EWKB PostGIS décodé en Shapely en contrôlant le SRID 2154, sans instance PostgreSQL ni modification de données.

- 992 codes IRIS de Paris (1 observation par code), identiques aux 992 codes de référence Insee.
- 0 polygone invalide, 0 géométrie vide ; emprises dans Paris, surface totale d'environ 105 380 051 m².
- Comparaison à l'archive secondaire préexistante revendiquant la géographie **2013** (SHA-256 `c6afee56f81b3a9d08316034f0f48259162276a3d7a0d11388c2472f2fd5d3a7`) : 992 correspondances parfaites de codes et de formes à la précision numérique.
- **IoU minimale : 1,0000000000** à dix décimales ; médiane 1,0000000000. Différence symétrique maximale **0,000008961 m²**, compatible avec la simple reprojection WGS84 → Lambert-93 du candidat 2013.
- L'audit antérieur confirme en outre que les 10 répétitions par IRIS dans cette republication tierce diffèrent de moins de 0,001 m² et ne sont pas des géométries concurrentes.

C'est une **corroboration institutionnelle très forte de la provenance géométrique** du candidat 2013. En revanche, il manque une confirmation du rattachement du fichier Atlasanté « 2014 » à l'édition *statistique-géographique* 2013, et une permission claire de diffuser ses polygones dérivés.

## Reproductibilité et décision de diffusion

```sh
/srv/vacant/venv/bin/python scripts/audit_iris2014_atlasante.py --data-root /srv/vacant/data
/srv/vacant/venv/bin/python -m unittest discover -s tests -p 'test_*.py' -q
node --test tests/*.test.mjs
```

Le script refuse les anomalies SHA, archives inattendues, SQL hors contrat, géométries invalides, mauvais SRID, doublons ou discordance de formes. **Il n'exécute aucune instruction SQL et ne produit aucun dérivé public.**

Décision : conserver cette source et le dérivé IRIS RP2011 **privés**, sans remplacer la carte historique par arrondissements. La demande à l'IGN, dans [demande-archives-ign.md](demande-archives-ign.md), inclut désormais les **deux empreintes de données identiques géométriquement** pour obtenir une confirmation formelle du millésime et des droits. Chercher ensuite indépendamment les éditions correspondant aux RP2006 et RP2016 (géographies 2008 et 2018).
