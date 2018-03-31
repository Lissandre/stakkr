#!/bin/bash
set -e

echo "Cleaning the old virtualenv"
rm -rf *.egg-info ${PWD##*/}_stakkr __pycache__
echo ""

echo "Installing various python packages"
sudo apt-get -y install python3-pip python3-setuptools python3-virtualenv virtualenv > /dev/null
sudo pip3 install -q --upgrade pip > /dev/null
sudo pip3 install -q autoenv > /dev/null
echo ""

echo "If you want to automatically load the current virtualenvironment, check that you have in your .bashrc something like :"
echo '    echo "source `which activate.sh`"'
echo "then run "
echo "    # source ~/.bashrc"
echo ""

echo "Creating the virtualenv"
virtualenv -p /usr/bin/python3  ${PWD##*/}_stakkr > /dev/null
source ${PWD##*/}_stakkr/bin/activate > /dev/null
pip3 install -e . > /dev/null
stakkr-init
echo ""

echo "Deactivate and reactivate the virtualenv again by launching:"
echo "   # deactivate ; source  \${PWD##*/}_stakkr/bin/activate"
