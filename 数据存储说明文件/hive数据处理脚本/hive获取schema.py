from flask import Flask,jsonify,request
from impala.dbapi import connect
import time as Time

from xlwt import *

hiveconn = connect(host='8.133.173.118', port=10000, database='default', user='123', password='123', auth_mechanism='PLAIN')

def create_excel():
    sql = 'show tables'
    tables = []
    with hiveconn.cursor() as cursor:
        cursor.execute(sql)
        res = cursor.fetchall()
        for table in res:
            tables.append(table[0])
    
    tableinfo = []
    for table in tables:
        tableinfo.append(get_column_info(table))
 
    create_excel_ex(tableinfo)
 
def create_excel_ex(tableinfo):
    w = Workbook()
    sheet = w.add_sheet(u'表结构')
    row = 0
    for info in tableinfo:
        row = write_tale_info(info,sheet,row)
    w.save('hive_schema.xls')
 
def write_tale_info(tableinfo,sheet,row):
    print(row)
    sheet.write_merge(row,row,0,2,tableinfo['table'])
    
    row += 1
    sheet.write(row,0,u'名称')
    sheet.write(row,1,u'类型')
    sheet.write(row,2,u'解释')
    row += 1
 
    fields = tableinfo['fields']
    for field in fields:
        sheet.write(row,0,field['name'])
        sheet.write(row,1,field['type'])
        row += 1
 
    return row + 1 
    
    
def get_column_info(table):
    sql = 'desc {table}'.format(table=table)
    info = {'table':table,'fields':[]}
    with hiveconn.cursor() as cursor:
        cursor.execute(sql)
        res = cursor.fetchall()
        for item in res:
            if item[0] == '':
                break
            info['fields'].append({'name':item[0],'type':item[1]})
 
    return info
 
if __name__ == '__main__':
    create_excel()