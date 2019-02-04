import re
import os
# Input and output files
inputfile = open('bigip.conf','r',newline='\n')
outputfile = open('bigip.conf.clear', 'w', newline='\n')
# Global variables
config_tree = 'none'
sub_config_tree = str()
open_braces = list()
is_first_cert = True
is_first_key = True
is_first_chain = True
# Counters for stats
radius_counter = 0
cookie_counter = 0
cert_counter = 0
key_counter = 0
chain_counter = 0
iapp_variable_counter = 0
pass_counter = 0
other_passwords = 0
kerberos_counter = 0
ad_counter = 0
ldap_counter = 0
# Function that returns the value of a given config object
def value_of(config_item):
    return words[words.index(config_item) + 1]
# Function to change regular config value to a new value regardless
def ChangeConfig(config_item, newvalue):
    i = words.index(config_item) + 1
    words[i] = newvalue
    newline = ' '.join(words)
    return newline
# Function that validates the curly braces within a config item
def CheckBraces():
    if '{' in words:
        open_braces.append('{')
    if '}' in words:
        open_braces.pop()
        if not open_braces:
            config_tree == 'none'
# Function that comments out (#) the whole line
def CommentOut():
    words.insert(0,'#')
    newline = ' '.join(words)
    return newline
# Function that returns true if there is a match to a keyword
def matches(keyword, search_line):
    search_line = str(''.join(search_line))
    pattern = re.compile(r'(%s)+' % keyword)
    if pattern.search(search_line):
        return True
    else:
        return False
# The program starts here!
# Main loop for the program going through each line of the file
for line in inputfile:
    words = line.split()
    # This flags the start of radius/tacacs config
    if matches('radius', words) or matches('tacacs', words) and '{' in words:
        outputfile.write(line)
        open_braces.append('{')
        config_tree = 'radius'
        continue
    if 'ltm' in words and 'persistence' in words and 'cookie' in words and '{' in words:
        outputfile.write(line)
        open_braces.append('{')
        config_tree = 'cookie'
        continue
    if 'ltm' in words and 'profile' in words and 'client-ssl' in words and '{' in words:
        outputfile.write(line)
        open_braces.append('{')
        config_tree = 'client-ssl'
        continue
    if 'sys' in words and 'file' in words and 'ssl-cert' in words or 'ssl-key' in words and '{' in words:
        outputfile.write(CommentOut())
        outputfile.write('\n')
        open_braces.append('{')
        config_tree = 'comment-out'
        continue
    if 'variables' in words and '{' in words:
        outputfile.write(line)
        open_braces.append('{')
        config_tree = 'iapp'
        continue
    if 'sys' in words and 'diags' in words and 'ihealth' in words and '{' in words:
        outputfile.write(line)
        open_braces.append('{')
        config_tree = 'ihealth'
        continue
    if 'ltm' in words and 'monitor' in words and '{' in words:
        outputfile.write(line)
        open_braces.append('{')
        config_tree = 'monitor'
        continue
    if 'ltm' in words and 'profile' in words and 'ocsp-stapling-params' in words and '{' in words:
        outputfile.write(CommentOut())
        outputfile.write('\n')
        open_braces.append('{')
        config_tree = 'comment-out'
        continue
    if 'sys' in words and 'crypto' in words and 'cert-validator' in words and 'ocsp' in words and '{' in words:
        outputfile.write(CommentOut())
        outputfile.write('\n')
        open_braces.append('{')
        config_tree = 'comment-out'
        continue
    if 'apm' in words and 'sso' in words and 'kerberos' in words and '{' in words:
        outputfile.write(line)
        open_braces.append('{')
        config_tree = 'kerberos'
        continue
    if 'apm' in words and 'aaa' in words and 'active-directory' in words and '{' in words:
        outputfile.write(line)
        open_braces.append('{')
        config_tree = 'active-directory'
        continue
    if 'auth' in words and 'ldap' in words and '{' in words:
        outputfile.write(line)
        open_braces.append('{')
        config_tree = 'ldap'
        continue   
    # This is the 2nd part of the program
    #
    # This is the start of radius/tacacs loop
    if len(open_braces) > 0 and config_tree == 'radius':
        CheckBraces()
        if 'secret' in words and value_of('secret')[:3] == '$M$':
            outputfile.write('    ' + ChangeConfig('secret', '123ratatata'))
            outputfile.write('\n')
            radius_counter += 1
        else:
            outputfile.write(line)
    # This is the start of cookie loop
    elif len(open_braces) > 0 and config_tree == 'cookie':
        CheckBraces()
        if 'cookie-encryption-passphrase' in words and value_of('cookie-encryption-passphrase')[:3] == '$M$':
            outputfile.write('    ' + ChangeConfig('cookie-encryption-passphrase', '123ratatata'))
            outputfile.write('\n')
            cookie_counter += 1
        else:
            outputfile.write(line)
    # This is the start of client-ssl loop
    elif len(open_braces) > 0 and config_tree == 'client-ssl':
        CheckBraces()
        if 'cert' in words and ('default.crt' or '/Common/default.crt') not in words:
            if is_first_cert == True:
                outputfile.write('    ' + ChangeConfig('cert', '/Common/default.crt'))
                outputfile.write('\n')
                is_first_cert = False
                cert_counter += 1
            else:
                outputfile.write('        ' + ChangeConfig('cert', '/Common/default.crt'))
                outputfile.write('\n')
                is_first_cert = True
        elif 'key' in words and ('default.key' or '/Common/default.key') not in words:
            if is_first_key == True:
                outputfile.write('        ' + ChangeConfig('key', '/Common/default.key'))
                outputfile.write('\n')
                is_first_key = False
                key_counter += 1
            else:
                outputfile.write('    ' + ChangeConfig('key', '/Common/default.key'))
                outputfile.write('\n')
                is_first_key = True
        elif 'chain' in words and 'none' not in words:
            if is_first_chain == True:
                outputfile.write('           ' + ChangeConfig('chain', 'none'))
                outputfile.write('\n')
                is_first_chain = False
                chain_counter += 1
            else:
                outputfile.write('    ' + ChangeConfig('chain', 'none'))
                outputfile.write('\n')
                is_first_chain = True
        elif 'ca-file' in words and 'none' not in words:
            outputfile.write('           ' + ChangeConfig('ca-file', 'none'))
            outputfile.write('\n')
            cert_counter += 1
        elif 'notify-cert-status-to-virtual-server' in words and 'enabled' in words:
            outputfile.write('    ' + ChangeConfig('notify-cert-status-to-virtual-server', 'disabled'))
        elif 'ocsp-stapling' in words and 'enabled' in words:
            outputfile.write('    ' + ChangeConfig('ocsp-stapling', 'disabled'))
        elif 'passphrase' in words and 'none' not in words:
            outputfile.write('    ' + ChangeConfig('passphrase', 'none'))
            outputfile.write('\n')
            pass_counter += 1
        else:
            outputfile.write(line)
    # This comments out sys file ssl-cert, ssl-key line and ocsp stapling
    elif len(open_braces) > 0 and config_tree == 'comment-out':
        CheckBraces()
        outputfile.write('    ' + CommentOut())
        outputfile.write('\n')
    # This is the start of iApps variables config line
    elif len(open_braces) > 0 and config_tree == 'iapp':
        CheckBraces()
        if 'value' in words and value_of('value')[:3] == '$M$':
            outputfile.write('            ' + ChangeConfig('value', '123ratatata'))
            outputfile.write('\n')
            iapp_variable_counter += 1
        else:
            outputfile.write(line)
    # This is the start of ihealth password line
    elif len(open_braces) > 0 and config_tree == 'ihealth':
        CheckBraces()
        if 'password' in words and value_of('password')[:3] == '$M$':
            outputfile.write('    ' + ChangeConfig('password', '123ratatata'))
            outputfile.write('\n')
            other_passwords += 1
        else:
            outputfile.write(line)
    elif len(open_braces) > 0 and config_tree == 'monitor':
        CheckBraces()
        if 'password' in words and value_of('password')[:3] == '$M$':
            outputfile.write('    ' + ChangeConfig('password', '123ratatata'))
            outputfile.write('\n')
            other_passwords += 1
        elif 'cert' in words and 'none' not in words:
            outputfile.write('    ' + ChangeConfig('cert', '/Common/default.crt'))
            outputfile.write('\n')
            cert_counter += 1
        elif 'key' in words and 'none' not in words:
            outputfile.write('    ' + ChangeConfig('key', '/Common/default.key'))
            outputfile.write('\n')
            key_counter += 1
        else:
            outputfile.write(line)
    # This is the start of kerberos password line
    elif len(open_braces) > 0 and config_tree == 'kerberos':
        CheckBraces()
        if 'account-password' in words and value_of('account-password')[:3] == '$M$':
            outputfile.write('    ' + ChangeConfig('account-password', '123ratatata'))
            outputfile.write('\n')
            kerberos_counter += 1
        else:
            outputfile.write(line)
    # This is the start of active-directory password line
    elif len(open_braces) > 0 and config_tree == 'active-directory':
        CheckBraces()
        if 'admin-encrypted-password' in words and value_of('admin-encrypted-password')[:3] == '$M$':
            outputfile.write('    ' + ChangeConfig('admin-encrypted-password', '123ratatata'))
            outputfile.write('\n')
            ad_counter += 1
        else:
            outputfile.write(line)
    elif len(open_braces) > 0 and config_tree == 'ldap':
        CheckBraces()
        if 'bind-pw' in words and value_of('bind-pw')[:3] == '$M$':
            outputfile.write('    ' + ChangeConfig('bind-pw', '123ratatata'))
            outputfile.write('\n')
            ldap_counter += 1
        else:
            outputfile.write(line)
    else:
        outputfile.write(line)
inputfile.close()
outputfile.close()
print(str(radius_counter) + ' radius secret(s) cleared')
print(str(kerberos_counter) + ' kerberos secret(s) cleared')
print(str(ad_counter) + ' active-directory passphrase(s) cleared')
print(str(ldap_counter) + ' ldap passphrase(s) cleared')
print(str(cookie_counter) + ' cookie profile(s) with passphrase cleared')
print(str(cert_counter) + ' certificates changed to default.crt')
print(str(key_counter) + ' keys changed to default.key')
print(str(chain_counter) + ' chains changed to none')
print(str(pass_counter) + ' passphrases cleared')
print(str(other_passwords) + ' other passwords cleared')
