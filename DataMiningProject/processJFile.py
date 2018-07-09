#!/usr/bin/python

#Loads the database with the records from the jobs.swf file into jobs
#after making sure that there are no -1 records found. (preprocess)

import sys
import MySQLdb

recDict = dict()

#---------------------------------------------------------------------
def connectDB():
    db = MySQLdb.connect("localhost","root","dmining")
    cursor = db.cursor()

#   build the database and the tables.
    cursor.execute("SET sql_notes = 0;")
    sql = 'CREATE DATABASE IF NOT EXISTS Project'
    cursor.execute(sql)
    cursor.execute("USE Project;")

#   creates the table
    cursor.execute("DROP TABLE IF EXISTS JOBS")
    sql = """ CREATE TABLE JOBS(
                JOB_ID INT NOT NULL,
                SUBMIT_TIME INT,
                WAIT_TIME INT,
                RUN_TIME INT,
                ALLOC_PROC INT,
                REQ_PROC INT,
                REQ_TIME INT,
                USER_ID INT,
                QUEUE INT,
                PRIMARY KEY(JOB_ID) ) """
    cursor.execute(sql)
    cursor.execute("SET sql_notes = 1;")

    return db, cursor

#---------------------------------------------------------------------
def loadTables(db, cursor):
    for key in recDict.keys():
        L = [int(item) for item in recDict[key]]
        sql = " INSERT INTO JOBS(JOB_ID, \
                SUBMIT_TIME, WAIT_TIME, RUN_TIME, \
                ALLOC_PROC, REQ_PROC, REQ_TIME, \
                USER_ID, QUEUE) \
                VALUES('%d','%d','%d','%d','%d','%d','%d','%d','%d')" % \
                (L[0], L[1], L[2],L[3], L[4], L[5], L[6], L[7], L[8] )
        try:
            cursor.execute(sql)
        except:
            db.rollback()

#---------------------------------------------------------------------
def main(argv):
    inputFile = argv[0]
    count = 1
    with open(inputFile) as fp:
        for line in fp:
            data = line.strip().split()
            if len(data) > 0 and not data[0].startswith(';'):
                newData = [items for items in data if items != '-1']
                recDict[count] = newData
                count += 1
    # there are 9 fields with positive value and we extract them all.
    #les = [ len([val for val in recDict[key]]) for key in recDict.keys() ]

#---------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) == 2:
        db, cursor = connectDB()
        main(sys.argv[1:])
#       commit and close the connection
        loadTables(db, cursor)

        db.commit();
        db.close();
    else:
        print '"insufficient number of arguments", len(sys.argv)'
#---------------------------------------------------------------------
