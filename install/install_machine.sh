#!/bin/bash -x

rootDir=$1
rootDir=/home/pi

mkdir $rootDir/hellodjango
mkdir $rootDir/downloads
cd $rootDir/hellodjango
sudo apt-get update
sudo apt-get install -y git
git init
git pull https://github.com/alexbid/hellodjango.git

#Install Python
cd $rootDir/downloads
wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
tar -xvf Python-2.7.10.tgz
cd $rootDir/downloads/Python-2.7.10
sudo ./configure
sudo make
sudo make install
sudo cp $rootDir/downloads/Python-2.7.10/setup.py /usr/local/bin/
sudo cp $rootDir/downloads/Python-2.7.10/setup.py /usr/local/lib/python2.7

cd $rootDir/hellodjango
sudo python setup.py build
sudo python setup.py install
#PATH=${PATH}:/usr/local/lib/python2.7
export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python2.7"
export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python2.7/dist-packages"


sudo apt-get install -y python-pip
sudo apt-get install -y python-dev
sudo apt-get install -y python-devel
sudo apt-get install -y libpq-dev

#web scrapping requirement
sudo apt-get install libxml2-dev libxslt-dev python-dev
sudo pip install lxml

#sudo apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
#sudo apt-get install -y libpq-dev python-dev libevent-dev libevent-devel python-devel build-essential 
#sudo apt-get install -y libcurl4-gnutls-dev libexpat1-dev gettext \ libz-dev libssl-dev

sudo pip install -y setuptools
sudo apt-get install python-scipy
sudo apt-get install python-pandas

#sudo pip install uwsgi
sudo pip install -r requirements.txt

#sudo rm -r /home/ubuntu/downloads

crontab < <(crontab -l ; echo "MAILTO=bidault@hotmail.fr")
crontab < <(crontab -l ; echo "@reboot python "$rootDir"/hellodjango/batchs/run_all.py")
crontab < <(crontab -l ; echo "* * * * *  python "$rootDir"/hellodjango/batchs/run_realtime.py")
crontab < <(crontab -l ; echo "0 13-16 * * *  python "$rootDir"/hellodjango/batchs/run_eod.py")
crontab < <(crontab -l ; echo "45 6 * * 1-5  python "$rootDir"/hellodjango/batchs/run_nav.py")
crontab < <(crontab -l ; echo "45 7 * * 1-5  python "$rootDir"/hellodjango/batchs/run_all.py")




