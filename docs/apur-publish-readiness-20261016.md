# VACANT — revue de prépublication Apur, compression et sécurité des releases

**Revue du vendredi 16 octobre 2026 — aucune fusion ni aucun déploiement.**

## Base de référence

- GitHub canonique `Kiwinokoto/vacant`. `main` : `72a9d06377541b7b266e0d8153e89a7ae19afb95`. PR **#23** de consolidation : `242799a83c4846d3ad55da948b7405a832dbd5b3` ; PR **#24** de raccordement local : `3ada6d9e0fb713edaa8dcea9a76f43f36d8aeaed`. Les deux sont en brouillon, en attente de revue. Cette branche **se superpose à la #24**, laquelle a la #23 pour base ; ne pas l'envoyer sur `main` indépendamment.
- Production statique volontairement maintenue sur `1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0`. Aucun accès aux données Apur depuis une URL publique. Le mode Apur est visible seulement sur `localhost` avec `?apur_lab=1`.
- Source Apur figée `EMPRISE_BATIE_PARIS` SHA-256 ZIP `f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11` ; **456 cellules privées** en grille 500 m, **128 089 emprises distinctes**, **138 381 placements**, **104 mauvaises géométries GEOS** et **13 identifiants métier manquants** exclus. Manifeste figé SHA `bb02fe9ac9ef7919018118659e12ac533b098234250eba540c6975e7b273bb0c`.
- Les périodes sont **attribuées à des emprises actuelles**, les hauteurs médianes `h_med` sont en **mètres** (pas les étages `H_ET_MAX` Paris Data), aucune vacance de logement n'est affectée à une emprise.

## Point critique de sécurité corrigé : copie d'une release

La procédure `deploy/README.md` proposait une copie globale `site/*` depuis un checkout. Or **`.gitignore` ne protège pas contre une telle copie**, et la recette locale de la PR #24 place temporairement les cellules privées dans `site/data/apur-grid/`. Risque : diffusion accidentelle de plusieurs Mo de données Apur **avant** validation des obligations ODbL.

La procédure est remplacée, pour les prochaines releases seulement, par **`scripts/stage_reviewed_release.py`** :

1. Accepte uniquement un **commit Git SHA complet égal au HEAD du checkout** ; fabrique un arbre `site/` depuis `git archive`, donc **fichiers suivis par Git exclusivement**, jamais les copies locales ignorées.
2. Refuse les chemins privés dans Git (sauf le marqueur `.gitignore` non copié), fichiers `*.geojson`/`*.json` inattendus, symlinks d'archives et archives hors périmètre, ou fichier géographique ajouté de force.
3. Demande **explicitement** les deux seules données géographiques publiques : `iris-2023.geojson` et `arrond-history.geojson`, avec **SHA-256 déjà audités**, avant toute copie. Refuse un fichier absent, altéré, trop gros ou un lien symbolique source.
4. Construit une **release neuve** à un chemin nommé par le commit, sans écraser une release existante ; staging d'abord privé, puis `site` et la release en lecture pour Nginx. **Aucun démarrage Docker et aucune action de déploiement**.
5. Exige un `--execute` volontaire. Les anciennes releases immuables restent intactes, les fichiers de test source privés aussi.

Recette du garde-fou sur clone réel de la branche : release artificielle en **`/tmp`**, fichiers Insee/arrondissements de l'ancienne release de production et leurs empreintes vérifiées, **aucun dossier `apur-grid/`, aucune fixture `apur-lab.geojson`**, sortie `755` pour les dossiers et `644` pour `index.html`. Les **sept nouveaux tests de sécurité** sont réussis : présence de fichiers ignorés, refus de les importer, tentative de suivi forcé, fichier inattendu, mauvais hash, mauvaise version, symlink et relance sans écrasement.

**Limitation :** ce script doit être employé lors de la prochaine préparation de release ; il ne neutralise pas magiquement une copie manuelle non conforme. Son utilisation et les contrôles sont désormais prescrits dans `deploy/README.md`. Pas de déploiement effectué dans cette passe.

## Mesures de compression sur les 456 cellules *réelles*

Calculs sans modification du GeoJSON, compression en mémoire (Node zlib gzip niveau 4 / Brotli qualité 4), chaque cellule compressée **indépendamment** :

| Mesure | Brut | gzip-4 | Brotli-4 |
|---|---:|---:|---:|
| Total 456 cellules (octets) | **91 515 440** | **27 435 040** | **23 089 233** |
| Réduction vs brut | — | **70,0 %** | **74,8 %** |
| Plus grosse cellule (octets) | 796 937 | 230 332 | 177 790 |
| Manifeste seul (octets) | 152 865 | 39 096 | 36 314 |

Temps de compression de toutes les cellules, sur VPS à ce niveau de qualité : **environ 5,3 s** ; mesure indicative de CPU, pas débit de production. Les empreintes SHA-256 **actuelles** restent celles du fichier GeoJSON décodé, y compris en HTTP `Content-Encoding: gzip` : le navigateur reçoit et vérifie les octets après décompression HTTP.

### Chargement réseau simulé dans Chromium

Linux desktop + Chromium en mobile **390×844** ; serveur HTTP strictement bouclé sur `127.0.0.1`, réponse compressée à la volée sans écrire de nouvel export. Réseau simulé avec `Network.emulateNetworkConditions` : **1,6 Mbit/s en téléchargement (200 000 octets/s), latence 150 ms**, une seule navigation par scénario. Requête manuelle identique sur le même emplacement (4 cellules, **2 284 emprises uniques**, 2 374 occurrences). Manifest inclus dans le volume transmis :

| Scénario | Octets servis | Temps clic → emprises visibles |
|---|---:|---:|
| HTTP sans compression | **1 610 329** | **8 973 ms** |
| HTTP avec `gzip` niveau 4 | **466 240** | **3 297 ms** |

Les emprises affichées, le manifeste et les SHA-256 de cellules ont passé les validations dans les deux scénarios ; aucun débordement ni erreur JS. La réduction de temps observée sur ce seul scénario est ~**63 %**. Les requêtes multiples sont encore **séquentielles**, ce qui accumule la latence. Un chargement contrôlé en parallèle pourrait l'améliorer, mais réclame une nouvelle recette de concurrence et une limite stricte de mémoire.

**Attention :** il s'agit d'une **émulation Chromium de débit et latence**, pas d'un test sur vrai smartphone, réseau 4G réel, Nginx chargé ou plusieurs visiteurs. Mesures indicatives, non garanties. La configuration Nginx du dépôt est désormais préparée avec `gzip on`, `gzip_comp_level 4`, `gzip_vary on` et les types `application/geo+json` / `application/json`, mais **la configuration réellement déployée en production n'a pas été modifiée**. Envisager PMTiles/TopoJSON uniquement après mesure vérifiable de couverture et d'altération géométrique.


### Vérification sur un véritable serveur Nginx isolé

Script de recette versionné : `scripts/recipe_nginx_gzip_loopback.py`, à exécuter depuis un clone contrôlé par :

```sh
python3 scripts/recipe_nginx_gzip_loopback.py --config deploy/nginx.conf
```

Le script ne lance **aucun conteneur**, ne modifie aucune configuration système et ne contacte pas un domaine public. Il fait démarrer un Nginx autonome sur un port **127.0.0.1** éphémère, sert uniquement des **géométries et métadonnées synthétiques**, exerce les en-têtes puis arrête le processus en `finally`. Aucun extrait réel Apur n'entre dans sa racine de test.

Recette réussie sur le VPS avec Nginx **1.18.0** :

- `cell_test.geojson` : **51 831 octets** bruts, **1 061 octets** avec gzip-4 (jeu artificiellement répétitif, donc ratio *non comparable* aux vraies cellules), MIME `application/geo+json` ;
- `manifest.json` synthétique : **1 503 → 618 octets**, MIME `application/json` ;
- `Content-Encoding: gzip` et `Vary: Accept-Encoding` présents uniquement quand négociés ; `Accept-Encoding: identity` rend les octets strictement identiques au fichier ;
- fichier trop petit non compressé, module `.mjs` avec MIME JavaScript valide, dotfiles refusés HTTP 403, fichiers absents HTTP 404 ;
- les octets décompressés correspondent **strictement** à la source synthétique, condition nécessaire à une validation SHA-256 côté client.

Un premier lancement du laboratoire a rencontré une attente de démarrage, mais le script non modifié a été rejoué avec succès après le diagnostic. Le serveur reste arrêté à la fin. Cela valide la **négociation HTTP** sur Nginx réel ; cela n'est ni un déploiement Nginx production, ni une mesure de concurrence, ni une preuve de performance réelle.

## Checklist ODbL 1.0 avant une couche publique

Source officielle Apur : [fiche EMPRISE BATIE](https://www.apur.org/open_data/EMPRISE_BATIE_OD.pdf), datée **01/09/2019**, mentionne **Open Data ODbL** et les limites d'exactitude par emprise. Le **millésime métier du SHP figé d'octobre 2026 reste non confirmé**, ce que la licence ne règle pas. Sources juridiques : [Open Data Commons, texte ODbL-1.0](https://opendatacommons.org/licenses/odbl/1-0/), sections pertinentes :

- **§ 4.2, 4.3 :** conserver les mentions de l'Apur, de la base, du lien de licence et l'attribution visible sur la carte/oeuvre produite ;
- **§ 4.4 :** si l'usage est public et la base transformée, diffuser la base dérivée selon ODbL ou licence compatible ;
- **§ 4.6 :** fournir gratuitement en ligne la base dérivée lisible par machine **ou** le fichier/la méthode de modifications permettant de la reconstruire ;
- **§ 4.7 :** ne pas imposer des mesures techniques incompatibles avec les droits garantis par la licence.

La licence **permet le développement privé sans attendre une autorisation individuelle**, mais n'autorise pas à présenter la date de mise à jour du serveur comme un millésime scientifique certain. Des droits sur d'autres contenus associés peuvent devoir être examinés séparément. Cette synthèse juridique ne remplace pas un avis spécialisé.

## Décision de revue

**PR #23 et #24 techniquement cohérentes pour l'expérimentation locale**, mais **non prêtes pour activation publique**. Points restants :

1. Employer systématiquement le garde-fou de release avant toute mise en ligne, même si la couche Apur est désactivée.
2. Préparer un vrai plan de distribution ODbL avec fichier/manifeste datés et transformations reproductibles, compatible avec la visibilité publique de la base adaptée.
3. Confirmer le millésime auprès de l'Apur ; conserver « millésime non confirmé » tant que nécessaire.
4. Tester les en-têtes de compression sur un serveur de recette isolé, les latences réseau et la mémoire d'un **vrai téléphone**, puis la charge d'utilisateurs simultanés.
5. Revoir éventuellement le séquencement des requêtes par cellule, la mise en cache, et les sorties plus compactes. Ne pas considérer la grille par périodes comme une reconstruction historique attestée et ne pas associer de vacance aux emprises.

**Aucune PR fusionnée, aucune modification de `main`, aucune nouvelle release activée.**
