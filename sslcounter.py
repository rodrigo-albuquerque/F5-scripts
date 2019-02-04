#!/usr/bin/python
 
import sys
import re
 
# Function that returns a dictionary of IP addresses and SSL handshake errors
def gen_stats(file_path, regex_group):
    '''
    pattern matches different groups in the same line:
    1 = SSL Handshake failed
    2 = src IP address
    3 = src port
    4 = dst IP address
    5 = dst port
    '''
    pattern = re.compile(r"(SSL Handshake failed).+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.+):(\d+).+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.+):(\d+)")
    # dict to keep IP:counter
    counter = dict()
    with open(file_path) as file:
        for line in file:
            match = pattern.search(line)
            if match is not None:
                arg = match.group(regex_group)
                try:
                    if counter[arg] is not None:
                        counter[arg] += 1
                except KeyError:
                    counter[arg] = 1
    return counter
# Function to iterate and print dictionary from gen_stats function
def print_stats(file_path, regex_group):
    for k,v in gen_stats(file_path, regex_group).items():
        print('IP address: {}, SSL Handshake Failures: {}'.format(k,v))
 
# Main program
acceptable_arguments = { '--src-ip' : 2,
                        '-s' : 2 ,
                        '--src-ip-port' : 3,
                        '-sp' : 3,
                        '--dst-ip' : 4,
                        '-d' : 4,
                        '--dst-ip-port' : 5,
                        '-dp' : 5,
                        }
if len(sys.argv) == 3:
    if sys.argv[1] in acceptable_arguments.keys():
        print_stats(sys.argv[2], acceptable_arguments[sys.argv[1]])
    else:
        print('Invalid usage. Usage: ')
        print('{} [--src-ip or -s, --dst-ip or -d] [file path]'.format(sys.argv[0]))
else:
    print('Invalid usage. Usage: ')
    print('{} [--src-ip or -s, --dst-ip or -d] [file path]'.format(sys.argv[0]))
