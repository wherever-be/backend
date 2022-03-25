#!/bin/sh
sudo apt update
sudo apt upgrade -y
sudo hostname backend

sudo snap install core
sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot certonly --standalone -d wherever.be,api.wherever.be

sudo apt install python3-pip -y
source ~/.bashrc
pip3 install poetry
poetry config virtualenvs.in-project true
poetry install
