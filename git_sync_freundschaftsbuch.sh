#!/bin/bash

# dieses script führt einen pull-request aus falls es dem remote branch hinterherliegt!

# In den Projektordner wechseln
cd /home/zvowevan/Projects/Freundschaftsbuch || { echo "Verzeichnis nicht gefunden!"; exit 1; }

# Sicherstellen, dass man sich auf dem tamagotchi-server-Branch befindet
current_branch=$(git rev-parse --abbrev-ref HEAD)
commits_behind=$(git fetch && git rev-list --right-only --count HEAD...origin/tamagotchi-server)

# Den Git-Status überprüfen vom tamagotchi-server Branch
if [ "$current_branch" == "tamagotchi-server" ]; then
    echo "Das Freundschaftsbuch befindet sich auf dem korrekten Branch: $current_branch"
    # die änderungen des remote branches holen (aber noch nicht anwenden!!!)
    git fetch && echo "es wurde gefetched!"

    if [ "$commits_behind" -eq 0 ]; then
        echo "der branch ist synschorn zum remote branch"
    elif [ "$commits_behind" -gt 0 ]; then
        echo "der lokale branch liegt den remote zurück"
        git pull && echo "der pull wurde ausgeführt!"
    else
        echo "der lokale branch liegt dem remote vor"
	git reset --hard origin/tamagotchi-server && echo "überflüssige files wurden gelöscht!"
    fi

else
    echo "Das Freundschaftsbuch befindet sich auf dem falschen Branch: $current_branch"
fi

