# Passation VACANT — 2026-10-16

## État Git de référence
Dépôt créé vide ; main initialisé par commit b42b1a47fc7fcbee2219a248db3c302877bae43b (README de garde-fous). Travail actuel sur **dev/source-audit-and-map**, à vérifier sur GitHub à la reprise. Aucun déploiement public autorisé.

## Décisions
- Paris intra-muros, public, statique, pas de données à risque individuelles.
- Paris Data Volumes bâtis v0.1 : **étages seulement**, âge/hauteur métrique/vacance **inconnus**.
- Apur Emprise bâtie Paris prioritaire pour recherche âge+hauteur ; Insee RP2023 IRIS prioritaire pour vacance ; LOVAC agrégé uniquement Paris commune.
- Historique avant 1900 : cartes originales sourcées et reconstruction explicitement qualifiée, jamais fiction annualisée.
- ODbL Apur/Paris Data et Licence Ouverte pour les autres sources selon fiche ; pas de réutilisation mixte sans audit de compatibilité.

## Réalisé
Audit officiel documentaire et premier contrat de données. Base statique et tests contractuels préparés sur la branche de développement ; vérifier l'état/CI/PR exact après commit.

## Incertitudes / blocages
- Aucun téléchargement réel des fichiers Apur, Insee/IRIS, IGN ni test réseau direct de l'API dans cet environnement. Couverture/CRS/attributs et qualité locale non certifiés.
- CORS, pagination et restrictions de l'API doivent être vérifiés dans un navigateur réel.
- Aucun contrôle des éventuelles branches/clones non poussés ni lease AgentCTL externe disponible depuis les seules métadonnées GitHub.
- Droits et formalités de diffusion des images historiques à traiter source par source.

## Prochaines étapes
1. Vérifier branche/HEAD/PR, travaux concurrents et leases avant écriture.
2. Ouvrir l'application avec accès réseau, vérifier sur vraie zone et enregistrer un test API + capture d'une réponse schéma ; relever volumes chargés/erreurs.
3. Télécharger un extrait Apur officiel, contrôler datation/hauteur, licences et jointure exacte ; ajouter tests de comparaison spatiale.
4. Télécharger RP2023 + limites IRIS 2025, contrôler variables, dénominateur et suppression des petits effectifs, **puis seulement** afficher la vacance en polygones IRIS.
5. Valider architecture 3D à partir de hauteurs **en mètres**, puis revue et éventuelle promotion/déploiement sur demande explicite.

Ressources : repo GitHub vacant uniquement ; **aucun VPS, aucune base ni déploiement occupé** lors de cette passe. Aucun lock créé sur une ressource distante.
