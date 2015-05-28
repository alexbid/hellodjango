mkdir /home/ubuntu/hellodjango
mkdir /home/ubuntu/downloads
cd hellodjango
sudo apt-get install git
git init
git pull https://github.com/alexbid/hellodjango.git
apt-get install libcurl4-gnutls-dev libexpat1-dev gettext \ libz-dev libssl-dev

#Install Python
sudo apt-get install build-essential
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
cd /home/ubuntu/downloads
wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
tar -xvf Python-2.7.10.tgz
cd /home/ubuntu/downloads/Python-2.7.10
./configure
make
sudo make install

#sudo apt-get install python 2.7.10
sudo pip install -r requirements.txt

