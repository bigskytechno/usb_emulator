#!/usr/bin/env bash

sudo apt-get update
audo apt-get upgrade

mkdir usb_mirror
sudo mkdir /mnt/usb_emu
sudo dd if=/dev/zero of=/piusb.bin bs=1M count=2048 # Change these values for different USB size.
sudo mkdosfs /piusb.bin

sudo apt-get install python3-pip
sudo pip3 install dropbox

echo "/piusb.bin /mnt/usb_emu vfat users,umask=000,noauto 0 2" >> /etc/fstab

sudo sed -i -e '$i sudo modprobe g_mass_storage file=/piusb.bin stall=0 removable=1 ro=0\n' /etc/rc.local
sudo sed -i -e '$i sudo python3 usb_controller.py &\n' /etc/rc.local

sudo modprobe g_mass_storage file=/piusb.bin stall=0 removable=1 ro=0
sudo python3 usb_controller.py &