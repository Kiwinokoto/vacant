# VACANT — checkpoint de reprise Apur

**16 octobre 2026, 18 h 12 (Europe/Paris).** Document prioritaire pour le prochain chat ; les autres sections de `docs/handoff.md` sont des historiques et peuvent contenir des indications devenues obsolètes.

## Source de vérité et environnement

- Dépôt GitHub canonique : `Kiwinokoto/vacant`, branche `main`. **HEAD avant ce checkpoint** : `cbf7e2ef2869e7e185ef1eb836932c8f045a9c1e` (PR #13, #14 et #15 fusionnées), aucune PR ouverte à ce contrôle. Le commit `main` évoluera lorsque cette passation sera fusionnée.
- Production : https://vacant.kiwinokoto.fr ; VPS personnel ; conteneur `vacant-vacant-web-1`. **Release effectivement déployée** : `1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0` (PR #13). Elle répond HTTP **200**, conteneur actif, zéro redémarrage au contrôle de 18 h 12. `main` est plus récent **uniquement à cause de scripts d’audit et de documentation** ; **ne pas redéployer par réflexe**.
- Ancienne release `2424a45ad590901e3c96c781e10d8b2309c874cb` conservée pour rollback. Les dérivés cartographiques publics sont `iris-2023.geojson` et `arrond-history.geojson` ; les candidats anciens ne sont **pas** exposés.
- Derniers tests : **25/25 Node, 48/48 Python** ; recette Chromium sur le site public réussie (desktop/mobile, chronologie, deux erreurs réseau simulées). Ce sont des résultats de la passe précédente, **pas des tests rejoués lors de ce checkpoint**.
- Aucun verrou AgentCTL VACANT actif au contrôle initial de 18 h 12. Contrôler à nouveau verrous, branche, GitHub, état local, déploiement et autres agents **avant** chaque nouvelle écriture. Lire `AGENTS.md`, `docs/sources.md`, `docs/architecture.md`, `docs/apur-bati-audit.md`.

## État scientifique et décisions

- **Vacance** : statistiques Insee 2006/2011/2016/2023 par arrondissement ; IRIS fins uniquement pour 2023, sur contours géographie 2025. Interdiction de déduire qu’un logement, une adresse ou un immeuble précis est vacant.
- **Fonds IRIS historiques** : géographie 2013 techniquement corroborée par Atlasanté 2014, mais millésime exact et droits de rediffusion à confirmer. Fonds 2008 et 2018 non authentifiés. Courriel envoyé le **16/10/2026** à `contact.geoservices@ign.fr`, ne pas renvoyer de doublon ; vérifier le fil Gmail avant toute relance.
- **Apur** : source géographique `https://carto2.apur.org/apur/rest/services/OPENDATA/EMPRISE_BATIE_PARIS/MapServer/0`, polygones EPSG:2154, licence ODbL annoncée (conditions de redistribution encore à instruire). Rapport : `docs/apur-bati-audit.md` ; code `scripts/audit_apur_emprises.py`, tests `tests/test_audit_apur_emprises.py`.
- Audit du service en lecture seule **agrégée** : **128 206 emprises**, dont **128 090** avec hauteur médiane `h_med` strictement positive, **120 412** avec période `c_perconst` connue, **47 056** sans année exacte `an_const`, **3** hauteurs médianes supérieures à 200 mètres. Aucune géométrie d’emprise Apur téléchargée ou affichée jusque-là.
- Une **emprise Apur peut représenter plusieurs bâtiments**. Les `h_med/h_moy/h_min/h_max` sont en **mètres** ; `H_ET_MAX` Paris Data est un **nombre d’étages** et `D_CRE` est une date de **fiche**, pas une date de construction. Aucune jointure aveugle Apur/Paris Data/Insee.

## Mission suivante, dans cet ordre

1. Vérifier la provenance/version datée du jeu d’**emprises bâties Apur**, son schéma et la licence ODbL (droits d’affichage, attribution, éventuelle redistribution de dérivés).
2. Faire un **petit échantillonnage en lecture seule**, borné et documenté, des géométries `n_sq_eb`, `h_med`, `c_perconst`, `an_const` : validité SIG, emprises sans date, les **trois `h_med` > 200 m**, coordonnées/projection, tailles, couverture, outliers. Ne pas télécharger en masse ni publier des détails sans nécessité.
3. Concevoir d’abord une **carte expérimentale par périodes de construction**, et ensuite les hauteurs médianes **en mètres**, dans une branche `dev/*`. Rendre les sources, l’incertitude, le millésime des données et l’unité visibles. Contrôler licences, performances (desktop/mobile), pagination et géométries avant activation.
4. PR ciblée, tests Python/Node et Chromium ; ne déployer qu’après contrôle du périmètre, des verrous et du rollback. Préserver les deux GeoJSON publics existants et ne jamais attribuer un taux de vacance d’IRIS aux emprises.
5. En parallèle ou après la couche Apur, reprendre la recherche des originaux IGN 2008/2018 et traiter une éventuelle réponse au courriel.

## Passation et sécurité

Ne jamais prendre les anciens clones VPS (`/srv/vacant/source`, branches `dev/*` de passes antérieures) pour la source de vérité. Utiliser GitHub comme référence, vérifier HEAD et éventuels travaux concurrents, verrouiller uniquement la ressource mutable, documenter les tests et limitations, libérer les leases à la fin. **Aucune migration BDD, aucun changement DNS/Traefik/Docker ni déploiement n'est requis pour cette passation ou pour la première inspection Apur.**
