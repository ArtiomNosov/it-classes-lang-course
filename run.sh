#!/bin/bash
# Запускает хостинг приложения
cd /var/www/it-classes-lang-course
sudo apt install python3-flask
sudo apt install python3-bcrypt
sudo apt install gunicorn

sudo systemctl start docker
gunicorn -w 4 -b 0.0.0.0:5000 run:app