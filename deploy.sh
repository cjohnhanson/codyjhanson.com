#!/bin/bash

if [ $(whoami) != 'root' ]; then
    echo "This script must be run as root!"
    exit 0
fi

git pull

service apache2 restart

