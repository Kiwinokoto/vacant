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

## Contours IGN : sélection non finalisée

[Contours...IRIS IGN (Licence Ouverte 2.0)](https://www.data.gouv.fr/datasets/contours-iris-r-2), [catalogue de téléchargement Géoplateforme](https://data.geopf.fr/telechargement/capabilities), [documentation officielle de l'API](https://cartes.gouv.fr/aide/fr/guides-utilisateur/utiliser-les-services-de-la-geoplateforme/telechargement/). Le recensement RP2023 requiert la géographie **01/01/2025**, donc ne pas prendre par commodité une édition 2024 ou 2026. Identifier la ressource **2025** et contrôler son contenu et sa licence avant téléchargement. Aucun identifiant de fichier IGN n'est inventé ici.

## Sécurité et reproductibilité

Le collecteur Python n'a aucune dépendance externe, affiche l'inventaire sans écrire par défaut, impose `--execute`, vérifie la destination HTTPS Insee, limite la taille à 750 Mio, contrôle les signatures binaires et refuse HTML, calcule SHA-256 en continu, conserve immutables les originaux et refuse tout écrasement. `flock` évite la concurrence entre instances du collecteur **mais ne remplace pas AgentCTL**.

Tester par `python3 -m unittest discover -s tests -p 'test_collect_insee.py' -v` (fixtures de données synthétiques uniquement dans les tests ; jamais dans la carte).

Aucune donnée LOVAC individuelle, aucune estimation à l'adresse, aucune exposition publique ou déploiement dans cette passe.
