#!/bin/sh
read -p 'Commit Message: ' commitname
cd /Downloads/chatbot-master/
git add .
git commit -m $commitname
git push -u origin master

