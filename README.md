# cluster-hat-automation
A small pet project for the cluster hat. Several utilities and some instructions are planned. Come check it out!
  
## But why?
There are a few different interesting articles regarding this but none seem to be updated to include the new Rasipian authentication requirements. Also, I dont think I've seen one that works with h3s so I figure while I tinker I should record.  
  
## RPI Locator
- Must have docker installed  

TLDR run make build find-raspberries  

### Current output:  
A few statements and IP address / Mac address of every found raspberry pi.   

### Interesting facts:  
I've parsed the IEEE OUI list of all companies from the actual site. This means as raspberry pis are added or updated to including new OUIs, this system should automatically pick that up.  

One of the things I loved was a java based GUI that would search my local network for all raspberri pis and give me the IP addreses. Last I checked that projects is semi abandoned. The first thing I need to do after install is find my IP addresses. This is because just about in all cases I do not want to connect a screen, keyboard, and mouse to my raspberry pi, ever.   
  
Originally I started writing this tool in GOlang. While I could gather information and calculate the network cidr range, I could not find any great packages for network scanning or arping or any great tools to query a host to gather its mac address. In the future I would like to port this over but I chose to move over to Python.  
  
This Python edition ended up working pretty well up until to the last inch. In Python, there is no great way to get information about a networking card (e.g. IP address, default route, Mac address, Subnetmask). After pouring over dozens of articles, probably hundreds, I could find no existing packages to import that would help. I found an okay method of using bash commands to pull the required information. Rather than use a VENV, I opted to leverage a host network bridged docker container to ensure the same linux version was used and produces the same output every time for parsing.   

