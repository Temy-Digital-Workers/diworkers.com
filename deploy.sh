#!/bin/sh
# Rebuild and deploy diworkers.com to the hub droplet okko-fra1-temy-demo (161.35.25.14).
# nginx site: /etc/nginx/sites-enabled/diworkers (certbot-managed TLS), files: /opt/diworkers/web
set -e
cd "$(dirname "$0")"
python build.py
tar -cf - index.html privacy.html terms.html support.html 404.html style.css |
  ssh -i ~/.ssh/id_ed25519 root@161.35.25.14 'tar -xf - -C /opt/diworkers/web && chown -R root:root /opt/diworkers'
curl -s -o /dev/null -w "https://diworkers.com/ -> %{http_code}\n" https://diworkers.com/
