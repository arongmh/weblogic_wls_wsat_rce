#!/usr/bin/env python
#coding:utf-8
import re
import time
import socket
import requests
import sys

headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'}
timeout = 5

'''
check weblogic by 404
'''
def check_weblogic(host,port):
    url = 'http://{}:{}/conso1e'.format(host,port)
    try:
        r = requests.get(url,headers = headers ,timeout =timeout)
        if r.status_code == 404 and 'From RFC 2068' in r.text:
            return check_weblogic_version(host,port)
        else:
            return (False,'may be not weblogic')
    except requests.exceptions.ConnectionError:
        return (False,'ConnectionError')
    except :
        #raise
        return (False,'request weblogic fail')

'''
get weblogic version by t3
modifide by weblogic-t3-info.nse of nmap script
'''
def check_weblogic_version(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.settimeout(timeout)
    try:
        sock.connect(server_address)
        # Send headers
        send_count = 0
        headers = 't3 11.1.2\nAS:2048\nHL:19\n\n'
        # print 'sending Hello'
        sock.sendall(headers)
        data = ''
        #receive data and check version:
        try:
            while True:
                data += sock.recv(1024).strip()
                #print data
                if not data.startswith('HELO'):
                    return (False, 'check version fail')
                m = re.findall(r'HELO:(\d+\.\d+\.\d+\.\d+)\.',data)
                if m:
                    return (True,m[0])
                time.sleep(0.1)
        except socket.timeout:
            return (False,'weblogic unknown version') 
    except Exception, e:
        #raise
        return (False, 'check version fail')
    finally:
        sock.close()

def main():
    if len(sys.argv) != 3:
        print 'usage:{} <ip> <port>'.format(sys.argv[0])
        exit()
   
    result,msg = check_weblogic(sys.argv[1],int(sys.argv[2]))
    print '{}'.format(msg)
        
if __name__ == '__main__':
    main()
