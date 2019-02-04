# F5-scripts

A couple of scripts that were useful for my troubleshooting.

# ./remove-big-ip-passphrases-python2.py
14 radius secret(s) cleared
1 kerberos secret(s) cleared
1 active-directory passphrase(s) cleared
13 cookie profile(s) with passphrase cleared
45 certificates changed to default.crt
45 keys changed to default.key
24 chains changed to none
38 passphrases cleared
5 other passwords cleared
# ls
bigip.conf  bigip.conf.clear  clear_passphrase-v2.py
# mv bigip.conf bigip.conf.backup
# mv bigip.conf.clear bigip.conf
# tmsh load sys config

$ ./sslcounter.py
Invalid usage. Usage:
./sslcounter.py [--src-ip or -s, --dst-ip or -d] [file path]
rodrigo@rodrigo-seattle-lab:~/rod$ ./sslcounter.py -s log/ltm.1
IP address: 172.96.0.81%2551, SSL Handshake Failures: 1
IP address: 192.168.246.173%2552, SSL Handshake Failures: 22
IP address: 192.168.218.14%2551, SSL Handshake Failures: 1
IP address: 220.0.16.239%2551, SSL Handshake Failures: 47451
IP address: 172.86.0.82%2551, SSL Handshake Failures: 1
IP address: 192.168.246.168%2552, SSL Handshake Failures: 19332
IP address: 192.168.218.16%2551, SSL Handshake Failures: 1
IP address: 220.2.147.73%2551, SSL Handshake Failures: 8
IP address: 172.87.0.83%2551, SSL Handshake Failures: 4
IP address: 192.168.246.178%2552, SSL Handshake Failures: 18486
IP address: 192.168.246.183%2552, SSL Handshake Failures: 18424
IP address: 192.168.246.188%2552, SSL Handshake Failures: 17468
IP address: 172.87.0.82%2551, SSL Handshake Failures: 1
IP address: 172.86.0.84%2551, SSL Handshake Failures: 3
IP address: 172.87.0.84%2551, SSL Handshake Failures: 1
IP address: 220.0.16.240%2551, SSL Handshake Failures: 47314
IP address: 192.168.246.193%2552, SSL Handshake Failures: 18537
rodrigo@rodrigo-seattle-lab:~/rod$ ./sslcounter.py -d log/ltm.1
IP address: 220.110.16.20%2551, SSL Handshake Failures: 11
IP address: 220.110.160.11%2552, SSL Handshake Failures: 92247
IP address: 220.110.16.11%2551, SSL Handshake Failures: 2
IP address: 220.110.16.12%2551, SSL Handshake Failures: 94773
IP address: 220.110.164.16%2552, SSL Handshake Failures: 22
