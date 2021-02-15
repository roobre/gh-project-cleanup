#!/usr/bin/env sh

if [ -n "$CONFIG" ]; then
    echo "$CONFIG" > projects.yml
fi

if [ ! -e projects.yml ]; then
    echo "Cannot find projects.yml. Either set \$CONFIG to the yaml contents or mount a config file."
    exit 1
fi

/ghp-cleanup/ghp-cleanup.py projects.yml
