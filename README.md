## init python3 env
apt install virtualenv
virtualenv -p /usr/bin/python3 pyenv
source pyenv/bin/activate

## init python lib
apt-get install libzmq3-dev gnupg-agent
pip install python-gnupg pyzmq

## setup configuration
cp config_example.py config.py

## pgp configuration
vim ~/.gnupg/gpg.conf
content：
use-agent
pinentry-mode loopback

generate gpg key
gpg --generate-key
gpg --list-keys
