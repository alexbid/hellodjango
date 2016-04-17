#!/bin/bash -x

mkdir /home/ubuntu/hellodjango
mkdir /home/ubuntu/downloads
cd hellodjango
sudo apt-get update
sudo apt-get install -y git
git init
git pull https://github.com/alexbid/hellodjango.git

#Install Python
cd /home/ubuntu/downloads
wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
tar -xvf Python-2.7.10.tgz
cd /home/ubuntu/downloads/Python-2.7.10
sudo ./configure
sudo make
sudo make install
sudo cp /home/ubuntu/downloads/Python-2.7.10/setup.py /usr/local/bin/
sudo cp /home/ubuntu/downloads/Python-2.7.10/setup.py /usr/local/lib/python2.7

cd /home/ubuntu/hellodjango
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

#sudo pip install uwsgi
sudo pip install -r requirements.txt

#sudo rm -r /home/ubuntu/downloads

crontab < <(crontab -l ; echo "MAILTO=bidault@hotmail.fr")
<<<<<<< HEAD:install_machine.sh
crontab < <(crontab -l ; echo "@reboot python /home/ubuntu/hellodjango/run_all.py")
crontab < <(crontab -l ; echo "* * * * 1-5  python /home/ubuntu/hellodjango/run_realtime.py")
crontab < <(crontab -l ; echo "15 12,16,18,20,21 * * 1-5  python /home/ubuntu/hellodjango/run_eod.py")
crontab < <(crontab -l ; echo "45 6 * * 1-5  python /home/ubuntu/hellodjango/run_nav.py")
crontab < <(crontab -l ; echo "45 6 * * 1-5 python /home/ubuntu/hellodjango/run_all.py")
=======
crontab < <(crontab -l ; echo "@reboot python /home/ubuntu/hellodjango/batchs/run_all.py")
crontab < <(crontab -l ; echo "* * * * *  python /home/ubuntu/hellodjango/batchs/run_realtime.py")
crontab < <(crontab -l ; echo "0 13-16 * * *  python /home/ubuntu/hellodjango/batchs/run_eod.py")
crontab < <(crontab -l ; echo "45 6 * * 1-5  python /home/ubuntu/hellodjango/batchs/run_nav.py")
crontab < <(crontab -l ; echo "45 7 * * 1-5  python /home/ubuntu/hellodjango/batchs/run_all.py")


>>>>>>> 5905fc4c205993fe4d6f68bc408da96af093ecb7:install/install_machine.sh


