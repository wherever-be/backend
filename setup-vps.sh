#!/bin/sh
sudo apt update
sudo apt upgrade -y
sudo hostname backend
sudo apt install python3-pip -y
pip3 install poetry
poetry config virtualenvs.in-project true
git clone https://github.com/wherever-be/backend.git
cd backend
poetry install
