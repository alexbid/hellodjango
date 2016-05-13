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

sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran
sudo pip install -y setuptools
sudo apt-get install python-scipy
sudo apt-get install python-pandas

#sudo pip install
sudo pip install -r requirements.txt

crontab < <(crontab -l ; echo "MAILTO=pi")
crontab < <(crontab -l ; echo "@reboot python "$rootDir"/hellodjango/batchs/run_all.py")
crontab < <(crontab -l ; echo "@reboot sleep 40; sudo mount -all")
crontab < <(crontab -l ; echo "* 6-20 * * 1-5  python "$rootDir"/hellodjango/batchs/run_realtime.py")
crontab < <(crontab -l ; echo "0 13,17,21 * * 1-5  python "$rootDir"/hellodjango/batchs/run_eod.py")
crontab < <(crontab -l ; echo "45 5 * * 1-5  python "$rootDir"/hellodjango/batchs/run_nav.py")
crontab < <(crontab -l ; echo "45 6 * * 1-5  python "$rootDir"/hellodjango/batchs/run_all.py")
crontab < <(crontab -l ; echo "0 6 * * * find "$rootDir"/Maildir/cur/ -type f -ctime +1 -exec rm -f {} \;")
crontab < <(crontab -l ; echo "0 6 * * * find "$rootDir"/Maildir/new/ -type f -ctime +1 -exec rm -f {} \;")




