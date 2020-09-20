#!/bin/sh
read name
cd /Downloads/chatbot-master/
git add .
git commit -m name
git push -f heroku master
git push -f -u origin master
zenity --info --text="Done Commiting" --title="Done Commiting" --ok-label="Close"

