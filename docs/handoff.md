# Passation VACANT — 2026-10-16

## État Git de référence
Dépôt créé vide ; main initialisé par commit b42b1a47fc7fcbee2219a248db3c302877bae43b (README de garde-fous). Travail sur **dev/source-audit-and-map** au commit initial de livraison `012ba9160a73fe243bc81413ef25cf35e193f259`, proposé dans la [PR brouillon #1](https://github.com/Kiwinokoto/vacant/pull/1). La présente mise à jour constitue un second commit : contrôler le SHA courant à la reprise. Aucun déploiement public autorisé.

## Décisions
- Paris intra-muros, public, statique, pas de données à risque individuelles.
- Paris Data Volumes bâtis v0.1 : **étages seulement**, âge/hauteur métrique/vacance **inconnus**.
- Apur Emprise bâtie Paris prioritaire pour recherche âge+hauteur ; Insee 2006–2023 IRIS prioritaire pour vacance (jalons 2006/2011/2016/2023, comparaison ≥5 ans et 2016–2023=7 ans) ; LOVAC agrégé 2020–2026 uniquement Paris commune.
- Historique avant 1900 : cartes originales sourcées et reconstruction explicitement qualifiée, jamais fiction annualisée.
- ODbL Apur/Paris Data et Licence Ouverte pour les autres sources selon fiche ; pas de réutilisation mixte sans audit de compatibilité.

## Réalisé
Audit documentaire des organismes officiels, architecture, interface statique 2D (polygones de volumes Paris Data chargés manuellement ; étages, pas mètres, aucune vacance par immeuble), README et tests. **9 vérifications contractuelles sur le module source récupéré de GitHub réussies dans un environnement JS**, mais la suite complète `node --test` n'a pas été exécutée. PR #1 brouillon ouverte ; pas de merge ni CI déclenchée volontairement.

## Dernière extension (chronologie)
Démarrage statistique **2006** acté dans [chronologie.md](chronologie.md). Chronologie de chiffres **Paris entier** vérifiés dans deux tableaux officiels Insee ajoutée au panneau du site ; aucune mise en couleur des polygones ni cartographie IRIS historique. Nouveaux modules `site/timeline.mjs`, `tests/timeline.test.mjs`. Chiffres historiques 2006/2011/2016 transcrits du RP2022 ; 2023 du RP2023 harmonisé. Écarts d'une unité autorisés dans les sommes arrondies. Important : ne pas comparer les millésimes annuels voisins, et ne pas superposer 2023 sur le bâti actuel comme observation historique.

## Incertitudes / blocages
- Aucun téléchargement réel des fichiers Apur, Insee/IRIS, IGN ni test réseau direct de l'API dans cet environnement. Couverture/CRS/attributs et qualité locale non certifiés.
- CORS, pagination et restrictions de l'API doivent être vérifiés dans un navigateur réel.
- Aucun contrôle des éventuelles branches/clones non poussés ni lease AgentCTL externe disponible depuis les seules métadonnées GitHub.
- Droits et formalités de diffusion des images historiques à traiter source par source.

## Prochaines étapes
1. Vérifier branche/HEAD/PR, travaux concurrents et leases avant écriture.
2. Ouvrir l'application avec accès réseau, vérifier sur vraie zone et enregistrer un test API + capture d'une réponse schéma ; relever volumes chargés/erreurs.
3. Télécharger un extrait Apur officiel, contrôler datation/hauteur, licences et jointure exacte ; ajouter tests de comparaison spatiale.
4. Télécharger à partir de 2006 (XLS géographie 2008) et jalons 2011/2016 puis RP2023 (schéma harmonisé + géographie 2025), contrôler variables, dénominateurs, changement de limites et petits effectifs, **puis seulement** afficher la vacance en polygones IRIS sans extrapolation spatiale.
5. Valider architecture 3D à partir de hauteurs **en mètres**, puis revue et éventuelle promotion/déploiement sur demande explicite.

Ressources : repo GitHub vacant uniquement ; **aucun VPS, aucune base ni déploiement occupé** lors de cette passe. Aucun lock créé sur une ressource distante.
