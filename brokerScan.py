#!/usr/bin/env python

import socket

from threading import Thread, Lock

mutex = Lock()

def host_scan(host_port, timeout):
    host, port = host_port.split(":")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, int(port)))
        sock.close()
        with mutex:
           print("Success connecting: " + host + ":" + port)
    except (socket.timeout, socket.error):
        with mutex:
            print("Cannot connect to:  " + host + ":" + port)


if __name__=="__main__":

    host_list = ["127.0.0.1:1883", "127.0.0.1:9001",
                 "broker.hivemq.com:1883", "broker.hivemq.com:8000",
                 "iot.eclipse.org:1883", "iot.eclipse.org:80"]

    print("\nMQTT broker hosts scanning:\n")
    for host in host_list:
        pThread = Thread(target=host_scan, args=(host, 5))
        pThread.start()
 
