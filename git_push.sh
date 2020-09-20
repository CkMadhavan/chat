#!/bin/sh
set -x
commitname=$(zenity --entry --text="Commit Message:") 
cd /Downloads/chatbot-master/
git add .
git commit -m $commitname
git push -f heroku master
git push -f -u origin master
zenity --info --text="Done Commiting" --title="Done Commiting" --ok-label="Close"

