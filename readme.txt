How to install project?

Clone this wiki locally
https://github.com/hjlarry/flask-shop.wiki.git
Use python virtual environment
First, Clone and Install dependence

git clone https://github.com/hjlarry/flask-shop.git

DROP DATABASE IF EXISTS `eshop`;
CREATE DATABASE `eshop`;

# modify the flaskshop/setting.py
flask createdb
# create the fake data and admin user for experience
flask seed
flask run


Use Docker
First, Build image and run in background
docker compose up -d

Second, enter container and add fake data
docker compose exec web sh
flask createdb
flask seed

# 网站地址
http://52.78.28.128:13145/