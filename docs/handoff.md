# ETAT COURANT — 16 octobre 2026 (prioritaire aux notes anciennes)

- PR #2 fusionnée dans main, commit 32ddd63fd45844113b74ba0a85ef4c5bdb7dc200. La release publique actuelle est /srv/vacant/releases/2424a45ad590901e3c96c781e10d8b2309c874cb/site (ancien déploiement 2e1a198e69f29e8ee36f8e462e839f68bb8b8565 conservé pour rollback).
- Branche de développement issue de ce main : dev/history-arrond-ux. Vérifier HEAD, PR, scripts/test et présence de verrous AgentCTL à chaque reprise.
- Les originaux sous /srv/vacant/data/raw/insee sont privés et conservés avec manifestes SHA dans /srv/vacant/data/manifests. Ne jamais les servir en HTTP.
- Insee RP2006, RP2011, RP2016 : 992 IRIS parisiens uniques par fichier, pas de logement/vacance manquant, géographies 2008, 2013, 2018 ; totaux Paris vérifiés (≈1 334 814/122 667, ≈1 356 074/98 698, ≈1 374 377/114 306).
- RP2023 et IGN contours 2025 : 992 IRIS cartographiés, 929 taux colorés ; dérivé /srv/vacant/data/processed/iris-2023/iris-2023.geojson SHA 0b79e30afb5055448d4561960f55db3cc92a84feb2a498adb2588c00b6499a6f.
- Cartographie des millésimes anciens UNIQUEMENT par 20 arrondissements : agréger les IRIS en codes 75101..75120 avec les valeurs de leur propre millésime, puis dissoudre les contours IGN 2025 pour afficher les limites d'arrondissements, qui servent de maille géographique stable. Jamais affecter une valeur ancienne aux IRIS de 2025.
- Générateur : scripts/build_arrondissement_history.py, avec vérification des SHA, données, catégories, cardinalité, arrondissements et topologie. Dérivé attendu /srv/vacant/data/processed/arrond-history/arrond-history.geojson ; sortir 20 polygones et quatre séries 2006/2011/2016/2023 sans données individuelles.
- UI : nouvelle couche historique par arrondissement, année liée à la chronologie, retour au centre/zoom de rue depuis les couches statistiques. Si une ancienne année est choisie quand IRIS 2023 est actif, transition automatique vers arrondissements.
- Tests réalisés : 22/22 Node et 17/17 Python, plus Chromium réel sur le site public : IRIS 2023 (992 IRIS, 929 taux), bascule vers les 20 arrondissements en 2006/2011/2016/2023, zoom 17 restauré après désactivation, 800 volumes chargés sans doublon/rejet avec avertissement de troncature. Aucune erreur applicative. Les popups cartographiques et le mobile restent à approfondir.
- Déploiement : release immuable contenant uniquement les dérivés validés sous site/data, sous locks AgentCTL deploy:vps-personal/vacant, service:vacant, host:vps-personal/docker ; rollback possible vers ancienne release. Vérifier service, TLS, types MIME et hashes.
- Aucun LOVAC individuel, aucune vacance au bâtiment. Les volumes Paris Data restent contemporains (étages, pas hauteur métrique). Favicon 404 et limite 800 volumes restent des dettes mineures.

---
# Passation VACANT — état opérationnel au 16 octobre 2026

## Source de vérité GitHub
- Dépôt public : `Kiwinokoto/vacant`, branche `main` au squash `df947684403fc34cfe6ab8ce450644b0a3e6ab6b` (PR #1).
- Travail courant : `dev/iris-provenance-validation`, [PR #2](https://github.com/Kiwinokoto/vacant/pull/2) **ouverte en brouillon**. Vérifier son HEAD et les éventuelles modifications concurrentes avant toute écriture ; la présente documentation ajoute des commits au-delà du code déployé.
- **Code en production :** commit `2e1a198e69f29e8ee36f8e462e839f68bb8b8565`. Ne pas confondre ce SHA de release et le HEAD Git de la branche après les commits documentaires. Pas de fusion dans `main` à ce stade.
- Consignes : [AGENTS.md](../AGENTS.md), [sources](sources.md), [architecture](architecture.md), [acquisition](acquisition.md), [déploiement](../deploy/README.md).

## Déploiement confirmé et reprise après interruption
- URL : https://vacant.kiwinokoto.fr — HTTPS et certificat validés depuis le VPS, page et GeoJSON HTTP 200.
- VPS personnel `vmi2505789.contaboserver.net` accessible avec **RDC LGC** ; conteneur dédié `vacant-vacant-web-1` (Docker Compose + Traefik partagé, sans modification des autres services).
- Release active immuable : `/srv/vacant/releases/2e1a198e69f29e8ee36f8e462e839f68bb8b8565/site`.
- Compose et Nginx : `/srv/vacant/working-2e1a198e69f29e8ee36f8e462e839f68bb8b8565/deploy/`. Montage en lecture seule du répertoire du site **et** de `nginx.conf` ; modules `.mjs` servis en `application/javascript`, `.geojson` en `application/geo+json`.
- Ancienne release `9167c822...` toujours conservée pour rollback (ancienne config Compose sans montage Nginx). Ne pas modifier les répertoires de release en place.
- Reprise le 16/10 : 18/18 tests Node, 13/13 tests Python, syntaxe JS et Nginx valides, contenu public conforme aux fichiers de la release ; aucune modification des originaux.

## Données effectivement disponibles
- **Sept fichiers officiels** Insee et IGN archivés avec manifestes SHA-256 sous `/srv/vacant/data/raw/` et `/srv/vacant/data/manifests/` (hors webroot) : recensements 2006, 2011, 2016, 2023 ; dictionnaire 2023 ; référence Insee IRIS géographie 2025 ; contours IGN 2025. Détails et provenances : [acquisition.md](acquisition.md).
- RP2023 Parquet : modalité validée `OCS=DW_VAC` ; couplage indépendant Insee RP2023 / référence Insee 2025 / contours IGN 2025 : **992 IRIS parisiens concordants** et 0 géométrie invalide selon GEOS.
- GeoJSON agrégé : `/srv/vacant/data/processed/iris-2023/iris-2023.geojson`, 822 545 octets, SHA-256 `0b79e30afb5055448d4561960f55db3cc92a84feb2a498adb2588c00b6499a6f` ; copie de ce seul dérivé servie publiquement dans `/data/iris-2023.geojson`.
- Totaux Paris issus de l'assemblage : environ 1 402 024 logements, dont 139 075 vacants selon le recensement 2023. 52 IRIS ont un parc nul ; 63 IRIS sont masqués si le parc est nul ou inférieur à 50 logements, d'où **929 taux représentés**.
- Aucune donnée individuelle LOVAC, aucun statut de vacance affecté à un bâtiment ou à une adresse.

## Vérifications fonctionnelles en navigateur — 16/10/2026
- Chromium headless sur machine LGC : chargement HTTP 200, Leaflet présent, chronologie 2006 / 2011 / 2016 / 2023 fonctionnelle (2023 : 9,9 %).
- Activation IRIS : 992 quartiers validés côté navigateur, 929 taux affichés, pas d'erreur JavaScript.
- Nouveau chargement des volumes sur une vue initiale zoomée : API Paris Data accessible, 800 volumes représentés, 0 rejeté, 0 doublon ; avertissement honnête de **troncature 800/3054**, puisque le plafond de récupération est volontairement 800.
- En quittant la couche IRIS, la carte reste cadrée sur tout Paris : un clic immédiat « Charger les volumes » signale « Zone trop large » jusqu'à un nouveau zoom. C'est une dette UX, pas une panne de collecte.
- `/favicon.ico` renvoie 404 : cosmétique, à traiter ensuite. Cartes OSM et API Paris Data dépendent de services tiers.

## Décisions et limites scientifiques
- Départ statistique **2006**, jalons 2006/2011/2016/2023 ; pas d'interpolation annuelle. Seule **la couche IRIS 2023** est cartographiée à ce stade ; la chronologie des quatre millésimes concerne **Paris entier** et ne recalcule pas le bâti.
- La vacance Insee est une **estimation par zone IRIS**, et non la vacance structurelle LOVAC. Aucune localisation de logement vide n'est établie.
- La couche Paris Data décrit des **volumes bâtis actuels** et leurs nombres d'étages, pas leur hauteur en mètres ni une date de construction. Aucun curseur historique de bâtiments ni 3D métrique fiable.
- Apur / IGN BD TOPO / LOVAC agrégé restent à auditer et réconcilier par licence, granularité, dates et géométrie avant activation.

## Prochaines étapes
1. Recontrôler PR #2 / HEAD, statut des branches, CI/protections, état local et locks AgentCTL avant écritures. Après revue, décider explicitement de la fusion vers `main` ; **ne pas supposer que production suit main**.
2. UX : résoudre la remise à niveau de zoom après IRIS, favicon 404 et tester mobile. Conserver le plafond de récupération et l'avertissement de troncature tant qu'aucun tuilage/stratégie de chargement revue n'existe.
3. Construire les couches IRIS 2006/2011/2016 uniquement avec leurs géographies compatibles, recontrôler les ruptures et les dénominateurs ; pas de séries annuelles fictives.
4. Auditer l'extrait Apur (hauteur, période de construction, couverture, licence, jointures potentiellement n:m) avant une représentation métrique ou historique.

## Coordination et état final
Le déploiement de cette reprise a utilisé des leases AgentCTL `deploy:vps-personal/vacant`, `service:vacant` et `host:vps-personal/docker` et s'est terminé sans incident ni rollback. Aucun verrou durable de déploiement n'est requis hors opération ; contrôler à chaque reprise. L'ancien répertoire `/srv/vacant/source` était en retard par rapport à GitHub ; ne pas le prendre pour source de vérité.
