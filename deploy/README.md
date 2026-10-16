# VACANT — déploiement statique sur le VPS personnel

Le domaine `vacant.kiwinokoto.fr` résout vers le VPS personnel. Traefik v3 est déjà actif avec le réseau externe `traefik_network` et le résolveur TLS `letsencrypt`. Aucune modification de Traefik ni d'un autre service n'est nécessaire.

1. Retenir un commit vérifié de `Kiwinokoto/vacant` (idéalement fusionné dans `main`).
2. **Ne jamais utiliser `cp -r site/*` ou `rsync site/`** depuis un clone de recette : ces commandes peuvent inclure un `site/data/apur-grid/` ou `apur-lab.geojson` ignoré par Git mais **privé**. Construire exclusivement une release à partir de l'archive des fichiers suivis par Git, avec `scripts/stage_reviewed_release.py` (voir ci-dessous).
3. Sélectionner explicitement **les deux dérivés publics déjà validés**, `iris-2023.geojson` et `arrond-history.geojson`, et vérifier leurs SHA-256 **indépendamment consignés au rapport de recette** avant de les inclure. Aucun fichier géographique Apur, brut ou expérimental n'est admis.
4. Acquérir les leases AgentCTL `deploy:vps-personal/vacant`, `service:vacant` et `host:vps-personal/docker`, puis vérifier la configuration : `VACANT_WEBROOT=/srv/vacant/releases/<commit>/site docker compose -f deploy/compose.yml -p vacant config`.
5. Démarrer uniquement le nouveau conteneur VACANT : même variable et `docker compose -f deploy/compose.yml -p vacant up -d`.
6. Contrôler la réponse HTTP→HTTPS, le certificat (pas le certificat par défaut de Traefik), l'HTTP 200 de la page et du GeoJSON, et le chargement de l'API Paris Data.

Le service est statique, sans base ni accès au répertoire des données brutes. **Ne jamais faire de déploiement non verrouillé ou forcé.** Les observations Insee ne permettent aucune conclusion sur un logement ou un immeuble individuel.


Pour la couche historique des arrondissements, ajouter seulement le dérivé validé /srv/vacant/data/processed/arrond-history/arrond-history.geojson sous site/data/arrond-history.geojson, avec contrôle SHA-256. Ne pas monter les Excel/Parquet bruts ni leurs répertoires.

## Étape obligatoire : préparation de release sans données Apur privées

Le script `scripts/stage_reviewed_release.py` archive uniquement les fichiers **suivis par Git à un commit de 40 caractères exactement égal au HEAD local**, exclut le dossier `site/data/apur-grid/` (y compris son fichier marqueur `.gitignore`), et refuse tout autre GeoJSON/JSON non prévu.

Lancer depuis un **clone neuf du commit validé** et uniquement après avoir relevé les SHA-256 des deux dérivés publics depuis leurs manifestes d'audit :

```sh
sha=$(git rev-parse HEAD)
python3 scripts/stage_reviewed_release.py \
  --repo "$PWD" --commit "$sha" \
  --destination "/srv/vacant/releases/$sha" \
  --iris "/srv/vacant/data/processed/iris-2023/iris-2023.geojson" \
  --iris-sha256 "<sha256-independant-confirme>" \
  --arrond "/srv/vacant/data/processed/arrond-history/arrond-history.geojson" \
  --arrond-sha256 "<sha256-independant-confirme>" \
  --execute
```

Les `<...>` doivent être remplacés par de **vraies empreintes SHA-256 de 64 caractères** ; ne pas inventer de valeur ni recalculer l'attendu à partir d'une source non vérifiée. Sans `--execute`, le script ne crée aucun fichier. Il refuse d'écraser un dossier de release existant, vérifie les données et assure l'accès en lecture au conteneur Nginx. **Le script ne redémarre rien et ne déploie rien** : l'étape Docker/AgentCTL reste une opération distincte nécessitant une autorisation.

Contrôles supplémentaires avant toute autorisation de déploiement :

```sh
# Doit afficher zéro occurrence ; ne jamais publier un GeoJSON Apur privé.
find "/srv/vacant/releases/$sha/site" -name 'cell_*.geojson' -o -name 'apur-lab.geojson' -o -name 'manifest.json'
test ! -d "/srv/vacant/releases/$sha/site/data/apur-grid"
```

Si l'une de ces vérifications échoue, **bloquer la publication et inspecter la release** ; ne jamais la corriger à la main sur place. Les suites `tests/test_stage_reviewed_release.py` assurent la non-régression du garde-fou, y compris la présence de fichiers Apur privés ignorés dans un clone.
