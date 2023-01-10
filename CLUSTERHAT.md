# Clusterhat Intial Hardware Setup  
There are several great articles out there worth noting and reading. Several were similar labour of love of tinkering. One of the original articles I first came across (referenced in CREDITS) was from github user abelperezok. (https://github.com/abelperezok)  

## Initial setup  
Warning: Do not put in the Micro SD Cards yet! You will need to flash images on them.  
- Follow assebly videos here: https://clusterhat.com/setup-assembly   
- Download OS images here: https://clusterctrl.com/setup-software  
 - Lite vs Full: One includes the Graphical User Interface. For my build I went with lite.  
 - CNAT vs CBRIDGE: 
  - CNAT keeps all clustered raspberri pi zeros isolated to a private network with the main Raspberri Pi.  
  - CBRIDGE connects each zero to the same network as the host Rasbperry PI sharing the main network interface.  
 - P1 - P5 Images: If you look at your cluster hat, right by the lights, each port is numbered. Each image is marked for which port it should be used with.  
- Burn the images using your favorite imaging method. My favorite to date is https://www.balena.io/etcher/.  
- Before removing the micro sd card, make sure you put the ssh file in the boot directory. Basically after burning the only drive that will show up from the sd card will be where you put the file. No information is required in the file, just an empty file called ssh. 
- Set your username and password file. There no more default credentials in raspbian. (https://www.raspberrypi.com/news/raspberry-pi-bullseye-update-april-2022/). You must create a file also in this boot drive called userconf with a username and password combo like username:encrypted- password. I went to a website like (https://www.cryptool.org/en/cto/openssl) to generate my first time user credentials and then immediately reset them on startup. Running echo 'clusterctrl' | openssl passwd -6 -stdin results in the encrypted output. My one time use userconf file contains this one line. pi:$6$jNGKpq7QHmtgKFDz$386OQaHRQ5TdqpJUhw2idkMaJ0Cc3jb6k/Ht4XG77Ffm1HYc9G.9uvBLyZXDueFvNM/2hvBh7XL/tH5zJNQxM1 which sets the credentials to pi:clusterctrl.  
  - You can also drop in a wpa_supplicant.conf file to handle all your wifi needs for the host cluster. Now that I think about it, if you are using Raspberry Pi Zero Ws you can do that as well for all nodes.  

- Plug in your micro sd cards and start up that bad boy. Its time to play!  
