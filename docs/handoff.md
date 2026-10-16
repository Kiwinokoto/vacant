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
