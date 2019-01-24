#!/bin/bash

export LANG=en_GB.UTF-8


mkdir /docs/imported
mkdir /docs/Scan
touch /docs/state

. /appenv/bin/activate
/appenv/docsearch/web.py /docs

while true
do
  echo 'Hello World!'
  sleep 1
done
