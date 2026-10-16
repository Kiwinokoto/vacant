## Laboratoire Apur datation par périodes — 16/10/2026, 19 h 20 (Paris)

- Source de vérité au départ : `main=72a9d06377541b7b266e0d8153e89a7ae19afb95`, PR #17 (audit géométrique) ouverte en brouillon. Aucun concurrent ni lease AgentCTL VACANT au contrôle ; session dédiée `chatgpt-apur-period-prototype-20261016` / `repo:Kiwinokoto/vacant` pendant les écritures, à libérer en fin de passe.
- Nouvelle branche isolée `dev/apur-period-experiment-20261016` : prototype **uniquement** sous `experiments/apur-periods/`, contrat JS et tests. **Aucun changement dans `site/`**, aucune géométrie Apur archivée ou déployée, aucun changement de production.
- Fiche Apur 2019 : ODbL, classement officiel en 11 périodes + 99 ; `c_perconst=11` = **2000–2007**, malgré une légende du renderer ArcGIS qui dit « 2000 et plus ». Les valeurs codées du schéma ArcGIS confirment 2000–2007. La version géographique exacte du service reste indéterminée ; ni la date du document (2019), ni la page de présentation (2024), ni le traitement miroir (2026) ne suffisent à la dater.
- Carte expérimentale par petite enveloppe, requête live **volontaire** : précompte, plafond 200 emprises, aucun retour partiel affiché, champs autorisés uniquement, données non datées grisées. **Aucun** indicateur de vacance rapporté au bâti.
- Validation : Node **35/35**, Python **48/48**, Chromium desktop **84** emprises / mobile **37**, 12 classes dans la légende, CORS et affichage OK, aucun débordement ni erreur JS. Défauts initialement repérés (hauteur desktop excessive, cadrage initial >200 objets) corrigés.
- Rapport détaillé : [apur-period-prototype-20261016.md](apur-period-prototype-20261016.md). Priorités : export Apur daté + SHA-256, obligations de rediffusion ODbL, QA complète des polygones et performances, puis PR distincte pour la véritable intégration UI. **Ne pas déployer ce prototype ni réinterpréter une période comme une observation de bâti ancien.**
- Production vérifiée inchangée au contrôle pré-écriture : release `1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0`, conteneur VACANT actif, 0 redémarrage. Pas de nouvelle recette de production nécessaire dans cette passe.

# VACANT — passation active (16 octobre 2026)

**Point de reprise prioritaire : [checkpoint Apur du 16/10/2026](checkpoint-apur-20261016.md).** Ce document reflète le dernier état vérifié ; les rubriques ci-dessous constituent l'historique des passes précédentes et peuvent contenir des statuts anciens.

## Validation finale — 16/10/2026

- **PR #13 fusionnée et déployée** : code `1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0`, release de même SHA active sous `/srv/vacant/releases/<SHA>/site`. 25/25 Node, 40/40 Python, Chromium réel local **et public** (desktop/mobile, cartes des quatre millésimes, erreurs HTTP simulées) ; HTTP/HTTPS et deux GeoJSON historiques publics contrôlés, géométries candidates toujours HTTP 404. Ancienne release `2424a45ad590901e3c96c781e10d8b2309c874cb` conservée pour rollback. Pas d'évolution des données publiques.
- **PR #14 recherche Apur fusionnée** : dernier `main` `642538708c802eb551fcfecd48f1492d5fc0602e` avant cette mise à jour de passation. Audit agrégé Apur 128 206 emprises, 128 090 hauteurs médianes positives, 120 412 périodes renseignées, 47 056 années exactes manquantes. 25/25 Node et **48/48 Python**. Voir [audit Apur](apur-bati-audit.md), `scripts/audit_apur_emprises.py` et tests. **Aucune géométrie Apur extraite ni publiée**.
- Déploiement VACANT **volontairement au commit PR #13**, pas au `main` plus récent : la PR #14 ne touche qu'aux scripts d'audit et à la documentation. Ne pas redéployer inutilement.
- **Suite ordonnée** : exporter/sourcer précisément la couche Apur datée et vérifier les conditions ODbL, contrôler un échantillon de géométries/emprises et les trois hauteurs médianes au-delà de 200 m, puis prototype distinct « période de construction » et « hauteur médiane (m) » avec tests et mentions de limites ; ensuite retourner aux originaux IGN 2008/2018 et à la réponse IGN déjà sollicitée. Pas de taux de vacance par emprise/bâtiment.
- Branches locales sur VPS dédiées, non poussées directement ; contenus des commits publiés par connecteur GitHub avec identité de tree vérifiée. Agents/locks et services à revérifier à la prochaine reprise. Après cette passation, libérer toutes les leases `vacant`.

## Mise à jour — déploiement PR #13 et audit Apur (16/10/2026)

- **PR #13 fusionnée** au commit `1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0` ; aucune action CI configurée. Tests 25/25 Node et 40/40 Python, recette Chromium locale puis **production** (quatre années, changement de couches, erreurs HTTP 503 simulées avec retour à la couche précédente, mobile 390 px) : `BROWSER_ALL_PASSED`.
- **Production effective** : release immuable `/srv/vacant/releases/1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0/site`, conteneur VACANT seul recréé via Compose, aucun redémarrage signalé. Certificat Let's Encrypt valide ; HTTPS 200 (accueil, fichiers JS et deux GeoJSON publics), HTTP 301→HTTPS ; fichiers historiques candidats HTTP 404. Données validées inchangées ; ancienne release `2424a45ad590901e3c96c781e10d8b2309c874cb` conservée comme retour arrière.
- **Audit Apur préliminaire** : 128 206 emprises EPSG:2154. `h_med` positive dans 128 090 cas ; `c_perconst` connue dans 120 412 ; `an_const` manquante dans 47 056 cas. Source, chiffres, limites et suites : `docs/apur-bati-audit.md`. Requêtes agrégées seulement, aucune donnée d'objet enregistrée ni publiée. Code : `scripts/audit_apur_emprises.py`, tests synthétiques.
- Branche pour cette étape `dev/apur-heights-dating-audit`, base `main` au commit de production. Vérifier le HEAD, PR, état local et locks avant toute écriture. **Aucune nouvelle couche Apur** en production. Ne jamais attribuer un taux de vacance territorial à une emprise.
- La demande IGN des archives 2008/2013/2018 a bien été **envoyée le 16/10/2026** ; consulter Gmail pour sa réponse, ne pas réexpédier un doublon.

## Passe 16/10/2026 — éditions historiques et correctif ergonomique

- **Contrôles réalisés** : Node 25/25, Python 40/40. Chromium réel sur clone de la branche avec dérivés agrégés publics aux SHA validés (IRIS 2023 `0b79e30a...`, arrondissements `97667772...`) : bascule de couches, quatre années, labels de géographie, retour aux volumes, deux échecs réseau simulés avec restauration de la couche précédente, mobile 390 px sans débordement ; résultat `BROWSER_ALL_PASSED` le 16/10/2026. Aucune archive géographique historique non autorisée employée dans la recette.
- **Publication** : la branche ne déploie pas automatiquement la correction UI. Contrôler revue/PR/CI avant fusion et obtenir l'accord de déploiement avant modification de la release publique.

- GitHub main de départ : b492ede6567d68cc6df1b18db852d68eb4cf09c5 ; aucune PR ouverte ; branche dev/iris-archive-readiness dans clone /srv/vacant/work-geography-readiness. À la reprise vérifier HEAD, travaux locaux/agents, PR, CI et leases AgentCTL.
- Recherche : IGN Contours…IRIS édition 2008 v1.0 ; édition 2018 = IRIS 2017 consolidés + 2018 provisoires ; édition 2019 = IRIS 2018 consolidés + 2019 provisoires. Livraison 2018-06-08 avec dossier FXX-2017 non assimilable automatiquement au fond RP2016 géographie 2018. AUCUNE nouvelle archive 2008/2018 acquise ; détails : docs/iris-archive-readiness.md.
- L'IGN a déjà reçu le courriel le 16/10/2026. Ne pas réexpédier. La provenance juridique/date 2013 du candidat RP2011 reste à confirmer.
- Code modifié : site/index.html, site/app.mjs, site/view-state.mjs, site/iris-contract.mjs, tests/view-state.test.mjs et tests/iris-contract.test.mjs. Titre et sous-titre de carte changent selon la couche réelle. Légende des taux à intervalles disjoints ; retrait du texte erroné sur le sélecteur. Publication d'une géographie IRIS autre que 2023 refusée explicitement jusqu'à levée formelle du blocage ; validation privée permise.
- Aucune nouvelle couche 2011 publiée. Production connue : release 2424a45ad590901e3c96c781e10d8b2309c874cb, HTTP à revalider. Aucun Docker/BDD/service modifié pendant cette passe ; tests à exécuter, PR à soumettre, pas de déploiement sans recette navigateur et validation de la portée.
- Suite : récupérer vrai 2008 et 2018 consolidé, vérifier les droits 2013 auprès IGN, tester UX dans Chromium réel sur candidate avant déploiement.

## IGN — demande envoyée le 16/10/2026

- La demande de géométries historiques **Contours…IRIS® 2008, 2013 et 2018 (Paris, 75)** a été **envoyée depuis le compte Gmail connecté** à `contact.geoservices@ign.fr` le 16 octobre 2026 ; Gmail a confirmé le statut `SENT`. **Ne pas envoyer de doublon.**
- Objet : « Demande d’archives Contours…IRIS® 2008, 2013 et 2018 — Paris (75) ». Le message demande également l'attestation que le jeu Atlasanté nommé **2014** correspond bien à la géographie Insee **2013**, et la licence historique de rediffusion de dérivés GeoJSON. Texte technique de référence : [demande-archives-ign.md](demande-archives-ign.md) (version proche du courrier envoyé).
- **Réponse IGN non encore obtenue** à la date d'envoi. Avant de relancer, rechercher ce fil dans Gmail ; ne pas considérer le silence comme un accord de licence. Le contenu de `site/`, les fichiers géographiques privés, le conteneur et la production n'ont pas changé pendant cette opération.
- Nouvelle piste de recherche indépendante : une documentation tierce cite `CONTOURS-IRIS_2-1__SHP__FRA_2018-06-08` avec un sous-répertoire `...FXX-2017`. La date de livraison **2018** ne prouve pas une géographie de référence **2018** : vérifier la notice, les codes et les géométries avant tout appariement à RP2016. Archive non acquise.
- Pendant l'attente : chercher les **fonds IGN officiels 2008 et 2018**, contrôler édition/CRS/SHA/conditions juridiques ; privilégier les améliorations UI et le contrôle mobile indépendants des anciennes licences. Les couches fines historiques secondaires restent **hors production**.

## Fin de passe — Atlasanté 2014 (16/10/2026)

- PR #10 **fusionnée** en squash sur `main` : `67648885c9996604fd539506c975a14050783c7e`. Source locale `dev/iris2014-atlasante-geometry` sans changement non commité ; arbre GitHub de la PR vérifié identique à Git local. La branche documentaire présente ajoute uniquement cet état final.
- Archive institutionnelle Atlasanté `IGN – Métropole – IRIS 2014` privée : SHA `5cefdde58d228b3f8643d01ef61c80c10bf4ce30a30e78b61e2dc48fdf9acf27`. Ancien candidat dit 2013 : `c6afee56f81b3a9d08316034f0f48259162276a3d7a0d11388c2472f2fd5d3a7`. Les **992 contours Paris** coïncident à mieux que `0,000009 m²` près après reprojection.
- Auditeur `scripts/audit_iris2014_atlasante.py` : lecture uniquement du SQL institutionnel, jamais exécuté ; revalide toutes les archives précédentes et les 992 appariements. Tests **22/22 JavaScript et 40/40 Python**.
- Contrôle final production : conteneur actif, 0 redémarrage, release inchangée `2424a45ad590901e3c96c781e10d8b2309c874cb` ; accueil, IRIS 2023 et arrondissements historiques HTTP 200 ; candidats RP2011/Atlasanté HTTP 404.
- **Blocage externe restant :** attestation de correspondance officielle édition 2013 et conditions IGN/Insee de rediffusion (notice Atlasanté date la *publication de notice* en 2013 mais intitule le jeu **2014**). La [demande IGN](demande-archives-ign.md) est prête, **non envoyée**. Ne pas déployer de polygones 2011 avant confirmation des droits et du millésime.
- Toujours aucune édition originale authentifiée 2008 ou 2018 ; conserver comparaison historique par 20 arrondissements.
- Vérifier à la reprise GitHub HEAD et tous locks AgentCTL avant toute écriture ; ne pas prendre les clones VPS pour source de vérité.

## Mise à jour — Atlasanté 2014 / candidat 2013

- GitHub main vérifié au début : 38a8db3cb25ec677ea1c029aeb8c8addd2dc1387 ; branche dev/iris2014-atlasante-geometry. Revérifier les commits et verrous AgentCTL avant nouvelle écriture.
- Archive institutionnelle Atlasanté « IGN – Métropole – IRIS 2014 » ZIP (16 411 555 octets), PostGIS EPSG:2154 et ISO XML ; SHA-256 5cefdde58d228b3f8643d01ef61c80c10bf4ce30a30e78b61e2dc48fdf9acf27 ; sauvegardée privée et manifestée sous /srv/vacant/data/raw/secondary/iris-2014-atlasante/ et /srv/vacant/data/manifests/.
- 992 géométries Paris, zéro invalide. Recoupement avec le candidat tiers 2013 : IoU minimale/médiane 100 % à dix décimales, différence surfacique maximale 0,000008961 m². Auditeur scripts/audit_iris2014_atlasante.py, tests unitaires ; preuves docs/iris-2014-atlasante.md.
- Métadonnées : jeu intitulé 2014 ; publication de notice 2013-09-16 et révision 2015-04-29. Ces dates ne prouvent pas l'édition géographique 2013. Conditions IGN/Insee spécifiques mentionnées : pas de republication sans confirmation.
- Demande IGN précisée dans docs/demande-archives-ign.md et non envoyée. Les éditions 2008 et 2018 restent à rechercher.
- Production non modifiée : https://vacant.kiwinokoto.fr, historique par 20 arrondissements et IRIS fins uniquement en 2023. Aucune couche 2011 ni donnée individuelle publiée.
- Suite : validation officielle du millésime et des droits ; si obtenue, PR ciblée couche RP2011 avec contrôles SIG/navigateur. Sinon conserver le dérivé privé.

## Fin de passe — contrôle indépendant des contours IRIS
- PR #8 fusionnée dans `main` : `2e4e53372bdfb31501149c00adfaff0b0ce86be8`. La nouvelle branche historique de travail `dev/iris-independent-crosscheck` n'a pas été déployée ; code, tests et documentation uniquement.
- 22/22 tests JavaScript et 33/33 tests Python réussis. Relecture de trois séries de 992 contours, IoU médian candidat2013/OSM2013 = 1,00000, candidat2013/secondaire2016 = 0,93688 et secondaire2016/IGN2025 = 0,98472.
- Archives secondaires à accès privé `/srv/vacant/data/raw/secondary/` et manifestes SHA `/srv/vacant/data/manifests/` : aucun transfert dans `site/data`, aucune publication des couches 2013/2016.
- Demande des archives originales IGN 2008/2013/2018 préparée dans `docs/demande-archives-ign.md`, **non envoyée** : accès Gmail indisponible. Les jeux secondaires demeurent non certifiés.
- Suite : obtenir et auditer les livraisons authentiques IGN ou leur provenance officiellement attestée, vérifier droits et concordances SIG, puis envisager seulement une carte IRIS historique par année.

## Source de vérité / état réel
- Dépôt public : `Kiwinokoto/vacant` ; dernière base `main` confirmée avant cette passe : `53837c7fb0fa35ac6eb3797eb3c190e921c6b604`, PR ouvertes : aucune. Travail courant sur `dev/iris-independent-crosscheck`. Revalider GitHub, HEAD, remotes, état local, CI/protections et leases AgentCTL avant écriture.
- Production inchangée : https://vacant.kiwinokoto.fr, VPS personnel `vmi2505789.contaboserver.net` via RDC LGC, release active au début `2424a45ad590901e3c96c781e10d8b2309c874cb`. HTTPS et conteneur à revérifier en fin/reprise. Aucun déploiement voulu pendant les audits privés.
- Sources et dérivés **privés** dans `/srv/vacant/data/raw`, `/srv/vacant/data/manifests`, `/srv/vacant/data/processed` ; ne pas les pousser vers GitHub ni les exposer au webroot.

## Produit publié et données validées
- Vacance résidentielle Insee aux recensements 2006/2011/2016/2023 : affichage historique par **20 arrondissements** ; les valeurs sont agrégées depuis les IRIS de leurs millésimes, sans les attribuer à d'autres contours.
- Couche précise IRIS : **2023 seulement**, contours IGN géographie 2025, 992 IRIS et 929 taux affichés (petits parcs masqués). Aucune identification de vacance par logement, immeuble ou volume bâti.
- Couche Paris Data volumes actuels : nombres d'étages, pas hauteur métrique, plafond API de 800 volumes avec avertissement, retour de zoom en quittant les statistiques. Tests Chromium validés précédemment.

## Recherche SIG terminée ou en cours
- Références Insee : archives géographies 2008/2013/2018/2025, 992 codes Paris inchangés, contreparties RP2006/RP2011/RP2016 appariées. **Code identique ≠ géométrie identique.**
- Source secondaire candidate 2013 (republication 2015) : ZIP privé SHA `c6afee56f81b3a9d08316034f0f48259162276a3d7a0d11388c2472f2fd5d3a7`, dix occurrences par code mais écarts de duplication infimes ; 992 polygones SIG valides. Dérivé RP2011 privé, SHA `a1ea1c1cb78172d1b6725d55307026b0f3b5ae0094a8c130dbfd52d7c8b5a2b2`. Voir `docs/iris-2013-candidate.md`. Jamais publié.
- **Nouveau contrôle indépendant** : archive 2013 modifiée par OSM (ODbL), SHA `deb1b378aefa823ad3f2b22700c5c12b8133f782ddb87f059b1dc7518207a2c2`, et archive secondaire « 2016 » (pas géographie RP2016 2018), SHA `843049e9af98c25bb74f9c8d8fe84348429596a3bf69fb6406b77fa8951436cd`. Chacune contient 992 codes Paris uniques et 0 forme invalide. Comparaison métrique Lambert-93 : IoU médiane 2013/OSM **1,00000**, 2013/2016 **0,93688**, 2016/IGN2025 **0,98472**. Voir `docs/iris-crosscheck.md` et `scripts/audit_iris_crosscheck.py`.
- Les trois jeux historiques demeurent des **sources secondaires non authentifiées comme livraisons IGN d'origine** ; ne pas les publier, ni attribuer une édition 2018 au fichier 2016.

## Décisions, blocages, prochaines étapes
1. Vérifier le dernier commit GitHub, fermer la PR de cette passe après tests, actualiser passation et libérer locks. Ressources AgentCTL verrouillées pendant l'écriture : `repo:Kiwinokoto/vacant`, `state:vacant`.
2. **Blocage externe :** obtenir les Contours…IRIS IGN d'origine pour les géographies 2008, 2013 et 2018 ou une attestation vérifiable de provenance de l'un des jeux secondaires. Voir `docs/demande-archives-ign.md`. Le texte est prêt mais **aucun courriel n'a été envoyé** (accès Gmail non autorisé lors du contrôle).
3. Après réception : audits CRS/SHA/licence, 992 codes et formes, géométrie GEOS, IoU et ruptures, provenance, métadonnées, puis seulement envisager une PR d'affichage IRIS année par année avec tests navigateur. En attendant garder la carte par arrondissement.
4. Sujets indépendants : UX mobile, popups, favicon ; audit hauteur/datation du bâti Apur/IGN sans confondre l'âge de fiche et l'âge de construction.

## Sécurité / passation
- Aucune migration BDD, service tiers, modification Docker, déploiement ou donnée LOVAC individuelle dans cette passe.
- Ancien clone VPS `/srv/vacant/source` est périmé, ne jamais le prendre comme vérité. Nouveau clone : `/srv/vacant/work-iris-independent-crosscheck`.
