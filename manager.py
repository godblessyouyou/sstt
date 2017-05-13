import sched
import time
import threading
import paramiko


class SSHConnect(object):

    def __init__(self, ip, username, password):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, 22, username, password)
        self.ssh = client

    def exe_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        out = ''
        for line in stdout:
            out += line;
        print out
        return out

event = sched.scheduler(time.time, time.sleep)

# Attention:
# Should use test library Collection to contain the data type [{host, command}]
def one_host_seq_exe(host):
    """
    give the host dictionary and command_list to execute.
    """
    connect = SSHConnect(host['ip'], host['username'], host['password'])
    for command in host['command_list']:
        event.enter(0, 0, connect.exe_command, (command,))
        event.run()

def one_host_concurrent_exe(host):
    """
    give the host dictionarary and command_list to execute.
    """
    connect = SSHConnect(host['ip'], host['username'], host['password'])
    for command in host['command_list']:
        event.enter(1, 0, connect.exe_command, (command,))
    event.run()

def multi_host_seq_exe(host):
    """
    give the host dictionarary and command_list to execute.
    """
    for host_node in host:
        connect = SSHConnect(host_node['ip'], host_node['username'], host_node['password'])
        for command in host_node['command_list']:
            event.enter(0, 0, connect.exe_command, (command,))
            event.run()

def multi_host_concurrent_exe(host):
    """
    give the host dictionarary and command_list to execute.
    """
    for host_node in host:
        connect = SSHConnect(host_node['ip'], host_node['username'], host_node['password'])
        for command in host_node['command_list']:
            event.enter(1, 0, connect.exe_command, (command,))
    event.run()


if __name__ == '__main__':
    node_list1 = {'ip': '192.168.102.129', 'username': 'root', 'password': 'fanghao', 'command_list': ['echo hello', 'echo world']}
    node_list2 = {'ip': '192.168.102.129', 'username': 'root', 'password': 'fanghao', 'command_list': ['echo hello', 'echo world']}
    node_list3 = [{'ip': '192.168.102.129', 'username': 'root', 'password':'fanghao', 'command_list': ['echo hello']}, {'ip': '192.168.102.132',
    'username': 'root', 'password': 'fanghao', 'command_list': ['echo hello','echo world']}]
    node_list4 = [{'ip': '192.168.102.129', 'username': 'root', 'password': 'fanghao', 'command_list': ['echo hello',]}, {'ip': '192.168.102.132',
    'username': 'root', 'password': 'fanghao', 'command_list': ['echo hello world',]}]
    
    one_host_seq_exe(node_list1)
    one_host_concurrent_exe(node_list2)
    multi_host_seq_exe(node_list3)
    multi_host_concurrent_exe(node_list4)
