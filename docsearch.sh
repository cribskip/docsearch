#!/bin/bash
cd /home/sascha/Dokumente

function finish {
 kill $!
}
trap finish EXIT

# Web-App
/usr/share/docsearch/web.py $(pwd) &
