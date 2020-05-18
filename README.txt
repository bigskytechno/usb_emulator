Quick and Important Definition:

|  ________ Pi Zero ____     ____   |
\__\______/_________\__/_____\__/___/
   Mini HDMI        DATA     PWR
                    Micro USB Ports

Setup
-----

1. Go to https://www.dropbox.com/developers/apps/create.
2. Click: Dropbox API -> Full Dropbox
3. Type in what you want to call the app ('USB Cloud' is fine) and click 'Create app'
4. Click the 'Generate' button under the OAuth2 heading and copy the text that appears.
5. Paste it on line 7 of the usb_controller.py script where it says to replace with your access token.
6. Take the MicroSD card out of the Raspberry Pi and open it on your computer (use adapter or whatever).
7. Create a file on the drive/partition called boot (easiest to do on a Linux PC, I don't know if Windows can handle multiple partition on one remvable device).
8. Name it 'wpa_supplicant.conf' and paste the following lines in:

country=AU
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
	ssid="REPLACE WITH NETWORK NAME"
	psk="REPLACE WITH NETWORK PASSWORD"
	key_mgmt=WPA-PSK
	scan_ssid=1
}

9. Return the MicroSD and plug in the Pi (data port). SFTP in (username: 'pi' password: 'raspberry') and drop in your edited usb_controller.py.

It now should be working as a USB Cloud. Feel free to contact me at hamishwhcox@gmail.com for any problems.

If you need to setup a new Pi to do this, flash Raspbian Stretch Lite onto the MicroSD and complete steps 6 to 8 before continuing onto the steps below.

10. Create a blank file called 'ssh' (no extension) on the boot partition.
11. Add the line 'dtoverlay=dwc2' to config.txt in the boot partition. Add 'modules-load=dwc2,g_mass_storage' after 'rootwait' in cmdline.txt.
    Make sure to include spaces between it and any other parts (i.e. 'rootwait{SPACE}modules-load=dwc2,g_ether{SPACE}quiet').
12. Return the MicroSD to the Pi.
11. Plug in the Pi (data port).
12. SFTP into pi@raspberrypi or pi@raspberrypi.local, password 'raspberry' (default). If neither work, use its IP address (use your router to find it).
13. Drop the setup.sh and edited usb_controller.py into the pi home directory (/home/pi/) and run 'sudo bash setup.sh'.
14. It should now be working.

General Use
-----------

Any files put onto the Raspberry Pi USB while it is running will be uploaded to Dropbox under the folder 'usb_cloud'.
While it can detect file deletion, creation, modification and renaming, it cannot handle folder renaming
(only while there are items inside the folder, which will be deleted, the folder itself will be fine)
and moving of folders (untested, maybe maybe not).

Note: Do not unplug the Pi once plugged in. This risks filesystem corruption and files may be unrecoverable. When use is not needed, SSH into the Pi and use 'sudo shutdown -h now'.
      If you need to power down the machine it is connected to (this would cut the power, risking corruption), your are able to power it through two different ports.
      Modify a Micro USB cable like so: Cut the power wires. Only preserve the Data +/- wires.
      Connect this Micro USB cable to the USB data port (to computer/machine) and a second unmodifed one to the USB power port (to a 5V power supply). This way the Pi is not overloaded with two much power.