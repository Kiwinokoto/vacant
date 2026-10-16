# VACANT — gel vérifiable d'un export Apur et contrôle SIG étendu

**Contrôle réalisé le 16 octobre 2026.** **Recherche interne seulement**, pas une nouvelle couche cartographique publiée. Dépôt source de vérité : `Kiwinokoto/vacant` ; `main` au démarrage : `72a9d06377541b7b266e0d8153e89a7ae19afb95`. Les PR #17 et #18 restent séparées, en brouillon.

## Export source préservé

- Fournisseur : **Apur**, item du catalogue public `85fa0a4303744ad4ab6e2a89882b5fca` (`EMPRISE_BATIE_PARIS`), couche 0.
- URL officielle de téléchargement : https://opendata.apur.org/api/download/v1/items/85fa0a4303744ad4ab6e2a89882b5fca/shapefile?layers=0 ; URL résolue par le portail : `hub.arcgis.com/api/v3/datasets/85fa0a4303744ad4ab6e2a89882b5fca_0/downloads/data?format=shp&spatialRefId=2154&where=1%3D1`.
- En-tête HTTP `Last-Modified` du **fichier téléchargeable** : **13/10/2026 16:39:04 GMT**. C'est une date de fichier/cache, **pas une date de référence métier**.
- Original privé : `/srv/vacant/data/raw/apur/frozen-2026-10-16/EMPRISE_BATIE_PARIS.shp.zip`, **31 981 417 octets**, SHA-256 :

  `f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11`

- ZIP intègre `.shp`, `.shx`, `.dbf`, `.prj`, `.cpg`, contrôle CRC complet réussi. Le JSON de catalogue, le XML Géocatalogue et un `manifest.json` contenant les URL, empreintes et dates sont **archivés uniquement sur le VPS privé** (dossier mode 0700, fichiers en lecture seule), **pas dans GitHub ni dans `site/`**. Le manifeste a été créé une seule fois, sans écraser de source. Aucune donnée LOVAC individuelle.

## Datation : conflit documenté, ne pas inventer de millésime

- [Fiche Apur 2019](https://www.apur.org/open_data/EMPRISE_BATIE_OD.pdf) : référentiel descriptif, ODbL.
- [Fiche Apur septembre 2024](https://www.apur.org/fr/open-data-cartes/open-data/emprises-baties-paris-metropole-une-lecture-tissu-urbain) : annonce notamment des orthophotographies jusqu'en 2024.
- Enregistrement officiel API de catalogue `/api/search/v1/collections/dataset/items/85fa0a4303744ad4ab6e2a89882b5fca` : création du catalogue **09/07/2025**, modification **30/07/2026** (ne pas confondre avec le millésime des emprises).
- Fiche géocatalogue XML, ID `28f07fd4-937b-4489-9331-90b4602d8cab` : **`lastUpdate=2025-02`** pour la ressource, mais **révision de métadonnées le 01/09/2026**.
- Le champ attributaire **`last_edi_1` de l'export figé contient au moins une date au 11/09/2026**, et d'autres champs portent des dates de 2026. **La valeur `lastUpdate=2025-02` ne peut donc pas dater intégralement le contenu effectivement archivé.** La date d'édition de fiche ou de ligne n'est pas l'année de construction.
- **Millésime métier effectif : NON CONFIRMÉ.** Un courriel a été **envoyé à data@apur.org le 16/10/2026** pour obtenir l'attestation de version, les modalités ODbL et le bon dictionnaire des périodes. Ne pas réexpédier avant consultation du fil Gmail.

## Audit attributaire exhaustif de l'archive

| Mesure | Résultat |
|---|---:|
| Lignes SHP/DBF | **128 206** |
| `n_sq_eb` manquant | **13** |
| Doublons parmi `n_sq_eb` non nuls | **0** |
| `an_const` manquante | **47 056** |
| `c_perconst=99` (non daté) | **7 786** |
| `c_perconst` nul | **8** |
| `h_med` manquante | **39** |
| `h_med=0` | **77** |
| `h_med > 200 m` | **3** |
| `h_med < h_min` | **347** |
| `h_med > h_max` | **18** |

Les anomalies métriques peuvent se recouper, les nombres **ne sont pas additionnables**. Les codes de période concordent avec le dictionnaire Apur (11 = 2000–2007, 12 = 2008 et après), avec deux groupes sans datation (99 et NULL). Une valeur atypique n'est pas automatiquement erronée : Tour Eiffel et Tour Montparnasse restent des cas plausibles.

## Audit GEOS déterministe sans redistribution

Sélection **`OBJECTID % 17 == 0` ou période non datée ou `h_med > 200`**, sur l'ensemble de l'archive ; cette règle privilégie volontairement les cas fragiles et **ne constitue pas un échantillon probabiliste représentatif**.

| Mesure | Résultat |
|---|---:|
| Géométries contrôlées avec Shapely/GEOS | **14 871** |
| Polygon | 14 846 |
| MultiPolygon | 25 |
| Polygones présentant une auto-intersection d'anneau | **6** |
| Cellules d'une grille parisienne 5×5 contenant un échantillon | 21 sur 25 |

Les MultiPolygon et anomalies de topologie appellent une investigation ciblée avant simplification, tuilage ou activation UI. La validation JavaScript de la PR #18 contrôle l'intégrité de la structure, **pas la topologie GEOS**. On ne peut pas extrapoler le nombre total d'invalides à partir de cet échantillon biaisé.

## Reproductibilité et blocages

Audit reproductible, sans réseau ni fichier géométrique généré :

```sh
/srv/vacant/venv/bin/python scripts/audit_apur_frozen_export.py \
  /srv/vacant/data/raw/apur/frozen-2026-10-16/EMPRISE_BATIE_PARIS.shp.zip \
  /srv/vacant/data/raw/apur/frozen-2026-10-16/manifest.json
```

Le programme vérifie SHA-256, taille, CRC, membres ZIP, compte, valeurs attributaires et qualité GEOS d'un échantillon borné. Bibliothèques déjà présentes sur le VPS : pyshp, Shapely, pyproj. Résultats sur clone GitHub de la branche : **53/53 Python et 25/25 Node**, puis audit du ZIP réel réussi. Aucun navigateur n'a été relancé lors de cette passe ; le prototype local de la PR #18 avait été recetté auparavant.

**Décisions :** maintenir les PR #17/#18 en brouillon et hors production. Avant publication, qualifier les six géométries invalides et les 13 emprises sans clé métier, vérifier les obligations ODbL pour une base adaptée, obtenir une réponse Apur sur le millésime et tester la performance/attribution de la future couche publique. La vacance Insee demeure **territoriale**, jamais affectée aux emprises bâties.
