# VACANT — passation active après audit SIG du 16/10/2026

## Fin de passe — 16 octobre 2026, vers 15 h 39 (heure de Paris)

- **PR #6 fusionnée**, code et audit du candidat IRIS 2013 intégrés à `main` via squash `75d8989c8f5082b32d4fb04965257d8727d949e0`. Aucun changement du site ni des fichiers GeoJSON publics.
- Validation finale : 22 tests JavaScript et 27 tests Python passent. Audit SIG rejoué depuis l'archive ZIP originale vérifiée, sans raccourci vers une extraction locale ; 992 IRIS, duplication 10× contrôlée, 0 géométrie invalide, recouvrement médian 2013/2025 de 0,947. Preuves et SHA : `docs/iris-2013-candidate.md`.
- Fichier dérivé RP2011/géographie candidate 2013 **strictement privé** (`/srv/vacant/data/processed/iris-2013-candidate/iris-2011-candidate.geojson`) ; l'archive brute est également privée. Répertoires candidats à permissions `0700`, fichiers `0600`. Vérification HTTPS : `/data/iris-2011-candidate.geojson` renvoie **404**, les anciens GeoJSON publics renvoient HTTP 200.
- Dernière release de production observée : `/srv/vacant/releases/2424a45ad590901e3c96c781e10d8b2309c874cb/site`, conteneur actif, aucun redémarrage. Le clone local `/srv/vacant/work-iris-2013-candidate` a un commit non poussé en direct, mais le contenu du commit GitHub a été vérifié par égalité des arbres Git.
- Suite prioritaire : vérifier indépendamment l'édition géométrique IGN 2013 et les conditions de redistribution, puis identifier des éditions 2008 et 2018 authentifiées. **Ne pas activer les polygones secondaires en production sans ce contrôle.**

## État confirmé
- Vérité GitHub au début de la passe : \`Kiwinokoto/vacant\` \`main\` à \`ecfea2e195e8f65da340f4e3beb60419b3dcd596\`. Travail de cette passe sur \`dev/iris-2013-candidate\`. Avant de reprendre, vérifier HEAD GitHub, PR, état des clones et verrous AgentCTL ; **ne pas utiliser le vieux clone /srv/vacant/source** comme vérité.
- Production VACANT **inchangée** : https://vacant.kiwinokoto.fr, conteneur \`vacant-vacant-web-1\` sur VPS personnel, release \`2424a45ad590901e3c96c781e10d8b2309c874cb\` à vérifier à chaque reprise.
- Couche IRIS 2023 validée (992 codes et 929 taux) + comparaison statistique 2006/2011/2016/2023 à **20 arrondissements**. Aucun bâtiment n'est identifié vacant.
- Références Insee géographie 2008, 2013, 2018, 2025 archivées et appariées à 992 codes Paris (audit \`docs/iris-historique.md\`). Mais des codes identiques ne prouvent pas des contours identiques.
- **NOUVEAU :** source secondaire 2013 (data.gouv.fr, republication 2015) téléchargée privée. SHA-256 \`c6afee56f81b3a9d08316034f0f48259162276a3d7a0d11388c2472f2fd5d3a7\`. 9 920 lignes Paris = 10 × 992 codes ; 3 variantes quasi identiques par code ; 0 polygone invalide, 0 chevauchement SIG significatif. Recouvrement par code vs contours IGN 2025 : médiane 94,7 %, minimum 63,83 %. **Il ne s'agit pas d'un original IGN audité.**
- Dérivé privé IRIS 2011 / géographie candidate 2013 : \`/srv/vacant/data/processed/iris-2013-candidate/iris-2011-candidate.geojson\` (1 240 568 octets), SHA \`a1ea1c1cb78172d1b6725d55307026b0f3b5ae0094a8c130dbfd52d7c8b5a2b2\`. **Jamais mis dans site/data ou GitHub**, ne pas le traiter comme géographie certifiée.
- Code candidat : \`scripts/audit_iris2013_candidate.py\` et \`tests/test_iris2013_candidate.py\`. Preuves complètes : \`docs/iris-2013-candidate.md\`.

## Suite
1. Reprendre les contrôles GitHub/locks, réaliser la revue du script et des tests, conserver les bruts dans \`/srv/vacant/data/raw\`, manifestes privés sous \`/srv/vacant/data/manifests\`.
2. Obtenir une géométrie IGN **originale** de millésime 2013, comparer quantitativement le candidat à l'original ; vérifier la compatibilité avec RP2011 et les droits de redistribution. Ne pas publier une source secondaire comme original.
3. Chercher séparément les originaux 2008 et 2018. Si aucune édition n'est accessible, conserver l'historique par arrondissement.
4. En cas de future validation, créer une nouvelle PR avec tests navigateur, attribution, légende année/géographie distinctes et garantie de ne jamais utiliser le 2025 pour 2006/2011/2016.
5. Prochains sujets indépendants : test mobile, popups, favicon, Apur pour datation/hauteur.

## Concurrence
Travail sur nouveau clone privé \`/srv/vacant/work-iris-2013-candidate\`, verrous temporaires \`repo:Kiwinokoto/vacant\` et \`state:vacant\`, à libérer au terme de la passe. Aucun service Docker, base ou déploiement modifié ici.

---

# VACANT — passation active (16/10/2026)

## Source de vérité et production
- Repo public `Kiwinokoto/vacant` ; dernière base `main` vérifiée avant cette passe : `babf33c7e50bbf2591064c85f111cb5f19a7a02b`. La branche de cette passe est `dev/iris-historical-references` ; **vérifier GitHub, PR et HEAD à la reprise**, car ils peuvent évoluer.
- Production : https://vacant.kiwinokoto.fr, VPS personnel `vmi2505789.contaboserver.net` via RDC LGC. Release `2424a45ad590901e3c96c781e10d8b2309c874cb` active au contrôle de début ; conteneur `vacant-vacant-web-1`, données statiques en lecture seule, Traefik/TLS.
- Sources originales **privées** : `/srv/vacant/data/raw`, manifestes SHA-256 `/srv/vacant/data/manifests`, dérivés `/srv/vacant/data/processed` ; ne jamais publier de fichier brut ou LOVAC individuel.

## Accompli précédemment
- 2023 : 992 IRIS Paris Insee/IGN 2025, 929 taux affichés (petits effectifs grisés), GeoJSON SIG validé GEOS. **Pas de logement déclaré vacant à l'immeuble.**
- 2006/2011/2016/2023 : comparaison par 20 arrondissements, valeurs Insee calculées à partir des 992 IRIS de leur année respective ; les contours d'arrondissement sont tirés des contours IGN 2025 (aucune géométrie IRIS historique inférée).
- Carte de volumes bâtis actuels Paris Data (nombre d'étages, pas hauteur métrique), plafond volontaire 800 volumes et avertissement de troncature. Bascule de couche, retour au zoom précédent, tests navigateur validés précédemment.
- PR #2/#3/#4 fusionnées, états documentés dans GitHub.

## Passe présente : références géographiques historiques
- Quatre originaux Insee officiels **ajoutés et archivés en lecture privée** : IRIS 2008, 2013, 2018 et passage 2008→2013. SHA-256 et URL dans [l'audit historique](iris-historique.md).
- Concordance **992 codes parisiens sans aucun ajout/suppression** entre 2008/2013/2018/2025, et chaque fichier de recensement RP2006/RP2011/RP2016 est apparié sans lacune au référentiel de la géographie correspondante.
- Entre 2013/2018 : 24 libellés changés ; entre 2018/2025 : 212 ; aucun changement de type. Table de passage 2008→2013 : 0 ligne de mouvement concernant Paris.
- **Bloquant scientifique :** mêmes identifiants ≠ mêmes polygones. Les contours IGN 2008/2013/2018 originaux ne sont pas acquis. **Aucune nouvelle couche géographique fine activée.** Les géométries publiques anciennes proposées par des tiers ne sont pas équivalentes sans contrôles.
- Code : `scripts/collect_insee.py` étendu, `scripts/audit_iris_references.py` nouveau, tests ajoutés. Consulter `docs/iris-historique.md`.

## Suite ordonnée
1. Contrôler verrous AgentCTL, états des ressources, GitHub `main`, branches, PR, CI et éventuelles modifications locales avant écriture. `AGENTS.md` et ce document servent de passation.
2. Récupérer les contours historiques **éditions d'origine** IGN (2008/2013/2018). Avant intégration, prouver édition, droits, somme SHA, CRS, alignement avec le recensement, topologie et couverture.
3. Préparer une couche distincte pour chaque année, sans attribuer d'estimation IRIS à un immeuble ; ne jamais substituer les contours 2025 aux anciennes géographies.
4. À défaut de fonds exacts, conserver la représentation par arrondissements ; autres améliorations possibles et séparées : tests mobiles, popups, favicon manquant, puis étude APUR/BD TOPO pour hauteur/âge du bâti.

## Coordination
Verrous utilisés pour cette passe : `repo:Kiwinokoto/vacant` et `state:vacant` ; les relâcher en fin. Ne pas écraser les vieux clones VPS ; clone dédié `/srv/vacant/work-iris-boundaries-20261016`. Ne toucher ni aux autres services ni à la prod dans cette passe. Tests et commits doivent être consignés avant sortie.
