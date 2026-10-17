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

## Audit complémentaire des dénominateurs — 17/10/2026

| Édition | Locaux recensés | Provenance exacte | Réserve |
| --- | ---: | --- | --- |
| 2017 | **83 720** | [Fiche BDCOM 2017 d'origine, version 20/03/2018](https://www.apur.org/open_data/BDCOM_2017_OD.pdf) | Publication contemporaine 2017 : **7 804** locaux vacants ; archive rétrospective : **7 853** vacants/travaux. **Versions non identiques**. |
| 2020 | **83 399** | Somme du champ `localrdc` des 20 arrondissements dans [BDCOM 2020 structure, MapServer/0](https://carto2.apur.org/apur/rest/services/BDCOM/bdcom2020_structure/MapServer/0) | Note de février 2021 arrondit à **83 400**. Le service donne aussi **8 764** `localvacant`. |
| 2023 | **83 154** | [BDCOM 2023, MapServer/1](https://carto2.apur.org/apur/rest/services/BDCOM/bdcom2023/MapServer/1) | Total cohérent avec la note et les agrégats PR #35. |

**Source du conflit 2020, partiellement localisée :** le service 2020 distingue **7 247 vacants hors travaux** et **1 517 en travaux** ; la rétrospective Apur 2023 publie environ **1 310 en travaux** pour 2020, soit **207 de moins** dans la catégorie travaux, et ramène le total regroupé de ~8 760 à **8 560** (différence ~200). Les éventuelles révisions de la catégorie « travaux » ne sont **pas expliquées** : ne pas invoquer une reprise économique sans preuve.

**Contrôle de l'ancienne structure :** l'addition des catégories du service `bdcom2020_structure` produit 84 023 locaux pour les colonnes 2017, alors que la fiche d'origine en annonce 83 720 ; en 2020, cette somme produit 83 390 au lieu du champ officiel `localrdc = 83 399`. Le champ `tous_17/tous_20` ne peut pas non plus être assimilé sans vérification à tout le parc. Les nouvelles tailles de parc figurent **uniquement comme contexte de couverture** dans `site/potentiel.html`. **Aucun taux historique comparatif calculé** : trouver le dénominateur n'établit pas l'identité des protocoles et révisions des numérateurs.

**Contrôles :** le validateur JSON vérifie les 3 dénominateurs, leur provenance, les années, la séparation travaux/vacance et les divergences publiées. Aucune donnée BDCOM individuelle ni coordonnées ne sont distribuées.

## Contrôles définitifs PR #37
**Validation PR #37 (commit testé `f28ca91789c4649115dd1d3d7a802860426c4ad8`) :** 110/110 tests JavaScript, 99/99 Python dans le venv du VPS, `node --check`, `git diff --check`, clone Git propre. Recette Chromium réelle sur serveur temporaire : desktop 1440×900 et mobile simulé 390×844, trois tableaux historiques à cinq colonnes dont parcs 83 720 / 83 399 / 83 154, 3 barres de catégories et vingt arrondissements BDCOM 2023. Aucun débordement, aucune erreur JavaScript. **Aucune promotion ni changement de production.** Les taux historiques restent bloqués jusqu'à validation des éditions/numérateurs par Apur.


## Complément majeur — premiers résultats BDCOM 2026 (Apur, octobre 2026)

[Apur, note n°296, octobre 2026](https://www.apur.org/sites/default/files/2026-10/12p296_Commerces_Paris_tendances_enquete_2026.pdf), **enquête d'avril 2026**, p. 2 et p. 6 :
- 2026 : **83 115 locaux recensés**, **9 725 vacants travaux inclus** (11,7 %), **1 402 en travaux** ; soit **8 323 hors travaux** par différence, taux publié **10,0 %**.
- La même note **révise le 2023 de référence** à **83 284 locaux** et **9 104 vacants**. C'est **+130 locaux recensés** et **+45 vacants** par rapport au texte initial de la note n°236 de septembre 2023 (**83 154 / 9 059**) ; l'API 2023 en recense 9 060, une unité supplémentaire. L'écart de version doit être étudié : **ne pas écraser la source ouverte 2023 avec la statistique rétrospective 2026** sans métadonnées.
- La note 2026 rapporte elle-même **+621 vacants entre ses éditions 2023 (9 104) et 2026 (9 725)**, ce qui diffère du calcul utilisant la base initiale 2023. Ne pas reconstituer une tendance inter-édition en choisissant arbitrairement une des deux sources.
- Autre précision dans le texte de la note n°236 de septembre 2023 (p. 6) : **8 541 vacants en octobre 2020**, utilisés pour déduire **+518** en 2023 (9 059 − 8 541), alors que son graphique p. 7 affiche **8 560**. L'écart graphique/texte doit être demandé à l'Apur plutôt que considéré comme une simple erreur d'arrondi prouvée.

**Situation des données** : la publication 2026 est une **note de premiers résultats**, pas le jeu de données individuel BDCOM 2026 réutilisable avec schéma audité ; l'open data identifié officiellement reste 2017/2020/2023. VACANT l'affiche séparément sur la page `site/potentiel.html`, sans placer 2026 dans le JSON de la série cartographique ou calculer de taux longitudinal harmonisé. Aucune adresse ni localisation de local n'est enregistrée.

**Demande méthodologique envoyée le 17/10/2026 :** courriel Gmail à `data@apur.org` (message `1a149909decf1bfc`) pour demander les conventions de révision 2017/2020/2023/2026, les règles sur les locaux en travaux et la date prévue des données ouvertes 2026. Le courriel précédent, envoyé le 16/10/2026 à la même adresse, portait sur les emprises bâties et a déclenché une vérification humaine Mailinblack, confirmée par l'utilisateur. **Aucune réponse scientifique de l'Apur reçue lors de la dernière vérification.**
