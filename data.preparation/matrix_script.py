#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
import configurations.config as config #file with user and password (for privacy)

try:
    # DataBase Connexion
    conn = mc.connect(host = 'localhost',
    database = 'fouille', 
    user = config.BD_USER, 
    password= config.BD_PASSWORD) 
                
except mc.Error as err: # If connection fails
    print(err)
else:
    cursor = conn.cursor()
    #cursor.execute("""SELECT Gene_ID FROM Gene;""")
    #genes = cursor.fetchall()
    #print(genes)
    
    cursor.execute("""DROP VIEW IF EXISTS M;""")
    cursor.execute("""DROP VIEW IF EXISTS N;""")
    cursor.execute("""DROP VIEW IF EXISTS S;""")
    
    # View with info on MSD domain for each Gene
    # Retrieve max and min e_value of rpsblast 
    # number of MSD domain
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
                  FROM Gene LEFT JOIN (
                    SELECT Gene_ID, Type, Identification_Status
                      FROM Protein
                      WHERE Identification_Status != 'Rejected'
                  ) AS P
                  ON Gene.Gene_ID = P.Gene_ID
              ) AS T
            ;""")
        
    cursor.execute("""
        SELECT M.Gene_ID, M_Number, M_Min, M_Max, N_Number, N_Min, N_Max, S_Number, S_Min, S_Max
          FROM M JOIN (N JOIN S ON N.Gene_ID = S.Gene_ID)
          ON M.Gene_ID = N.Gene_ID
        ;""")
    
    data = cursor.fetchall()
