#!/usr/bin/python

import paramiko
import psycopg2

server = "10.10.94.129"

conn = psycopg2.connect(
   database="opensips", user='opensips', password='opensipsrw', host=server, port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()
cursor.execute("truncate load_balancer CASCADE;")

file = open("gsm.csv").readlines()
for line in file:
  data = line.strip().split(',')
  sql = (int(data[0]),data[1],data[2],int(data[3]),data[4])
  cursor.execute('''
		INSERT INTO load_balancer(group_id,dst_uri,resources,probe_mode,description) \
		VALUES {}'''.format(sql))

conn.commit()
conn.close()

ssh = paramiko.SSHClient()
ssh.connect(server, username="root", password="Pls@1234")
ssh.exec_command("opensipsctl fifo lb_reload")
