# VACANT — déploiement statique sur le VPS personnel

Le domaine `vacant.kiwinokoto.fr` résout vers le VPS personnel. Traefik v3 est déjà actif avec le réseau externe `traefik_network` et le résolveur TLS `letsencrypt`. Aucune modification de Traefik ni d'un autre service n'est nécessaire.

1. Retenir un commit vérifié de `Kiwinokoto/vacant` (idéalement fusionné dans `main`).
2. Construire une **release immuable** dans `/srv/vacant/releases/<commit>/site/` en copiant `site/*`, et `docs/` comme documentation publique. Ne jamais y mettre `raw/` ou des données personnelles.
3. Copier uniquement `/srv/vacant/data/processed/iris-2023/iris-2023.geojson` dans `site/data/iris-2023.geojson` et comparer son SHA-256 à la validation géographique.
4. Acquérir les leases AgentCTL `deploy:vps-personal/vacant`, `service:vacant` et `host:vps-personal/docker`, puis vérifier la configuration : `VACANT_WEBROOT=/srv/vacant/releases/<commit>/site docker compose -f deploy/compose.yml -p vacant config`.
5. Démarrer uniquement le nouveau conteneur VACANT : même variable et `docker compose -f deploy/compose.yml -p vacant up -d`.
6. Contrôler la réponse HTTP→HTTPS, le certificat (pas le certificat par défaut de Traefik), l'HTTP 200 de la page et du GeoJSON, et le chargement de l'API Paris Data.

Le service est statique, sans base ni accès au répertoire des données brutes. **Ne jamais faire de déploiement non verrouillé ou forcé.** Les observations Insee ne permettent aucune conclusion sur un logement ou un immeuble individuel.


Pour la couche historique des arrondissements, ajouter seulement le dérivé validé /srv/vacant/data/processed/arrond-history/arrond-history.geojson sous site/data/arrond-history.geojson, avec contrôle SHA-256. Ne pas monter les Excel/Parquet bruts ni leurs répertoires.
