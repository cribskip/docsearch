#!/bin/bash

export LANG=en_GB.UTF-8

. /appenv/bin/activate
/appenv/docsearch/web.py /docs

while true
do
  echo 'Hello World!'
  sleep 1
done
