#!/bin/sh
commitname=$(zenity --entry --text="Commit Message:") 
cd /Downloads/chatbot-master/
git add .
git commit -m $commitname
git push heroku master
git push -u origin master
zenity --info --text="Done Commiting" --title="Done Commiting" --ok-label="Close"

