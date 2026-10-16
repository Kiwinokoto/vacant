# VACANT — audit des référentiels IRIS historiques (16/10/2026)

## Objet et verdict

Audit **des identifiants Insee**, pas des contours. Résultat : les 992 codes IRIS parisiens demeurent présents dans les références 2008, 2013, 2018 et 2025 ; les fichiers des recensements 2006, 2011, 2016 concordent chacun exactement avec leur géographie officielle. Aucune modification de code parisien dans la table de passage Insee 2008→2013.

**Non validé :** l'identité des géométries en 2008, 2013, 2018 et 2025. Les mêmes codes peuvent conserver des contours modifiés, notamment à la suite d'un recalage cartographique. Une archive de *table d'appartenance géographique* n'est pas un fichier SIG. Le site ne doit donc **pas** montrer les valeurs historiques à l'IRIS sur les contours 2025 sous prétexte que les identifiants coïncident.

## Provenance officielle, stockée hors webroot

Références : [Insee — tables géographiques](https://www.insee.fr/fr/information/7708995), [IGN — fonds de carte IRIS](https://www.insee.fr/fr/information/2017372).

| Archive | Géographie | SHA-256 exact (source téléchargée) |
| --- | --- | --- |
| [IRIS_table_geo2008.zip](https://www.insee.fr/fr/statistiques/fichier/7708995/IRIS_table_geo2008.zip) | 2008 | `c36c217a3e39bc00652580f59164a6b461d2154b4394f34a9472040add7f43d5` |
| [IRIS_table_geo2013.zip](https://www.insee.fr/fr/statistiques/fichier/7708995/IRIS_table_geo2013.zip) | 2013 | `e5398549dc6e08227bb8e1a713e01af4f8c1febbe63b18150047b507ec1a1e26` |
| [reference_IRIS_geo2018.zip](https://www.insee.fr/fr/statistiques/fichier/7708995/reference_IRIS_geo2018.zip) | 2018 | `09e6cc7e94d8c7a349229806c7abbb8d9f4be6d04270207a250dd5a332ca0e67` |
| [table_passage_geo2013_geo2008.zip](https://www.insee.fr/fr/statistiques/fichier/7708995/IRIS_table_passage_geo2013_geo2008.zip) | 2008→2013 | `a21c3c2eb28b1f1032e709cb4c3f6c284be6609f080a4372df96e1716e102e9d` |

Enregistrements immuables dans `/srv/vacant/data/raw/insee/<dataset-id>/` et manifestes horodatés dans `/srv/vacant/data/manifests/`. La référence 2025 déjà archivée : SHA-256 `57803d2b5d1670e0065f6febc1a3b98cf44a7420e8830ce198ceed5c6abd5006`.

## Résultats chiffrés

| Comparaison | Codes retirés | Codes ajoutés | Libellés différents | Types H/A/D modifiés |
| --- | ---: | ---: | ---: | ---: |
| 2008 → 2013 | 0 | 0 | 0 | 0 |
| 2013 → 2018 | 0 | 0 | 24 | 0 |
| 2018 → 2025 | 0 | 0 | 212 | 0 |
| 2008 → 2025 | 0 | 0 | 234 | 0 |

Chaque référentiel contient **861 IRIS d'habitat, 88 d'activité et 43 divers** pour Paris. Les changements de libellés sont purement textuels au regard de cet audit : ils **ne permettent ni d'établir ni d'exclure** un changement de limites. Les écarts ne sont pas additifs d'une période à l'autre.

Le fichier de passage fourni par l'Insee comporte 0 mouvement documenté pour Paris entre 2008 et 2013. Cela signifie **aucune correspondance de codes à traiter dans ce fichier**, pas une preuve d'égalité des tracés.

## Reproduire

Depuis le VPS privé, après avoir contrôlé l'absence de verrou actif :

```sh
python3 scripts/collect_insee.py --root /srv/vacant/data --fetch iris-ref2008 iris-ref2013 iris-ref2018 iris-passage2013-2008
# L'option --execute n'est requise que si les originaux ne sont pas déjà archivés.
/srv/vacant/venv/bin/python scripts/audit_iris_references.py --data-root /srv/vacant/data
```

Le script vérifie les manifestes, SHA-256, noms et structures d'archives, cardinalités, codes IRIS uniques, millésimes déclarés, concordance avec les fichiers de recensement bruts et table de passage. Les tests unitaires n'utilisent que des données synthétiques. Aucun GeoJSON de vacance ancien n'est produit.

## Candidats cartographiques et suites

- **IGN / Insee — Contours...IRIS, éditions historiques exactes 2008, 2013 et 2018 :** références faisant autorité ; fichiers historiques complets **non encore obtenus** et disponibilité actuelle à confirmer directement auprès de l'IGN. Le téléchargement IGN 2025 déjà contrôlé ne constitue pas une archive historique.
- Une diffusion secondaire de **Contours IRIS 2013 adaptés aux limites OSM** est répertoriée sur [data.gouv.fr](https://www.data.gouv.fr/datasets/decoupage-iris-combine-aux-limites-communales-openstreetmap), sous ODbL. Elle modifie certaines limites et **ne doit pas être présentée comme l'original IGN 2013** ; ses contraintes de redistribution doivent être étudiées séparément.
- Les fonds Région Île-de-France « Contours...Iris » diffusés actuellement sont étiquetés **édition 2024** ; ne pas les rebaptiser 2008/2013/2018.

**Condition avant toute carte IRIS historique :** date de l'édition de géométrie démontrée, URL et licence exactes, SHA-256 de l'original, projection et conversion vérifiées, cardinalité/identifiants couvrant Paris, validité et éventuels écarts topologiques, jointure sans ambiguïté avec le RP correspondant, puis test navigateur. En attendant la carte par arrondissement 2006–2023 déjà publiée est le niveau historique sûr.
