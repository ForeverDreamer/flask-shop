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
docker compose -f docker-compose_dev.yml up -d
docker compose down
# Dockerfile的copy文件部分抽空改为volume映射，避免每次都要build
docker compose build

Second, enter container and add fake data
docker compose exec web sh
flask createdb
flask seed
flask seed --type product

# 网站地址
http://52.78.28.128:13145/

# 测试用户
aqiang
aqiang@gmail.com
123456
