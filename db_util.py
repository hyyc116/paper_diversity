#coding:utf8
'''Some common tools'''
'''Yong Huang @ 10:35 02-24-2017 '''
import MySQLdb
from MySQLdb import cursors
import sys
from collections import defaultdict
import re
import codecs
import random as rn
import logging
import psycopg2


class dbop:

    def __init__(self,insert_index=0):
        
        self._insert_index=insert_index
        self._insert_values=[]


    def connect_aws(self,isSS=False):
        if isSS:
            logging.debug("connect database with normal SScursor.")
            self._db = MySQLdb.connect("localhost","root","irlab2013","aws",cursorclass = cursors.SSCursor)
        else:
            logging.debug("connect database with normal cursor.")
            self._db = MySQLdb.connect("localhost","root","irlab2013","aws")    
        self._cursor = self._db.cursor()


    def connect_wos(self,isSS=False):
        if isSS:
            logging.debug("connect database with normal SScursor.")
            self._db = MySQLdb.connect("localhost","root","irlab2013","aws",cursorclass = cursors.SSCursor)
        else:
            logging.debug("connect database with normal cursor.")
            self._db = MySQLdb.connect("localhost","root","irlab2013","aws")    
        self._cursor = self._db.cursor()



    def query_database(self,sql):
        self._cursor.close()
        self._cursor = self._db.cursor()
        self._cursor.execute(sql)
        logging.debug("query database with sql {:}".format(sql))
        return self._cursor

    def insert_database(self,sql,values):
        self._cursor.close()
        self._cursor = self._db.cursor()
        self._cursor.executemany(sql,values)
        logging.debug("insert data to database with sql {:}".format(sql))
        self._db.commit()
        

    def batch_insert(self,sql,row,step,is_auto=True,end=False):
        if end:
            if len(self._insert_values)!=0:
                logging.info("insert {:}th data into database,final insert.".format(self._insert_index))
                self.insert_database(sql,self._insert_values)
        else:
            self._insert_index+=1
            if is_auto:
                row[0] = self._insert_index
            self._insert_values.append(tuple(row))
            if self._insert_index%step==0:
                logging.info("insert {:}th data into database".format(self._insert_index))
                self.insert_database(sql,self._insert_values)
                self._insert_values=[]

    def get_insert_count(self):
        return self._insert_index

    def execute_del_update(self,sql):
        self._cursor.execute(sql)
        self._db.commit()
        logging.debug("execute delete or update sql {:}.".format(sql))

    def execute_sql(self,sql):
        self._cursor.execute(sql)
        self._db.commit()
        logging.debug("execute sql {:}.".format(sql))

    def close_db(self):
        self._db.close()


if __name__=="__main__":
    dboperation = dbop(isSS=True)
    sql=" select * from m_notbuy_api_log order by userid desc"
    cursor = dboperation.query_database(sql)
    last_userid=-1
    usercount=0
    head= 'id,appid,appkey,uuid,iostoken,userid,mdels,netmodel,channelid,ip,apipath,resultjson,parameter,type,os,browser,operationcode,execute_time,createby,updaeby,createtime,updatetime,version,module,sessionindex,phonetype\n'
    file = open("../../Task_List/notbuy_1000.txt", "w")
    file.write(head)
    outlist=[]
    # sessionindex_count=defaultdict(int)
    for row in cursor:
        userid = row[5]
        # print userid
        # break
        if userid!=last_userid and last_userid!=-1:
            
            if rn.random()<0.5:
                usercount+=1
                print usercount,userid
                file.write('\n'.join(outlist))
                outlist=[]

            if usercount>1000:
                break

        outlist.append(','.join([unicode(str(vol),errors='ignore') for vol in row]))

        last_userid = userid


    print 'done'
    

    
    # file.close()












