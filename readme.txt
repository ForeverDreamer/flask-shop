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
# Dockerfile的copy文件部分抽空改为volume映射，避免每次都要彻底删除再拷贝文件，再build
docker compose build

Second, enter container and add fake data
docker compose exec web sh
flask createdb
flask seed
flask seed --type product

# 网站地址
http://43.202.0.14/

# 测试用户
eshop
eshop@gmail.com
123456


# Localization support
# First, in the translation directory, check the babel.cfg
cd translations

# If you want to add a new language support, like zh-CN:
# create a new lang file
pybabel init -i messages.pot -d . -l zh_Hans_CN
# modify the zh_CN/messages.po file to your own language
# compile the translations
pybabel compile -d .

# If you modify the source code, and need to update the exist translations:
# update the messages.pot
pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot ../
# update the translations
pybabel update -i messages.pot -d . -l zh_Hans_CN
# then translate it and compile it