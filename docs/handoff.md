# Passation VACANT — 2026-10-16

## État Git de référence
**PR #1 fusionnée** en `main` par squash le 16/10/2026 : **`df947684403fc34cfe6ab8ce450644b0a3e6ab6b`**. Pas de déploiement ni de workflow CI. La branche `dev/source-audit-and-map` demeure pour l'historique, sans écriture prévue dessus.

**Travail actuel :** `dev/iris-provenance-validation`, créée depuis le commit main ci-dessus ; premier commit `814a237229a3789f10aeb5116dafefb7f3ff207b`, [PR brouillon #2](https://github.com/Kiwinokoto/vacant/pull/2) ouverte, non fusionnée. Validation stricte d'imports IRIS préparés. 15/15 contrôles JS réussis sur les blobs GitHub (9 existants, 5 contrats IRIS, 1 test CLI simulé) ; suite Node native non exécutée, données sources absentes. Vérifier la nouvelle tête GitHub et la PR à chaque reprise. Pas de modifications du VPS.

## Décisions
- Paris intra-muros, public, statique, pas de données à risque individuelles.
- Paris Data Volumes bâtis v0.1 : **étages seulement**, âge/hauteur métrique/vacance **inconnus**.
- Apur Emprise bâtie Paris prioritaire pour recherche âge+hauteur ; Insee 2006–2023 IRIS prioritaire pour vacance (jalons 2006/2011/2016/2023, comparaison ≥5 ans et 2016–2023=7 ans) ; LOVAC agrégé 2020–2026 uniquement Paris commune.
- Historique avant 1900 : cartes originales sourcées et reconstruction explicitement qualifiée, jamais fiction annualisée.
- ODbL Apur/Paris Data et Licence Ouverte pour les autres sources selon fiche ; pas de réutilisation mixte sans audit de compatibilité.

## Réalisé
Audit documentaire des organismes officiels, architecture, interface statique 2D (polygones de volumes Paris Data chargés manuellement ; étages, pas mètres, aucune vacance par immeuble), README et tests. **9 vérifications contractuelles sur le module source récupéré de GitHub réussies dans un environnement JS**, mais la suite complète `node --test` n'a pas été exécutée. PR #1 de référence, à contrôler sur GitHub au moment de la reprise ; tests du code en runtime V8 exécutés sur les **9 cas présents dans les fichiers de tests du dépôt** (9/9 OK), mais ni la suite Node native ni les requêtes HTTP navigateur n'ont été validées.

## Dernière extension (chronologie)
Démarrage statistique **2006** acté dans [chronologie.md](chronologie.md). Chronologie de chiffres **Paris entier** vérifiés dans deux tableaux officiels Insee ajoutée au panneau du site ; aucune mise en couleur des polygones ni cartographie IRIS historique. Nouveaux modules `site/timeline.mjs`, `tests/timeline.test.mjs`, plus l'interface de sélection 2006/2011/2016/2023. Commit fonctionnel `548449801ba3ab015b5415c436c479b67d7087eb`. Chiffres historiques 2006/2011/2016 transcrits du RP2022 ; 2023 du RP2023 harmonisé. Écarts d'une unité autorisés dans les sommes arrondies. Important : ne pas comparer les millésimes annuels voisins, et ne pas superposer 2023 sur le bâti actuel comme observation historique.

## Travaux préparatoires IRIS sur branche dédiée
Contrat `site/iris-contract.mjs` ; commande `scripts/validate-iris.mjs` ; 5 nouveaux tests `tests/iris-contract.test.mjs` réussis dans le runtime V8 sur les blobs créés via GitHub. GeoJSON et manifeste explicites obligatoires ; sortie refusée sans contrôles de cardinalité. Le CSV 2023 harmonisé et les contours géographie 2025 n'ont **pas** été téléchargés ; aucun jeu IRIS n'est construit ni visible sur la carte.

## Préparation de la collecte — 16/10/2026
Dossier cible approuvé en architecture : **`/srv/vacant/data` sur le VPS personnel**, hors racine web. `scripts/collect_insee.py` prépare cinq téléchargements Insee officiels avec manifestes SHA-256 et verrou `flock` local. [Guide et URLs](acquisition.md). **Aucun téléchargement réel n'a été effectué : appareils RDC personnels hors ligne (deux vérifications), accès direct Insee indisponible dans le conteneur. Aucun dossier VPS créé.** Six tests Python du collecteur réussis sur une copie locale de développement ; à rejouer depuis GitHub avant exploitation. Les contours IGN édition 2025 restent à sélectionner (ne pas substituer l'édition 2024).

## Incertitudes / blocages
- Aucun téléchargement réel des fichiers Apur, Insee/IRIS, IGN ni test réseau direct de l'API dans cet environnement. Couverture/CRS/attributs et qualité locale non certifiés.
- CORS, pagination triée par identifiant de volume et restrictions de l'API doivent être vérifiés dans un navigateur réel. Le schéma `geom`, `geom_x_y`, `h_et_max` et `n_sq_vb` a été revérifié sur la fiche officielle Paris Data du 08/10/2026.
- 12 contrôles supplémentaires de chronologie/provenance vérifiés dans le runtime JS sur les blobs GitHub (tous OK). `npm test` complet non exécuté : `git clone` public depuis le conteneur de test a échoué sur la résolution DNS de github.com. Aucun RDC ni VPS utilisé pour contourner ; réexécuter localement.
- Aucun contrôle des éventuelles branches/clones non poussés ni lease AgentCTL externe disponible depuis les seules métadonnées GitHub. Les PR GitHub et branches ont été vérifiées avant création de la branche, sans conflit constaté.
- Droits et formalités de diffusion des images historiques à traiter source par source.

## Prochaines étapes
1. Vérifier branche/HEAD/PR, travaux concurrents et leases avant écriture.
2. Ouvrir l'application avec accès réseau, vérifier sur vraie zone et enregistrer un test API + capture d'une réponse schéma ; relever volumes chargés/erreurs.
3. Télécharger un extrait Apur officiel, contrôler datation/hauteur, licences et jointure exacte ; ajouter tests de comparaison spatiale.
4. Télécharger à partir de 2006 (XLS géographie 2008) et jalons 2011/2016 puis RP2023 (schéma harmonisé + géographie 2025), contrôler variables, dénominateurs, changement de limites et petits effectifs, **puis seulement** afficher la vacance en polygones IRIS sans extrapolation spatiale.
5. Valider architecture 3D à partir de hauteurs **en mètres**, puis revue et éventuelle promotion/déploiement sur demande explicite.

Avant toute promotion supplémentaire vers main, récupérer le HEAD exact, vérifier PR / checks et assurer l'absence de déploiement implicite. Le validateur IRIS n'a pas d'interface utilisateur ni de données réelles ; le présenter comme préparation, non comme une carte IRIS fonctionnelle. Après fusion, mettre à jour l'état ici si une nouvelle passe l'exige.

Ressources : repo GitHub vacant uniquement ; **aucun VPS, aucune base ni déploiement occupé** lors de cette passe. Aucun lock créé sur une ressource distante.
