#!/bin/sh
commitname=$(zenity --entry --text="Commit Message:") 
cd /Downloads/chatbot-master/
git add .
git commit -m $commitname
git push -u origin master

