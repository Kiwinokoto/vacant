# VACANT — passation immédiate (17 octobre 2026)

## Contrôle final de cette reprise — 17/10/2026

- **Code testé** : `c128bfcf6b83dd2c961c05bfc78055f60ae37c65` (page 2026 + note d'audit), **111/111 JS**, **99/99 Python**, `git diff --check`, clone temporaire propre. **Chromium réel** desktop 1440×900 / mobile simulé 390×844 : section 2026 complète (83 115 / 9 725 / 1 402 / 8 323, et révision 2023 83 284 / 9 104), anciens 3 millésimes et 20 arrondissements visibles, aucun débordement ni erreur JavaScript.
- **Audit GitHub lecture seule** : PR #28–#37 ouvertes, en brouillon et déclarées fusionnables au contrôle ; **aucun check-run GitHub sur chacun des HEAD** et aucun statut combiné de CI sur les HEAD contrôlés. Ne pas confondre fusionnabilité avec validation. Aucun workflow Actions relancé.
- **Apur** : brouillon Gmail vers `data@apur.org` créé (sujet « BDCOM Paris 2017–2026 : clarification des dénombrements et des locaux en travaux »), **non envoyé**. Écart 2020 texte 8 541/graphique 8 560, édition 2026 révisant 2023 9 104 vs édition initiale 9 059/ API 9 060. Attendre réponse / tableau de passage pour toute harmonisation.
- **Livraison** : pas de fusion, changement de main, ni de production. Vérifier à nouveau lock Git/AgentCTL et HEAD avant prochaine modification.


## État de GitHub
- Dépôt : [Kiwinokoto/vacant](https://github.com/Kiwinokoto/vacant) ; **main** : `22f0ad1a07f0c8ea5bc6931c6369df410fac65bc`, production historique `8711f307`. Relire les HEAD actuels avant intervention.
- **Chaîne de PR brouillons sans fusion** : #29 (Insee / IRIS) → #30 (comparaison des arrondissements) → #31 (LOVAC ouvert) → #32 (carte LOVAC) → #33 (part de longue durée) → #34 (potentiel de réemploi) → #35 (BDCOM 2023) → #36 (BDCOM 2017–2023) → **#37** (dénominateurs). **#28** IGN historique indépendante. Ne pas pousser sur main. Tous les HEAD observés déclarés mergeable, mais **aucun statut CI et aucun check-run** ne sont publiés sur les HEAD échantillonnés : cela n'est pas une recette.
- Précédente validation technique du code #37 : **110 JS, 99 Python, Chromium desktop et mobile simulé**, `f28ca917`. La modification ultérieure de la page 2026 doit être re-testée et son commit noté ci-dessous.

## Résultats scientifiques (rail V prioritaire)
- Logements : **Insee RP2023** et **LOVAC privé millésime 2026, observation 01/01/2025** ne sont ni sommables ni des indications d'habitabilité. Part de vacance longue parmi les *seuls vacants privés* à Paris = 26 264 / 105 785 = 24,8 %. Ratio BDCOM, taux Insee et LOVAC restent distincts.
- Commerces locaux en RDC : BDCOM 2017/2020/2023 offre **6954+899 / 7247+1517 / 7495+1565** (vacants hors travaux + travaux), provenant de **versions de données différentes**. Parcs par édition **83 720 / 83 399 / 83 154** ; **aucun taux historique harmonisé certifié**.
- Divergences BDCOM non résolues : 2020 initial 8 760, API 8 764, rétrospective graphique 2023 8 560 mais texte 2023 **8 541**. Le nombre de travaux 2020 dans l'API est 1 517 contre 1 310 dans le graphique rétrospectif 2023. Publication 2017 originale 7 804 vacants, archive rétrospective 7 853 vacants et travaux.
- **Nouvelle note Apur n°296 (octobre 2026)** : 83 115 locaux en avril 2026, 9 725 vacants dont 1 402 en travaux, donc 8 323 hors travaux ; taux officiels 11,7 % travaux inclus et 10,0 % hors travaux. **Référence 2023 révisée dans cette édition : 83 284 locaux / 9 104 vacants**, vs note 2023 : 83 154 / 9 059 et API : 9 060. Afficher 2026 séparément, sans rejoindre la série JSON 2017–2023.
- Bureaux : ≈1,5 million m² d'offre immobilière Paris intra-muros juin 2026 (Colliers / C&W), **pas** une mesure d'habitabilité ni une estimation de places.
- **Distinguer destination, occupation, salubrité, travaux, conversion et droit d'usage.** Aucun bureau ni commerce vide n'est présumé prêt à accueillir. Pas de données à l'adresse/propriétaire ; agrégats seulement.

## Sources / tâches
- [Audit BDCOM](bdcom-historical-audit-20261017.md), [sources](sources.md), [méthode potentiel](potentialite-locaux-20261017.md), [passation LOVAC](PASSATION-LOVAC-2026-10-17.md), [roadmap](../ROADMAP.md).
- **Contact Apur** : [data@apur.org](https://www.apur.org/fr/open-data-cartes/open-data/base-donnees-commerces-parisiens) ; brouillon Gmail préparé **mais non envoyé**, pour demander correspondance 2017–2026, révision des travaux, double version 2023 et mise en ligne BDCOM 2026. Ne prétendre ni envoi ni réponse.
- **Prochaine étape** : revue/fusion éventuelle des PR dans l'ordre seulement après contrôles et consentement à la promotion ; attendre les métadonnées Apur avant taux historiques. Rail B IGN #28 parallèle.

## Concurrence / livraison
- AgentCTL : vérifier lock avant écritures, libérer en fin de passe ; tests locaux avant PR. Aucune fusion/main/déploiement prévu. La passation est dans Git et non dans le chat.
