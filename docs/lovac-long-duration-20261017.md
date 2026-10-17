# VACANT — Où la vacance longue est-elle la plus importante ? (LOVAC 2026)

## Périmètre
Agrégats publics DGALN / Cerema (Licence Ouverte 2.0) à la maille des 20 arrondissements parisiens (codes communes 75101–75120). Source figée et SHA vérifiés dans [l'audit LOVAC](lovac-open-audit-20261017.md). **Millésime de production : 2026 ; date effective d'observation des deux variables : 1er janvier 2025** (dictionnaire de la publication du 25 juin 2026).

## Deux questions différentes

1. **Combien ?** Nombre absolu de logements du parc privé fiscal vacants depuis plus de deux ans. Les grandes circonscriptions peuvent arriver en tête simplement parce qu'elles comportent davantage de logements.
2. **Quelle part parmi les vacants ?** `100 × vacants privés de plus de deux ans / ensemble des vacants privés fiscalement recensés` dans **le même arrondissement et à la même date**. C'est une proportion *conditionnelle au fait d'être recensé vacant*, **pas** le taux de vacance du parc résidentiel, ni la part des logements du parc privé. Le dénominateur du parc privé 2026 à la date 01/01/2025 n'est pas présent dans la livraison ouverte.

**Paris entier :** 26 264 de longue durée / 105 785 vacants privés = **24,8 %**, calculé depuis les totaux et non depuis la moyenne non pondérée des arrondissements.

### Lecture du millésime 2026

| Lecture | Territoire | Longue durée | Tous vacants privés | Part parmi vacants |
| --- | --- | ---: | ---: | ---: |
| Part maximale | 8e | 1 488 | 3 614 | 41,2 % |
| Deuxième part | 1er | 562 | 1 583 | 35,5 % |
| Effectif maximal | 18e | 2 449 | 10 118 | 24,2 % |
| Deuxième effectif | 16e | 2 247 | 8 418 | 26,7 % |
| Paris | Total | 26 264 | 105 785 | 24,8 % |

L'ordre des territoires change selon que l'on classe les effectifs ou les parts. Des ratios importants n'établissent ni causes économiques, ni disponibilité réelle, ni état d'habitabilité des logements, ni densité d'immeubles vacants.

## Ruptures et limite temporelle

Le ratio est **interdit pour le millésime 2023**, où la variable longue durée est observée au 01/01/2022 et la variable « tous vacants » au 01/01/2023. Les millésimes 2020–2022 et 2024–2026 disposent d'une date interne commune pour les deux indicateurs, mais les ruptures GMBI/collecte (2024, puis 2025) interdisent d'interpréter un saut interannuel comme une occupation/libération réelle. Les cartographies sont des **photographies statistiques séparées**.

LOVAC fiscal n'est pas le recensement Insee ; aucun taux IRIS ou bâtiment ne reçoit cette valeur. Les contours IGN 2025 servent exclusivement d'appui visuel aux agrégats communaux, sans géométrie historique des logements.

## Implémentation et contrôle

- `site/lovac-long-analysis.mjs` : mêmes dates obligatoires pour le ratio, Paris pondéré, classement déterministe, seuils de légende fixes.
- Carte LOVAC : bascule part parmi les vacants / effectifs de longue durée / tous vacants et millésime. Ratio 2023 explicitement indisponible.
- `tests/lovac-long-analysis.test.mjs` : chiffres 2026, top par effectif/part, année incompatible, pondération et données corrompues.
- Source : https://www.data.gouv.fr/datasets/61816c6e23197bb34835228e ; documentation : https://doc-datafoncier.cerema.fr/doc/fiche_descriptive/lovac .

## Recette finale du code (17/10/2026)
Commit testé : `717f5bdc55f5dc7f72b02fb65cf95de28fa31a0d` sur la branche de PR #33 ; **98/98 tests JavaScript et 99/99 tests Python** (venv du VPS). Contrôle Chromium headless sur serveur statique temporaire avec le **vrai GeoJSON des arrondissements** servi par VACANT : 20 polygones, 20 rangs, 20 lignes, 5 classes de légende, 8e premier sur le ratio 2026, refus du ratio 2023, comptages 2023 disponibles, retour à 2026 ; largeur desktop 1440 et mobile émulée 390, **zéro débordement** et zéro erreur JavaScript applicative. Contours IGN 2025 réutilisés seulement à l'échelle des vingt arrondissements. Pas de publication.
