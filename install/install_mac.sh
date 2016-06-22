#!/bin/bash -x

#HomeBrew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install wget

#cd hellodjango
#"http://downloads.sourceforge.net/project/git-osx-installer/git-2.3.5-intel-universal-snow-leopard.dmg?r=http%3A%2F%2Fsourceforge.net%2Fp%2Fgit-osx-installer%2Factivity%3Fpage%3D0%26limit%3D100&ts=1447965480&use_mirror=freefr"
#
#sudo apt-get update
#sudo apt-get install -y git
#git init
#git pull https://github.com/alexbid/hellodjango.git
#
##Install Python
cd /Users/alex/Downloads
wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
tar -xvf Python-2.7.10.tgz
cd /Users/alex/Downloads/Python-2.7.10
sudo ./configure
sudo make
sudo make install
sudo cp /Users/alex/Downloads/Python-2.7.10/setup.py /usr/local/bin/
sudo cp /Users/alex/Downloads/Python-2.7.10/setup.py /usr/local/lib/python2.7

sudo python setup.py build
sudo python setup.py install

curl -O https://svn.apache.org/repos/asf/oodt/tools/oodtsite.publisher/trunk/distribute_setup.py
sudo python distribute_setup.py
sudo rm distribute_setup.py

cd /Users/alex/hellodjango
PATH=${PATH}:/usr/local/lib/python2.7
export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python2.7"
export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python2.7/dist-packages"

#sudo apt-get install -y python-pip
sudo easy_install pip
sudo easy_install lxml #apres avoir installe command line tool

sudo apt-get install -y python-dev
#sudo apt-get install -y python-devel
#sudo apt-get install -y libpq-dev

#web scrapping requirement
#sudo apt-get install libxml2-dev libxslt-dev python-dev
#sudo apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2dev
#sudo apt-get install -y libpq-dev python-dev libevent-dev libevent-devel python-devel build-essential 
#sudo apt-get install -y libcurl4-gnutls-dev libexpat1-dev gettext \ libz-dev libssl-dev

sudo pip install setuptools
sudo easy_install cython

#first install gfortran for lion cf. website scipy
#sudo pip install numpy
#sudo pip install scipy
#sudo pip install uwsgi
#sudo pip install -r requirements.txt
#sudo rm -r /home/ubuntu/downloads

#crontab < <(crontab -l ; echo "MAILTO=bidault@hotmail.fr")
#crontab < <(crontab -l ; echo "@reboot python /home/ubuntu/hellodjango/run_all.py")
#crontab < <(crontab -l ; echo "* 6-20 * * 1-5  python /home/ubuntu/hellodjango/run_realtime.py ERROR")
#crontab < <(crontab -l ; echo "0 13,17,21 * * 1-5  python /home/ubuntu/hellodjango/run_eod.py")
#crontab < <(crontab -l ; echo "45 5 * * 1-5  python /home/ubuntu/hellodjango/run_nav.py")
#crontab < <(crontab -l ; echo "45 6 * * 1-5  python /home/ubuntu/hellodjango/run_all.py")
