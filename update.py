#!/usr/bin/python

import paramiko
import psycopg2

server = "10.10.94.129"

conn = psycopg2.connect(
   database="opensips", user='opensips', password='opensipsrw', host=server, port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()
data = open("gsm.csv").readlines()
for line in data:
  ip,resource = line.strip().split(',')
  text = ''' UPDATE load_balancer set resources = 'vt={0}' where dst_uri = 'sip:10.10.{1}:5060';
  '''.format(resource,ip)
  print(text)
  cursor.execute(text)

conn.commit()
conn.close()

ssh = paramiko.SSHClient()
ssh.connect(server, username="root", password="Pls@1234")
ssh.exec_command("opensipsctl fifo lb_reload")
