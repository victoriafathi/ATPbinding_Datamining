#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
import argparse 
import csv
import sys
from configurations import config


parser = argparse.ArgumentParser(description='Matrix Creation')
parser.add_argument('--database', '-b', type = str, help = "database you want to connect to")
parser.add_argument('--drop', '-d', required=False, action="store_true", help='drop all views')
parser.add_argument('--create_views', '-c', required=False, action="store_true", help='create intermediary views')

args = parser.parse_args()

try:
    # DataBase Connexion
    conn = mc.connect(host = 'localhost',
    database = args.database, 
    user = config.BD_USER, 
    password= config.BD_PASSWORD) 
                
except mc.Error as err: # If connection fails
    print(err)

else:
    cursor = conn.cursor()
    
    if args.drop:
        cursor.execute("""DROP VIEW IF EXISTS M;""")
        cursor.execute("""DROP VIEW IF EXISTS N;""")
        cursor.execute("""DROP VIEW IF EXISTS S;""")
        cursor.execute("""DROP VIEW IF EXISTS ABC;""")
        cursor.execute("""DROP VIEW IF EXISTS IND_VAR_MATRIX""")

    # View with info on MSD domain for each Gene
    # Retrieve max and min e_value of rpsblast 
    # number of MSD domain
    
    if args.create_views:
        cursor.execute("""
            CREATE VIEW M
                AS
                SELECT Gene.Gene_ID, 
                  CASE
                    WHEN M_Number IS NULL THEN 0 ELSE M_Number
                  END
                    AS M_Number,
                  M_Min, M_Max
                  
                  FROM Gene LEFT JOIN (
                    SELECT Gene_ID, COUNT(*) AS M_Number, MIN(e_Value) AS M_Min, MAX(e_Value) AS M_Max
                      FROM Functional_Domain NATURAL JOIN Conserved_Domain
                      WHERE Family_Link REGEXP '^M'
                      GROUP BY Gene_ID
                  ) AS D
                  ON Gene.Gene_ID = D.Gene_ID
                ;""")
                
        # View with info on NBD domain for each Gene
            # Retrieve max and min e_value of rpsblast 
            # number of MSD domain
        cursor.execute("""
                CREATE VIEW N
                AS
                SELECT Gene.Gene_ID, 
                  CASE
                    WHEN N_Number IS NULL THEN 0 ELSE N_Number
                  END
                    AS N_Number,
                N_Min, N_Max
                
                  FROM Gene LEFT JOIN (
                    SELECT Gene_ID, COUNT(*) AS N_Number, MIN(e_Value) AS N_Min, MAX(e_Value) AS N_Max
                      FROM Functional_Domain NATURAL JOIN Conserved_Domain
                      WHERE Family_Link REGEXP '^N'
                      GROUP BY Gene_ID
                  ) AS D
                  ON Gene.Gene_ID = D.Gene_ID
                ;""")
        
        # View with info on SBP domain for each Gene
            # Retrieve max and min e_value of rpsblast 
            # number of MSD domain
        cursor.execute("""
                CREATE VIEW S
                AS
                SELECT Gene.Gene_ID, 
                  CASE
                    WHEN S_Number IS NULL THEN 0 ELSE S_Number
                  END
                    AS S_Number,
                  S_Min, S_Max
                  
                  FROM Gene LEFT JOIN (
                    SELECT Gene_ID, COUNT(*) AS S_Number, MIN(e_Value) AS S_Min, MAX(e_Value) AS S_Max
                      FROM Functional_Domain NATURAL JOIN Conserved_Domain
                      WHERE Family_Link REGEXP '^S'
                      GROUP BY Gene_ID
                  ) AS D
                  ON Gene.Gene_ID = D.Gene_ID
                ;""")
        
        cursor.execute("""
                CREATE VIEW ABC
                AS
                SELECT T.Gene_id,
                  CASE
                    WHEN T.Type = 'ABC' 
                      AND T.Identification_Status = 'Confirmed' 
                      THEN TRUE
                    WHEN (T.Type IS NULL) 
                      OR (T.Type != 'ABC'
                        AND T.Identification_Status = 'Confirmed'
                      ) THEN FALSE
                    ELSE NULL
                  END
                    AS ABC
                  
                  FROM (
                    SELECT Gene.Gene_ID, Type, Identification_Status
                      FROM Gene LEFT JOIN Protein AS P 
                      ON Gene.Gene_ID = P.Gene_ID
                      WHERE NOT Identification_Status <=> 'Rejected'
                  ) AS T
                ;""")
            
        cursor.execute("""
            CREATE VIEW IND_VAR_MATRIX
            AS
            SELECT M.Gene_ID, M_Number, M_Min, M_Max, N_Number, N_Min, N_Max, S_Number, S_Min, S_Max, ABS(Start - End + 1) AS 
            Gene_Size, Self_Score, ABC
              FROM ((((M 
                NATURAL JOIN N) 
                NATURAL JOIN S) 
                NATURAL JOIN ABC) 
                NATURAL JOIN Gene)
            ;""")
              
    cursor.execute("""SELECT * FROM IND_VAR_MATRIX;""")
    data = cursor.fetchall()

    # Writing tsv file for ind-var matrix 
    matrix = csv.writer(open('matrix_ind_var.tsv', 'w', encoding='utf-8'),delimiter='\t')
    matrix.writerow([i[0] for i in cursor.description])
    for row in data:
      line = ["*" if el is None else el for el in row] #Replace empty values by * 
      # Adding default value 
      for i in [2,3,5,6,8,9] :
          if line[i] == "*":
              line[i]= 10000
      
      matrix.writerow(line)

  #End of connection
    conn.commit() 
    cursor.close() # close cursor
    conn.close() # close connection


