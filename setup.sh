#! /bin/bash

#check for root
UID=$(id -u)
if [ x$UID != x0 ] 
then
    #Beware of how you compose the command
    printf -v cmd_str '%q ' "$0" "$@"
    exec sudo su -c "$cmd_str"
fi

# Show errors
function catch_errors() {
   echo "Error";
}

trap catch_errors ERR;

# Make sure only root can run the script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Global variables
HOME_PI="/home/pi"
cd $HOME_PI/radio_exea

# Verify that git works fine
rc=$?
if [[ $rc != 0 ]] ; then
    exit $rc
fi

echo "Updating system..."
apt-get -y update

echo "Installing some tools..."
apt-get install -y curl libsdl2-mixer-2.0-0 libsdl2-image-2.0-0 libsdl2-2.0-0
apt-get install -y python3-vlc python3-dev python3-setuptools python3-pip i2c-tools
apt-get install -y python3-pygame

echo "Installing dependencies"
pip3 install -r requirements.txt

rc=$?
if [[ $rc != 0 ]] ; then
    exit $rc
fi

echo "Copying files for automatic initialization of software..."
cp $HOME_PI/radio_exea/scripts/player /etc/systemd/system/player.service

# Verify command
rc=$?
if [[ $rc != 0 ]] ; then
    exit $rc
fi

# Permisions of the file
systemctl daemon-reload
systemctl enable player.service
systemctl start player.service

chown -Rf pi $HOME_PI/*

echo "Finishing setup"
