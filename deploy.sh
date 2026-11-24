#!/bin/sh
# Rebuild and deploy diworkers.com to the hub droplet okko-fra1-temy-demo (161.35.25.14).
# nginx site: /etc/nginx/sites-enabled/diworkers (certbot-managed TLS), files: /opt/diworkers/web
set -e
cd "$(dirname "$0")"
python build.py
tar -cf - --exclude=.git --exclude=build.py --exclude=deploy.sh --exclude='*.md' . |
  ssh -i ~/.ssh/id_ed25519 root@161.35.25.14 'rm -rf /opt/diworkers/web.new && mkdir -p /opt/diworkers/web.new && tar -xf - -C /opt/diworkers/web.new && chown -R root:root /opt/diworkers/web.new && find /opt/diworkers/web.new -type d -exec chmod 755 {} + && find /opt/diworkers/web.new -type f -exec chmod 644 {} + && rm -rf /opt/diworkers/web.old && mv /opt/diworkers/web /opt/diworkers/web.old && mv /opt/diworkers/web.new /opt/diworkers/web'
for u in / /workers.html /workers/ap-clerk.html /how-it-works.html /assets/video/flow-ap-clerk.mp4 /assets/img/temy-logo.svg; do
  curl -s -o /dev/null -w "https://diworkers.com$u -> %{http_code}\n" "https://diworkers.com$u"; done
