#!/bin/bash -x

#mkdir /Users/alex/hellodjango
#mkdir /Users/alex/downloads
#cd hellodjango
#"http://downloads.sourceforge.net/project/git-osx-installer/git-2.3.5-intel-universal-snow-leopard.dmg?r=http%3A%2F%2Fsourceforge.net%2Fp%2Fgit-osx-installer%2Factivity%3Fpage%3D0%26limit%3D100&ts=1447965480&use_mirror=freefr"
#
#sudo apt-get update
#sudo apt-get install -y git
#git init
#git pull https://github.com/alexbid/hellodjango.git
#
##Install Python
#cd /home/ubuntu/downloads
#wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
#tar -xvf Python-2.7.10.tgz
#cd /home/ubuntu/downloads/Python-2.7.10
#sudo ./configure
#sudo make
#sudo make install
#sudo cp /home/ubuntu/downloads/Python-2.7.10/setup.py /usr/local/bin/
#sudo cp /home/ubuntu/downloads/Python-2.7.10/setup.py /usr/local/lib/python2.7
#
#sudo python setup.py build
#sudo python setup.py install
#cd /home/ubuntu/hellodjango
#sudo python setup.py build
#sudo python setup.py install
##PATH=${PATH}:/usr/local/lib/python2.7
#export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python2.7"
#export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python2.7/dist-packages"

#sudo apt-get install -y python-pip
sudo easy_install pip
sudo easy_install lxml #apres avoir installe command line tool
#sudo apt-get install -y python-dev
#sudo apt-get install -y python-devel
#sudo apt-get install -y libpq-dev

#web scrapping requirement
#sudo apt-get install libxml2-dev libxslt-dev python-dev


#sudo apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
#sudo apt-get install -y libpq-dev python-dev libevent-dev libevent-devel python-devel build-essential 
#sudo apt-get install -y libcurl4-gnutls-dev libexpat1-dev gettext \ libz-dev libssl-dev

sudo pip install -y setuptools
sudo easy_install cython

#first install gfortran for lion cf. website scipy
sudo pip install numpy
sudo pip install scipy

#sudo pip install uwsgi
sudo pip install -r requirements.txt

#sudo rm -r /home/ubuntu/downloads

crontab < <(crontab -l ; echo "MAILTO=bidault@hotmail.fr")
crontab < <(crontab -l ; echo "@reboot python /home/ubuntu/hellodjango/run_all.py")
crontab < <(crontab -l ; echo "* * * * *  python /home/ubuntu/hellodjango/run_realtime.py")
crontab < <(crontab -l ; echo "0 16 * * *  python /home/ubuntu/hellodjango/run_eod.py")
crontab < <(crontab -l ; echo "0 13 * * *  python /home/ubuntu/hellodjango/run_eod.py")
crontab < <(crontab -l ; echo "45 6 * * 1-5  python /home/ubuntu/hellodjango/run_nav.py")