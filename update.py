#!/usr/bin/python

import paramiko
import psycopg2

server = "10.10.94.129"

conn = psycopg2.connect(
   database="opensips", user='opensips', password='opensipsrw', host=server, port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()

data = open("gsm.csv","r")
sql = "COPY load_balancer FROM STDIN DELIMITER '|' CSV HEADER"

cursor.execute("truncate load_balancer CASCADE;")
cursor.copy_from(data, "load_balancer", columns=("id","group_id","dst_uri","resources","probe_mode","description"), sep=",")

conn.commit()
conn.close()

ssh = paramiko.SSHClient()
ssh.connect(server, username="root", password="Pls@1234")
ssh.exec_command("opensipsctl fifo lb_reload")
