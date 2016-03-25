#!/bin/bash -x

sudo apt-get install -y python-dev
sudo apt-get install -y python-devel
sudo apt-get install -y libpq-dev

#web scrapping requirement
sudo apt-get install libxml2-dev libxslt-dev python-dev
sudo apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2dev
sudo apt-get install -y libpq-dev python-dev libevent-dev libevent-devel python-devel build-essential
sudo apt-get install -y libcurl4-gnutls-dev libexpat1-dev gettext \ libz-dev libssl-dev

sudo pip install setuptools
sudo easy_install cython

#first install gfortran for lion cf. website scipy
sudo pip install numpy
sudo pip install scipy
sudo pip install uwsgi
sudo pip install -r requirements.txt
