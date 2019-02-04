#!/usr/bin/python
 
import commands
import time
import re
 
# 300 seconds = 5 minutes
MAX_TIME_RUNNING = 600
start = time.time()
 
def get_d_processes():
    '''
    Returns a List of Uninterrupted Processes.
    Each Uninterrupted Process is a List containing state, pid and cmd
    '''
    output = commands.getoutput("ps -eo state,pid,cmd | grep '^D'").split('\n')
    for index, process in enumerate(output):
        output[index] = process.strip().split(' ', 2)
        output[index] = re.sub(r' +', ' ', ' '.join(output[index])).split(' ', 2)
    return output
 
def get_rw_io_by_pid(pid):
    '''
    Returns a tuple with read_bytes and write_bytes
    '''
    return commands.getoutput('cat /proc/%s/io' % pid)
 
def lsof(pid):
    '''
    Returns
    '''
    return commands.getoutput('lsof -p %s' % pid)
 
while True:
    top = open('/shared/tmp/top.txt', 'ab')
    top.write('--------------------------\n')
    top.write(commands.getoutput('date') + '\n')
    top.write('--------------------------\n')
    top.write(commands.getoutput('top -Hcbn 1') + '\n')
    file = open('/shared/tmp/processes.txt', 'ab')
    all_d_processes = get_d_processes()
    # if there is no process to check, we skip below code
    if '' != all_d_processes[0][0]:
        file.write('--------------------------\n')
        file.write(commands.getoutput('date') + '\n')
        file.write('--------------------------\n')
        file.write ('All D processes: \n')
        file.write(commands.getoutput("ps -eo state,pid,cmd | grep '^D'") + '\n')
        file.write('--------------------------\n')
        file.write('current top IO: \n')
        file.write('--------------------------\n')
        file.write(commands.getoutput('top -Hcbn 1 | head -6') + '\n')
        for process in all_d_processes:
            file.write('--------------------------\n')
            file.write('Process: \n')
            file.write('--------------------------\n')
            file.write(' '.join(process) + '\n')
            file.write('--------------------------\n')
            file.write('cat /proc/%s/io output: \n' % process[1])
            file.write('--------------------------\n')
            file.write(get_rw_io_by_pid(process[1]) + '\n')
            file.write('--------------------------\n')
            file.write('lsof -p %s output: \n' % process[1] + '\n')
            file.write('--------------------------\n')
            file.write(lsof(process[1]) + '\n')
    time.sleep(10)
    if time.time() > start + MAX_TIME_RUNNING:
        file.close()
        top.close()
        break
