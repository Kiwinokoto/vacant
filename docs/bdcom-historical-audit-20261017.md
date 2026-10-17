# VACANT — audit temporel BDCOM 2017 / 2020 / 2023 (17 octobre 2026)

## Périmètre et résultat

**Statistiques agrégées de locaux en rez-de-chaussée dans les services cartographiques Apur**, obtenues exclusivement avec des requêtes `groupByFieldsForStatistics`, `COUNT(OBJECTID)` et `returnGeometry=false`. Aucun enregistrement individuel, nom, enseigne, adresse ou coordonnée importé dans GitHub. Données ODbL, attribuer **© Apur — BDCOM 2017/2020/2023**. Les trois observations ne sont ni des taux de parc résidentiel, ni des nombres de places d'hébergement.

| Édition | Vacants hors travaux | En travaux | Regroupés (comptage API) | Note Apur |
| --- | ---: | ---: | ---: | --- |
| 2017 | 6 954 | 899 | **7 853** | 7 850 (chiffre arrondi rétrospective 2023) |
| 2020 | 7 247 | 1 517 | **8 764** | **8 760** (premiers résultats 2021) ; **8 560** (rétrospective 2023) |
| 2023 | 7 495 | 1 565 | **9 060** | **9 059** (texte de 2023) |

**Différences préservées sans aucune correction arbitraire.** Il n'y a **pas de série harmonisée confirmée** de taux : les périmètres et le dénominateur de locaux totaux par année, les corrections éventuelles des bases et les traitements méthodologiques de l'Apur doivent encore être vérifiés. Ne pas publier de variations annuelles ou taux de croissance causaux, même si les effectifs d'API apparaissent ordonnés. Un local présent dans deux éditions ne peut pas être présumé suivi individuellement.

## Sources API et méthode reproductible

- **2017** : `https://carto2.apur.org/apur/rest/services/BDCOM/bdcom20032020/MapServer/6/query` ; colonnes `donnees_pour_dataviz_evolution_vacants_csv_annee=2017` et `donnees_pour_dataviz_evolution_vacants_csv_codact`. Groupement année + code activité : `AA101=6954`, `AA102=899`.
- **2020** : `https://carto2.apur.org/apur/rest/services/BDCOM/bdcom2020/MapServer/6/query` ; colonne `C20_CODACT` : `AA101=7244`, `aa101=3` (casse inattendue), `AA102=1517` ; donc **7 247** hors travaux. Le total direct de la couche est **8 764**.
- **2023** : `https://carto2.apur.org/apur/rest/services/BDCOM/bdcom2023/MapServer/1/query` ; `codact=AA101` **7495**, `codact=AA102` **1565** ; cette couche comporte **83 154** locaux, dont **9 060** `type=V` (incluant travaux). Pour 2017/2020, les 83 154 locaux 2023 **ne doivent pas** servir de dénominateur.
- Chaque requête de regroupement a utilisé `where=1=1`, `f=json`, `returnGeometry=false`, `groupByFieldsForStatistics=<colonnes>` et `outStatistics=[{"statisticType":"count","onStatisticField":"OBJECTID","outStatisticFieldName":"n"}]`. Le résultat a été repris **seulement sous forme de trois lignes de totaux** dans `site/data/bdcom-paris-history-2017-2023.json`. Date de consultation 17/10/2026. Les données 2023 au niveau arrondissement restent dans le dérivé indépendant de PR #35.

## Divergences des publications

[Premiers résultats Apur 2020, 8 février 2021, pp. 1 et 5](https://www.apur.org/sites/default/files/bdcom_paris_premiers_resultats.pdf) : première campagne interrompue au confinement puis enquête **1–29 octobre 2020** ; la note est provisoire et donne **8 760 vacants**, dont **1 520 travaux** ; en 2017 **7 850 vacants**, environ **900 travaux**.

[Note Apur n°236, septembre 2023, p. 7](https://www.apur.org/sites/default/files/8p236_bdcom_2023.pdf) : graphique rétrospectif à **7 850 (2017)**, **8 560 (2020)**, **9 060 (2023)** ; « travaux » 900, 1 310, 1 560. Le **texte de la même note, p. 2** mentionne **9 059 vacants** pour 2023. Il n'est pas établi pourquoi les totaux de 2020 diffèrent de **200 locaux** entre les deux publications. Possibles états/nomenclatures/traitements différents **non prouvés** : ne pas choisir une explication arbitraire.

## Contrats et suite

Validation JS `site/bdcom-history-contract.mjs` : exactement les trois éditions, provenance institutionnelle, nombres entiers et concordance, signalement explicite des divergences éditoriales ; refus de champs supplémentaires (notamment adresse) ; **aucune conversion en taux historiques**. `tests/bdcom-history.test.mjs` vérifie le contrat et le lien à la page accessible. Les barres constituent une comparaison **des comptages archivés**, pas une trajectoire inférée de la disponibilité de logements.

À confirmer auprès de l'Apur : cause des divergences 2020/2023, éventuelle révision 2017, liste complète de changements de codes et de périmètre, fichiers définitifs et droits de partage des agrégats. En particulier, rechercher les dénominateurs BDCOM 2017 et 2020 provenant d'éditions correspondantes avant publication de taux ; **ne pas** réutiliser les 83 154 locaux de 2023 pour un taux de 2017/2020. Le rail V conserve le logement résidentiel comme sujet prioritaire et la conversion commerciale comme potentiel séparé.

## Validation du livrable de PR #36

Code `6868825d5fb5e03a82971a072cf4bdb98e331004` : **109/109 tests JS, 99/99 Python**, syntaxe JS et `git diff --check` réussis. Recette de la page `site/potentiel.html` en **Chromium desktop 1440×900 et mobile simulé 390×844** : 3 barres, 3 lignes et 20 arrondissements (bloc 2023) ; années 2017, 2020 et 2023 affichées sans espaces de groupement ; aucun débordement ; aucune erreur JavaScript. Ces vérifications portent sur la PR et non la production.
