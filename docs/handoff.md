# VACANT — passation active (16 octobre 2026)

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
