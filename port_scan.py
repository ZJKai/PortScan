# -*- conding:utf8 -*-

import socket
import argparse
import sys
from IPy import IP
import queue
import threading


def scan_server(q):
    global lock
    while True:
        ip, port = q.get()
        ss = socket.socket()
        ss.settimeout(1)
        result = ss.connect_ex((ip, port))
        ss.close()

        if result == 0:
            lock.acquire()
            print('{} 开放端口: {}'.format(ip, port))
            lock.release()
        q.task_done()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--hosts', required=True, help='destination host')
    parser.add_argument('-p', '--ports', default='3389,22', help='destination port, default 3389,20')
    parser.add_argument('-t', '--threads', default='20', help='maximum threads, default 20')
    args = parser.parse_args()

    try:
        ips = IP(args.hosts)

    except ValueError:
        print('格式错误')
        sys.exit()

    ports = args.ports

    if ports == 'all':
        ports = [int(x) for x in range(65536)]
    else:
        ports = [int(x) for x in args.ports.split(',')]

    threads = args.threads

    if threads != None and int(threads) != 0:
        threads = int(threads)

    lock = threading.Lock()
    q = queue.Queue()

    print('start scan: \n')

    for i in range(threads):
        t = threading.Thread(target=scan_server, args=(q,))
        t.setDaemon(True)
        t.start()

    for ip in ips:
        ip = str(ip)
        if int(ip.split('.')[-1]) not in (0, 254, 255):
            for port in ports:
                q.put((ip, port))
    q.join()
    