mkdir /home/ubuntu/hellodjango
mkdir /home/ubuntu/downloads
cd hellodjango
sudo apt-get update
sudo apt-get install git
git init
git pull https://github.com/alexbid/hellodjango.git
sudo apt-get install -y libcurl4-gnutls-dev libexpat1-dev gettext \ libz-dev libssl-dev

#Install Python
sudo apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
cd /home/ubuntu/downloads
wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
tar -xvf Python-2.7.10.tgz
cd /home/ubuntu/downloads/Python-2.7.10
./configure
make
sudo make install
sudo cp ./Python-2.7.10/setup.py /usr/local/bin/python

cd /home/ubuntu/hellodjango
sudo apt-get install -y python-pip libpq-dev python-dev libevent-dev libevent-devel python-devel build-essential 
python setup.py build
sudo python setup.py install

sudo pip install --upgrade setuptools
sudo pip install uwsgi
sudo pip install -r requirements.txt

