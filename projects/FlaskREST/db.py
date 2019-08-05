#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

#populate demo database
conn = sqlite3.connect("algo_params.db")
c = conn.cursor()
c.execute('''CREATE TABLE algo_params(
algo_id INTEGER PRIMARY KEY AUTOINCREMENT,
algo_name TEXT NOT NULL,
algo_param1 TEXT NOT NULL,
algo_param2 TEXT NOT NULL);''')
c.execute('''INSERT INTO algo_params (algo_name, algo_param1, algo_param2)
    VALUES ('BowtieSpark', '/s1/snagaraj/project_env/SRR639031_1.fastq' , '/s1/snagaraj/project_env/SRR639031_2.fastq');''')
c.execute('''INSERT INTO algo_params (algo_name, algo_param1, algo_param2)
    VALUES ('Fragment_assignment', '/s1/snagaraj/project_env/SRR639031_1.fastq_1' , '/s1/snagaraj/project_env/SRR639031_2.fastq_2');''')
conn.commit()
conn.close()
