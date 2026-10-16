# VACANT — audit préalable des hauteurs et périodes de construction Apur

Date : **16 octobre 2026**. Audit en lecture seule, par requêtes **agrégées uniquement**, sans géométrie, identifiant individuel ou donnée d'adresse. **Source candidate, aucune nouvelle couche publique.**

## Sources vérifiées

- Documentation et licence : https://www.apur.org/fr/open-data-cartes/open-data/emprises-baties-paris-metropole-une-lecture-tissu-urbain
- Jeu de données : https://opendata.apur.org/datasets/emprise-batie-paris
- Service ArcGIS REST interrogé : https://carto2.apur.org/apur/rest/services/OPENDATA/EMPRISE_BATIE_PARIS/MapServer/0

L'Apur précise qu'une **emprise bâtie peut couvrir un ou plusieurs bâtiments**. Le site du jeu annonce une licence **ODbL**, qui exige revue des attributions et des obligations de rediffusion. Le millésime réel et la précision des attributs de ce service n'ont pas encore été établis à partir d'un export daté.

## Schéma effectivement observé

Polygones EPSG:2154. Champs : `n_sq_eb` identifiant séquentiel d'emprise ; `h_med`, `h_moy`, `h_min`, `h_max` **hauteurs en mètres** ; `an_const` année de construction ; `an_rehab` année de réhabilitation ; `c_perconst` période de construction (`99` = non daté). **Ne pas confondre** les hauteurs de l'Apur avec `H_ET_MAX` de Paris Data, qui est un nombre d'étages, ni une période avec une année précise. Une emprise Apur ne se joint pas directement à un volume Paris Data par simple identifiant.

## Résultats des requêtes réelles du 16/10/2026

| Statistique | Enregistrements |
| --- | ---: |
| Total emprises du service | **128 206** |
| Hauteur médiane `h_med` absente | 39 |
| Hauteur médiane égale à 0 m | 77 |
| Hauteur médiane positive disponible | **128 090** |
| Hauteur médiane négative | 0 |
| Hauteur médiane supérieure à 200 m | 3 |
| Année exacte `an_const` absente | **47 056** |
| Période `c_perconst` nulle | 8 |
| Période explicitement non datée (`99`) | 7 786 |
| Période documentée | **120 412** |

Soit environ **99,9 %** des emprises avec une hauteur médiane strictement positive et **93,9 %** avec une période documentée, contre **63,3 %** seulement avec une année précise de construction renseignée. La borne maximale statistique de `h_med` est **300 m** : les 3 enregistrements supérieurs à 200 m demandent une vérification avant affichage (artefacts ou cas atypiques). Le service ne certifie pas ici l'exactitude de chaque valeur.

Fréquences `c_perconst` : code 1 = 11 223 ; 2 = 17 679 ; 3 = 56 949 ; 5 = 10 204 ; 6 = 6 133 ; 7 = 4 468 ; 8 = 2 185 ; 9 = 2 260 ; 10 = 4 657 ; 11 = 2 222 ; 12 = 2 432 ; 99 = 7 786 ; nul = 8. Somme : 128 206.

## Décision et étapes suivantes

**Étudier d'abord la période de construction** : elle est nettement mieux renseignée que l'année exacte. Puis la **hauteur médiane en mètres**, avec contrôle des valeurs nulles, nulles à zéro et aberrantes. Aucune activation de couche à ce stade.

1. Vérifier une version/export officiel Apur daté, ses métadonnées, sa licence ODbL et ses conditions d'utilisation ; consigner URL, date et SHA-256.
2. Inspecter un échantillon spatial limité pour valider géométries, CRS, complétude par arrondissement, incohérences de hauteur et période, et dates de modification.
3. Mesurer soigneusement les relations entre emprises Apur et volumes Paris Data, potentiellement plusieurs-à-plusieurs ; **pas de jointure automatique à un logement vacant**.
4. Déterminer attribution, mode de diffusion, simplification, performances mobile et stratégie de requête/pagination avant prototype public.
5. Séparer clairement trois mesures : **étages Paris Data**, **mètres/période Apur**, **vacance territoriale Insee**. Tester sur Chromium puis déployer une PR spécifique si les validations aboutissent.

## Reproduction

`python3 scripts/audit_apur_emprises.py` : aperçu, sans réseau.

`python3 scripts/audit_apur_emprises.py --live` : **11 demandes HTTP en lecture seule** (schéma et statistiques agrégées) ; aucune récupération ni stockage de polygones.

`python3 -m unittest discover -s tests -p 'test_audit_apur_emprises.py'` : tests synthétiques sans réseau.
