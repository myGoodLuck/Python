# -*- coding: utf-8 -*-

import pymysql
def dbHandle():
    conn = pymysql.connect(
        host = "localhost",
        user = "root",
        passwd = "root",
        db="text",
        port =3306,
        charset = "utf8",
        use_unicode = False
    )
    return conn

class newyorkerPipeline(object):
    def process_item(self,item,spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE text")
        sql = "INSERT INTO newtext(title,author,time,article,image_urls,w_sum,s_sum,p_sum,v_sum,a_sum,avg_w,avg_s,avg_p) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor.execute(sql, (item['title'], item['author'], item['time'], item['article'],item['image_urls'],item['w_sum'],item['s_sum'],item['p_sum'],item['v_sum'],item['a_sum'],item['avg_w'],item['avg_s'],item['avg_p']))
            cursor.connection.commit()
        except BaseException as e:
            print e
            dbObject.rollback()
         
        return item