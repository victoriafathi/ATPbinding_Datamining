# -*- coding: utf-8 -*-

import mysql.connector as mc
import configurations.config as config

try:
    # Connection à la base de donnée
    conn = mc.connect(host = 'localhost',
    database = 'fouille', 
    user = config.BD_USER, # nom user dans le fichier config
    password= config.BD_PASSWORD) # mot de passe dans le fichier config
                
except mc.Error as err: # si la connexion échoue
    print(err)

finally:
    cursor = conn.cursor()
    #cursor.execute("""SELECT Gene_ID FROM Gene;""")
    #genes = cursor.fetchall()
    #print(genes)
    
    cursor.execute("""DROP VIEW IF EXISTS M;""")
    cursor.execute("""DROP VIEW IF EXISTS N;""")
    cursor.execute("""DROP VIEW IF EXISTS S;""")
    
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
        SELECT M.Gene_ID, M_Number, M_Min, M_Max, N_Number, N_Min, N_Max, S_Number, S_Min, S_Max
          FROM M JOIN (N JOIN S ON N.Gene_ID = S.Gene_ID)
          ON M.Gene_ID = N.Gene_ID
        ;""")
    
    data = cursor.fetchall()