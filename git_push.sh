#!/bin/sh
read name
git add .
git commit -m $name
git push -f heroku master
git push -f -u origin master
