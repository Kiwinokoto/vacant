# VACANT — sources réelles et stockage (16 octobre 2026)

## Décision : VPS personnel, espace privé

Après vérification de l'identité du serveur, du stockage disponible et de l'absence de travail concurrent/lease AgentCTL, utiliser **/srv/vacant/data/**, hors racine HTTP.

- `raw/insee/<id>/` : originaux intacts, immuables.
- `manifests/` : provenance, date UTC, taille en octets, SHA-256, URL finale HTTP et millésime.
- `processed/` : dérivés à construire après audit, jamais écrits par le collecteur.
- GitHub public : seulement code, documentation, métadonnées non sensibles et résultats ouverts préalablement validés.

**État : aucun fichier encore téléchargé ni stocké sur le VPS** : RDC personnel hors ligne lors de deux vérifications et téléchargements conteneur indisponibles.

## Téléchargements Insee confirmés sur les pages officielles

| Identifiant | Recensement / géographie | Format et source vérifiée |
| --- | --- | --- |
| `rp2006` | 2006 / 2008 | [XLS 2006](https://www.insee.fr/fr/statistiques/fichier/2028562/BTX_IC_LOG_2006.xls) |
| `rp2011` | 2011 / 2013 | [ZIP 2011](https://www.insee.fr/fr/statistiques/fichier/2028269/infra-logement-2011.zip) |
| `rp2016` | 2016 / 2018 | [ZIP 2016](https://www.insee.fr/fr/statistiques/fichier/4228432/base-ic-logement-2016.zip) |
| `rp2023` | 2023 / 2025 | [Parquet 2023, Insee/Melodi](https://api.insee.fr/melodi/file/DS_RP_LOGEMENT_PRINC_IRIS_2023/PARQUET) |
| `rp2023-passage` | 2023 / 2025 | [Correspondance des dimensions RP2023](https://www.insee.fr/fr/statistiques/fichier/9061333/table_passage_logement.xlsx) |

Les URL et millésimes figurent dans [les pages Insee RP2006](https://www.insee.fr/fr/statistiques/2028562), [RP2011](https://www.insee.fr/fr/statistiques/2028269), [RP2016](https://www.insee.fr/fr/statistiques/4228432), [RP2023](https://www.insee.fr/fr/statistiques/9061333). URLs vérifiées **documentairement** mais aucun téléchargement HTTP réussi dans cette session.

Le fichier `RP2023` est harmonisé : ne pas confondre résidences principales (`DW_MAIN`) et logements vacants. Conserver la table de passage originale.

## Procédure sur le VPS — non exécutée

1. Vérifier que le bon VPS est connecté, qui travaille dessus, les locks/leases AgentCTL actifs, les ressources disque/inodes (`df -h`, `df -i`), les droits et les sauvegardes. Un lock actif interdit d'écrire. Ne pas toucher aux services existants.
2. Après validation, créer le dossier privé `/srv/vacant/data` avec les droits minimaux nécessaires et sans exposition HTTP. Ne pas modifier récursivement les propriétaires d'un arbre inconnu.
3. Depuis une copie propre du dépôt : lancer l'aperçu **sans écriture** :

   ```sh
   python3 scripts/collect_insee.py --fetch rp2023 rp2023-passage
   ```

4. Si conditions validées, exécuter la collecte explicite :

   ```sh
   python3 scripts/collect_insee.py --root /srv/vacant/data --fetch rp2023 rp2023-passage --execute
   python3 scripts/collect_insee.py --root /srv/vacant/data --fetch rp2006 rp2011 rp2016 --execute
   ```

5. Inspecter les cinq manifestes, signatures, empreintes, contenu et schémas. La collecte seule ne suffit pas à dire qu'une maille IRIS est couverte, comparable ou publiable.

## Contours IGN : source exacte 2025 identifiée

[Contours...IRIS IGN (Licence Ouverte 2.0)](https://www.data.gouv.fr/datasets/contours-iris-r-2), [catalogue de téléchargement Géoplateforme](https://data.geopf.fr/telechargement/capabilities), [documentation officielle de l'API](https://cartes.gouv.fr/aide/fr/guides-utilisateur/utiliser-les-services-de-la-geoplateforme/telechargement/). Le recensement RP2023 requiert la géographie **01/01/2025**, donc ne pas prendre par commodité une édition 2024 ou 2026. Identifier la ressource **2025** et contrôler son contenu et sa licence avant téléchargement. Aucun identifiant de fichier IGN n'est inventé ici.

## Sécurité et reproductibilité

Le collecteur Python n'a aucune dépendance externe, affiche l'inventaire sans écrire par défaut, impose `--execute`, vérifie la destination HTTPS Insee, limite la taille à 750 Mio, contrôle les signatures binaires et refuse HTML, calcule SHA-256 en continu, conserve immutables les originaux et refuse tout écrasement. `flock` évite la concurrence entre instances du collecteur **mais ne remplace pas AgentCTL**.

Tester par `python3 -m unittest discover -s tests -p 'test_collect_insee.py' -v` (fixtures de données synthétiques uniquement dans les tests ; jamais dans la carte).

Aucune donnée LOVAC individuelle, aucune estimation à l'adresse, aucune exposition publique ou déploiement dans cette passe.

## Premiers résultats constatés sur le VPS — 16 octobre 2026

Téléchargements **effectués et tests réellement exécutés** sur le VPS personnel, sous lease AgentCTL `state:vacant`, avec code GitHub à `47aa9bac2f50121f43163c9103e0abaffb22b427`. Originaux dans `/srv/vacant/data/raw/insee/`, avec manifestes horodatés sous `/srv/vacant/data/manifests/` :

| Dataset | Taille en octets | SHA-256 |
| --- | ---: | --- |
| `rp2006` | 74348544 | `20d81952ac0e8032bbd9ab38e5d8d1b86c708fb6090ce3809cd7a44566f2ee88` |
| `rp2011` | 29531432 | `c05249a8512e0f237347b889fdc6462e471ab189ebb1a09549a8be67bfa35e50` |
| `rp2016` | 32677503 | `ca1f44bac285f7cebbb1a223d821877381e123db80e0bc1269848348f6dda40c` |
| `rp2023` | 47461890 | `aa44509bec7d3aa5a3bef399c082c79433b1617fdb13f81370e39bfa6d5db661` |
| `rp2023-passage` | 14423 | `a3a0ce33bcd4080734403ca6107667e0b6dcdd2467e085e46fe00bd363b5f34f` |

Validation native : `node --test tests/*.test.mjs` = **14/14 OK** ; `python3 -m unittest discover -s tests -p 'test_collect_insee.py'` = **6/6 OK**. Dépendances de traitement installées dans **`/srv/vacant/venv` isolé** (Python 3.12, DuckDB 1.4.1, openpyxl 3.1.5, xlrd 2.0.2, pyshp 2.3.1, pyproj 3.7.2), pas au niveau global.

Le Parquet RP2023 réellement ouvert contient 5 066 022 observations nationales ; le dictionnaire XLSX révèle `RP_MEASURE=DWELLINGS`, `OCS=DW_VAC` pour vacants, `OCS=_T` pour logements totaux, `TDW=_T` pour l'ensemble des logements. Cette vérification est préliminaire : filtrage précis et contrôle des effectifs à produire et tester.

### Deux nouvelles sources découvertes

- [Table d'appartenance IRIS au 1er janvier 2025](https://www.insee.fr/fr/statistiques/fichier/7708995/reference_IRIS_geo2025.zip) : identifiants indépendants, **pas** géométrie. Id de collecte `iris-ref2025`, via `scripts/collect_insee.py`.
- [IGN Contours...IRIS édition 2025 GeoParquet WGS84G](https://data.geopf.fr/telechargement/resource/CONTOURS-IRIS/CONTOURS-IRIS_3-0__GEOPARQUET_WGS84G_FRA_2025-01-01), [fichier concret](https://data.geopf.fr/telechargement/download/CONTOURS-IRIS/CONTOURS-IRIS_3-0__GEOPARQUET_WGS84G_FRA_2025-01-01/contours_iris.parquet) : géométrie correspondant au millésime RP2023. Collecteur distinct `scripts/collect_ign.py` avec HTTPS strict, SHA-256, original immuable et manifeste. Déterminer couverture et code IRIS après téléchargement réel.

Commandes sous garde AgentCTL une fois le nouveau code GitHub récupéré sur VPS :
```sh
python3 scripts/collect_insee.py --root /srv/vacant/data --fetch iris-ref2025 --execute
python3 scripts/collect_ign.py --root /srv/vacant/data --execute
```
