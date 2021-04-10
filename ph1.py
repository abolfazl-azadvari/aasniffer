import socket, sys, threading, time
from queue import Queue
from datetime import datetime


host = input("Enter the host address: ")
timeout = input("Enter the timeout for each port: ")
socket.setdefaulttimeout(int(timeout))


def check(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((host, port))
        print('port', port, 'open.')
        con.close()
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting.')
    except socket.error:
        print('port', port, 'closed.')
    except:
        pass

def threader():
    while True:
        worker = q.get()
        check(worker)
        q.task_done()

q = Queue() 

threads = input("Enter the number of threads: ")

mode = input("Enter Mode (common, range, known): ")

if mode == "known":
    ports = [80, 443, 25, 21, 23, 22]
elif mode == "common":
    ports = range(0, 1024)
else:
    start = input("Enter start of the range: ")
    end = input("Enter end of the range: ")
    ports = range(int(start), int(end) + 1)

for _ in range(int(threads)):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for worker in ports:
    q.put(worker)

q.join()
