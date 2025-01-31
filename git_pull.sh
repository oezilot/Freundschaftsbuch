#!/bin/bash

# Log den Empfang des Webhooks
echo "Webhook empfangen: $(date)" >> /home/zoef/Projects/Freundschaftsbuch/logs/git_pull.log

# Wechsle ins Projektverzeichnis
cd /home/zoef/Projects/Freundschaftsbuch || exit 1

# Pull die Änderungen vom Branch tamagotchi-server
git pull origin Poseidon >> /home/zoef/Projects/Freundschaftsbuch/logs/git_pull.log 2>&1

# Neustart des Dienstes
sudo systemctl restart freundschaftsbuch.service >> /home/zoef/Projects/Freundschaftsbuch/logs/git_pull.log 2>&1

# Logge den Abschluss
echo "Deployment abgeschlossen: $(date)" >> /home/zoef/Projects/Freundschaftsbuch/logs/git_pull.log
