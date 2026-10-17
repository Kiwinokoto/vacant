# VACANT — comparer la vacance par arrondissement entre deux recensements

**17 octobre 2026 · Rail V-03, branche de développement empilée sur PR #29.** Cette fonctionnalité est fondée sur le dérivé Insee/IGN des **20 arrondissements déjà audité et publié** par VACANT, et non sur une projection des taux actuels au bâtiment.

## Périmètre et géographie

- **Millésimes RP** : **2006, 2011, 2016, 2023**, uniquement. Ce sont les quatre points du `site/timeline.mjs`, indépendants des jalons **2007, 2012, 2017** de la page historique Paris entier `site/evolution.html`. Il ne faut pas échanger ces millésimes.
- **Données** : fichier `site/data/arrond-history.geojson`, disponible uniquement dans la release préparée : **20 features**, chacune avec quatre groupes `series["année"]` comportant `vacant_count`, `housing_count` et `vacancy_percent`. Pipeline producteur documenté dans `scripts/build_arrondissement_history.py`. Source statistique : Insee RP de l'année correspondante, agrégation des IRIS d'époque **à l'arrondissement**, avant tout affichage. Les données d'origine ont été archivées avec leurs SHA-256 et contrôlées contre les totaux Insee.
- **Géométrie d'affichage** : vingt contours d'arrondissement issus du **fond IGN 2025**. Ils ne sont pas les polygones historiques d'IRIS et ne doivent pas être interprétés comme des affectations de la vacance à un bâtiment ou logement précis.
- **Droits** : chiffres agrégés Insee et contours IGN sous **Licence Ouverte 2.0** (voir `docs/sources.md`).

## Deux mesures rigoureusement distinctes

Pour un arrondissement donné, comparaison du numérateur et du dénominateur **non arrondis** issus des recensements validés :

1. **Nombre de logements vacants** : `vacants_fin - vacants_début`, en logements estimés. Le signe indique une différence de **stocks statistiques**, jamais combien de logements précisément ont été évacués ou remis en occupation.
2. **Taux de vacance, en points de pourcentage** : `100 × (vacants_fin / logements_fin - vacants_début / logements_début)`. Ce sont des **points**, pas un pourcentage de croissance du nombre de vacants.

Les classes de couleur divergeantes sont expliquées par une légende spécifique, avec intervalles fixes. La carte ne mélange jamais la coloration du bâti Paris Data avec les classes statistiques de vacance.

**Paris entier** : les totaux d'arrondissement sont vérifiés à la précision de **1,1 logement**, cohérente avec les chiffres fractionnaires et arrondis publiés. Pour le libellé de variation **Paris entier**, on affiche la différence des **totaux officiels Paris** de `TIMELINE`, ce qui évite les écarts éventuels de ±1 issus des sommes IRIS/arrondissement. Le taux Paris repose sur les deux **dénominateurs totaux** Insee, jamais la moyenne simple des vingt taux.

## Interface et garde-fous

Après activation de la couche « Évolution de la vacance · arrondissements », un panneau permet de sélectionner **une année de départ**, **une année d'arrivée**, puis **variation en points** ou **en logements**. L'année d'arrivée doit être strictement plus tardive ; sinon la comparaison est désactivée avec un message explicite, et la carte simple est restaurée. Les cinq classes de la légende et un **classement des vingt arrondissements** sont recalculés sans réinterroger le serveur.

Les popups affichent les deux effectifs vacants/total, les deux taux, la différence en points, la différence en logements, les géographies des statistiques et celle des contours. Tout contenu est construit en nœuds DOM via **`textContent`**, jamais en HTML non contrôlé.

La comparaison est automatiquement masquée lorsqu'on quitte la couche arrondissement au profit des volumes contemporains ou des IRIS 2023. Elle ne modifie pas les statistiques nationales Paris de `site/evolution.html`.

## État de la recette et validation

- [`site/arrondissement-compare.mjs`](../site/arrondissement-compare.mjs) : fonctions pures `compareArrondissement`, `compareColor`, `summarizeArrondissementChanges`, `buildComparisonPopup`.
- [`tests/arrondissement-compare.test.mjs`](../tests/arrondissement-compare.test.mjs) : chiffres, années interdites, écarts en points vs %, schémas/total, couleur, injection DOM.
- Recette Chromium **1440×900 ordinateur** et **390×844 simulé**, avec vrai fichier `arrond-history.geojson` déjà diffusé : carte simple OK ; comparaison 2006→2023 donne **+16 408 logements** et environ **+0,7 point** pour Paris, **13 arrondissements en hausse de taux**, 7 en baisse ; 5 classes, classement 20/20 ; bascule en « logements », puis 2011→2023 ; refus 2023→2023, retour au mode simple et passage à IRIS 2023 ; **zéro erreur JavaScript et zéro débordement**.
- Le chiffre 2011→2023 est basé, pour Paris, sur les chiffres Insee officiels **139 075 − 98 698 = 40 377** (les 20 arrondissements peuvent donner un écart d'une unité après agrégation des chiffres fractionnaires). Les couleurs de chaque arrondissement utilisent quant à elles les **effectifs précis**, sans arrondi préalable.
- Pas de changement de production ni d'écriture de données sur le VPS en dehors des clones temporaires de test. Les sources officielles restent intactes.

## Suite

1. Terminer les derniers contrôles sur le HEAD exact, mettre à jour **`ROADMAP.md`**, la [passation durable](PASSATION-2026-10-17.md) et ouvrir une **PR empilée sur la PR #29**.
2. **V-04** : ne collecter que la source **publique agrégée LOVAC 2020–2026 à la commune** ; définir la métrique, vérifier secret statistique, champs, parc privé et **ruptures 2024/2025** avant toute visualisation.
3. **Rail B** : relire la PR #28 et continuer l'appariement spatial n:m, sans présenter corrections de BD TOPO comme des rénovations ou démolitions attestées.
