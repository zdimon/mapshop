Локальный деплой
----------------

apt-get install python-virtualenv

virtualenv mpashop_ve

cd mapshop_ve

source ./bin/activate

git clone git@github.com:zdimon/mapshop.github

cd mshop

pip install -r requirements.txt

./manage.py syncdb

./manage.py migrate




