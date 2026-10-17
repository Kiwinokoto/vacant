# VACANT — revue et ordre de fusion des travaux Apur (proposition, non exécutée)

**16 octobre 2026. Les PR sont toutes des brouillons. Aucune fusion ni publication autorisée par ce seul document.**

## Dépendances réelles

| Étape de revue | PR | Branche | Base actuelle | Condition |
|---|---|---|---|---|
| 1 | [#23](https://github.com/Kiwinokoto/vacant/pull/23) | `dev/apur-consolidated-20261016` | `main` | Revue des 6 sources #17–#22, tests, audit SIG, exclusions |
| 2 | [#24](https://github.com/Kiwinokoto/vacant/pull/24) | `dev/apur-grid-site-local-20261016` | branche #23 | Revue du chargement privé, 404/503, viewport et interfaces territoriales |
| 3 | [#25](https://github.com/Kiwinokoto/vacant/pull/25) | `dev/apur-release-gate-review-20261016` | branche #24 | Revue du filtre release Git-only, sécurité des GeoJSON, gzip et contrats ODbL |

**Ne pas fusionner #24 ou #25 avant leurs bases.** Lors d'une future promotion avec approbation explicite, préserver les commits de l'assemblage à sept parents de #23, puis réévaluer les bases des PR empilées (ne jamais les laisser viser une branche temporaire supprimée). Éviter un squash/rebase implicite qui rendrait difficile la traçabilité des six PR historiques. Ces anciennes PR #17–#22 restent ouvertes tant que le remplacement par la consolidation n'est pas accepté.

Tous les contrôles ci-dessous sont des **critères**, pas une autorisation de déploiement.

## Critères de fusion Git

- [ ] La tête `main` n'a pas bougé, ou les modifications intermédiaires sont examinées/rebasées proprement.
- [ ] Vérifier GitHub, diff complet, `git diff --check`, arborescence de commits et état mergeable pour **chaque PR**.
- [ ] Rejouer intégralement tests Python + JS sur le **commit GitHub exact** prévu et effectuer une recette navigateur depuis ce commit.
- [ ] Vérifier que le seul conflit historique (`docs/handoff.md`) est remplacé par une passation canonique sans perdre d'information utile.
- [ ] Aucun fichier GeoJSON Apur individuel, manifeste privé ou ressource `_local/` n'est suivi par Git.
- [ ] Le mode Apur demeure invisible hors `localhost` avec paramètre `?apur_lab=1`, sans repli API ni jointure vacance.
- [ ] Préparer une release exclusivement par `scripts/stage_reviewed_release.py`, **en dehors du dossier servi**, avec seulement IRIS et arrondissements explicitement vérifiés ; pas de commande `cp -r site/*`.

## Critères pour publication d'une couche Apur (distincts de la fusion du code de laboratoire)

- [ ] Contrat d'attribution Apur : titre du jeu `EMPRISE_BATIE_PARIS`, source officielle, licence ODbL 1.0, date d'extraction, version scientifiquement attestée **ou avertissement visible d'incertitude**.
- [ ] Définir et mettre à disposition sous ODbL un dérivé téléchargeable lisible par machine **ou** l'ensemble des transformations/reconstitutions exigées par la section 4.6 ; ne pas considérer la simple légende comme suffisante.
- [ ] Documenter CRS EPSG:2154 → EPSG:4326, choix de grille 500m, polygones répétés, 104 exclusions topologiques, 13 identifiants absents, politique de hauteur `h_med` et de période `c_perconst` ; fichiers ZIP source et manifeste SHA figés.
- [ ] Contrôler les droits sur toute donnée complémentaire avant fusion de bases, **ne pas attribuer un taux de vacance IRIS à une emprise**.
- [ ] Tester Nginx réel **sur serveur de recette isolé** : gzip, Vary, MIME, 403 et 404, ainsi que le contrôle SHA côté navigateur après décompression.
- [ ] Recette sur **téléphone physique et vraie connexion mobile**, budgets de latence/mémoire, zoom panoramique, textes, comparaison avec la carte territoriale ; charge multiutilisateur ensuite.
- [ ] Le cas échéant, préparer des cellules compressées, un cache et une stratégie de mise à jour/retrait, avec un contrôle de provenance et un processus de rollback.
- [ ] Obtenir une **décision explicite de publication**, puis seulement acquérir les leases AgentCTL de déploiement et modifier la release publique.

## État au soir du 16 octobre 2026

Le code de laboratoire est validé localement, la grille complète reste privée sur le VPS, la compression a été mesurée, la sécurité de staging a été améliorée et **une nouvelle recette Nginx en boucle locale avec données synthétiques a réussi**. Ce n'est pas une recette réseau 4G sur appareil réel. En conséquence : **techniquement prometteur, non encore prêt pour une publication cartographique Apur**. `vacant.kiwinokoto.fr` doit rester inchangé.
