# VACANT — évolution du nombre de logements vacants, Paris (1968–2023)

**17 octobre 2026 — première tranche du rail V (« vacance avant tout »).** Source statistique unique des neuf jalons : [Insee, LOG T1 — Paris (75), dossier complet RP2023](https://www.insee.fr/fr/statistiques/2011101?geo=DEP-75). Les recensements anciens sont des dénombrements ; les recensements rénovés sont des estimations sur une autre base méthodologique. Le tableau Insee donne des valeurs sur un périmètre géographique identique (Paris) selon la géographie au 01/01/2026.

## Valeurs officielles transcrites (LOG T1)

| Année | Ensemble des logements | Résidences principales | Secondaires / occasionnels | Logements vacants | Mode de recensement |
| --- | ---: | ---: | ---: | ---: | --- |
| 1968 | 1 221 954 | 1 152 953 | 28 102 | 40 899 | Ancien dénombrement |
| 1975 | 1 238 732 | 1 113 295 | 37 580 | 87 857 | Ancien dénombrement |
| 1982 | 1 279 730 | 1 114 400 | 53 369 | 111 961 | Ancien dénombrement |
| 1990 | 1 304 428 | 1 095 090 | 91 777 | 117 561 | Ancien dénombrement |
| 1999 | 1 323 464 | 1 111 721 | 75 725 | 136 018 | Ancien dénombrement |
| 2007 | 1 336 209 | 1 139 192 | 80 931 | 116 087 | Recensement rénové |
| 2012 | 1 357 081 | 1 159 105 | 97 276 | 100 699 | Recensement rénové |
| 2017 | 1 382 779 | 1 141 623 | 124 073 | 117 082 | Recensement rénové |
| 2023 | 1 402 024 | 1 124 522 | 138 426 | 139 075 | Recensement rénové |

Les catégories sont distinctes ; certains totaux Insee publiés présentent **un écart de 1 logement** dû aux arrondis statistiques. Les taux sont recalculés comme `vacants / total des logements × 100`, arrondis à **0,1 point**. Par exemple : `139075 / 1402024 = 9,9 %` en 2023. La différence entre **2012 et 2023**, dans la méthode RP : **+38 376 logements vacants**, soit **+2,5 points** environ ; elle ne correspond pas à une liste identifiable de logements restés inoccupés.

## Première interface

`site/evolution.html` est une **page de consultation distincte de la carte**. Elle a deux représentations explicites des **neuf observations** (pourcentage et nombre absolu), sans tracé continu ni interpolation annuelle, des libellés de méthode, le tableau complet lisible sans calcul mental, les catégories secondaires séparées et un lien officiel. La navigation sur la carte existante mène à cette page, avec retour vers la carte IRIS et les arrondissements.

La carte 2023 reste **la seule cartographie fine IRIS officiellement validée et affichée**. Le « 9,9 % Paris » est un taux **pondéré par les logements au dénominateur Paris**, non une moyenne arithmétique des couleurs des IRIS. Sur la carte, les IRIS de parc inférieur à 50 logements sont masqués. Impossible de savoir combien de logements d'une adresse précise sont vacants depuis ces statistiques.

La mini-chronologie de la carte conserve ses jalons propres **2006, 2011, 2016, 2023** : issus des sources RP2022 / RP2023 précédemment validées, ils pilotent les agrégats par arrondissement. Les séries **2007, 2012, 2017, 2023** de la nouvelle page viennent du tableau historique RP2023 : **ne pas remplacer silencieusement** le moteur de carte avec une date différente.

## Distribution réelle des taux IRIS 2023 (nouvelle synthèse de carte)

Lecture du dérivé Insee/IGN 2023 **déjà diffusé** (`992` IRIS, géographie 2025), sans aucune adresse ni appartement identifié : après classement sur le rapport **non arrondi** `vacant_count / housing_count`, **77 IRIS** sont sous 5 %, **241** entre 5 et 8 %, **362** entre 8 et 12 %, **237** entre 12 et 20 %, **12** à 20 % ou plus ; **63 IRIS** dont le parc est inférieur à 50 logements sont grisés. Parmi les **929 IRIS à taux affichable**, **852 atteignent au moins 5 %** et **249 au moins 12 %**.

Les 63 IRIS grisés représentent un parc cumulé d'environ **276 logements seulement** : ils ne doivent pas devenir des zones artificiellement « à taux nul ». L'ensemble des 992 IRIS (petits compris) somme au parc Insee de **1 402 024 logements** et aux **139 075 vacants**, soit le taux **pondéré 9,9 %** pour Paris. **Ne pas moyenner simplement les 929 pourcentages d'IRIS** ni confondre nombre d'IRIS et part de la surface de Paris.

L'ancienne carte classait quelques cellules proches des seuils à partir de la **valeur arrondie à une décimale** `vacancy_percent` ; le moteur corrigé utilise `100 × vacant_count / housing_count` pour la couleur tout en gardant la valeur à une décimale dans les infobulles. La nouvelle synthèse affichée dans le panneau de la carte est calculée depuis le même fichier IRIS vérifié, avec assertion indépendante des totaux Paris.

## Limites / suite

- **Écart méthodologique 1999 → 2007** : pas de comparaison causale directe ni de tendance annuelle continue.
- Recensement rénové : dates de référence espacées ; les ruptures liées à la pandémie autour des recensements 2019–2023 exigent des écarts suffisants.
- La vacance résidentielle Insee inclut les situations de rotation/mise en vente, ne mesure pas directement les logements structurellement vacants depuis plus de deux ans ; les résidences secondaires ne sont pas des vacants.
- **LOVAC public** (2020–2026) est un indicateur **fiscal distinct du parc privé**, avec ruptures de série en 2024/2025. Il appartient à une section autonome et ne doit pas être ajouté à ce graphique.
- Prochaine tranche prioritaire du rail V : documenter la distribution réelle des taux IRIS 2023 (nombre de zones, poids par nombre de logements, zone masquée) et ajouter des comparaisons de deux années **par arrondissement** sur les données déjà validées.
- Rail B : [PR #28](https://github.com/Kiwinokoto/vacant/pull/28), audit privé des géométries IGN 2008/2011/2018, avec contrôle de comparabilité avant toute publication. Ne pas assimiler révision géométrique à construction ni IRIS à immeuble.

**Règle stricte** : `site/evolution-data.mjs` ne stocke que des **comptages agrégés publics** ; aucune adresse, identité, logement privé ou liste LOVAC individuels.
