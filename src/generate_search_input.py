import mysql.connector.pooling
import itertools
import json

dbconfig = {"database": 'author', "user": 'root', "password": 'root', "host": 'ecs-devo-db.ctl0cr5o3mqq.ap-southeast-1.rds.amazonaws.com'}
cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="author_pool", pool_size=1, autocommit=True, **dbconfig)
db_conn = cnxpool.get_connection()
cursor = db_conn.cursor(buffered=True)


print "query pratilipi"

max_offset = 200000
offset = 0

with open('PRATILIPI', 'wb') as fobj:
    while offset <= max_offset:
        sql = """SELECT a.id as pratilipi_id, author_id, title_en, title, summary, a.language, a.type, GROUP_CONCAT(name) as category, GROUP_CONCAT(name_en) as category_en
                 FROM pratilipi.pratilipi a LEFT JOIN pratilipi.pratilipis_categories b ON (a.id = b.pratilipi_id) LEFT JOIN pratilipi.categories c ON (b.category_id = c.id)
                 WHERE STATE = 'PUBLISHED'
                 GROUP BY 1,2,3,4,5,6,7
                 ORDER BY 1
                 LIMIT 10000
                 OFFSET %(offset)s"""
        cursor.execute(sql, {'offset': offset})
        desc = cursor.description
        pratilipis = [dict(itertools.izip([col[0].upper() for col in desc], row)) for row in cursor.fetchall()]
        for row in pratilipis:
            fobj.write(json.dumps(row))
            fobj.write("\n")
        offset = offset + 10000
        print "write to file pratilipi - {}".format(offset)
print "done writing to file pratilipi"

print "query author"
max_offset = 1025000
offset = 0

with open('AUTHOR', 'wb') as fobj:
    while offset <= max_offset:
        sql = "SELECT id as author_id, language, first_name, last_name, pen_name, first_name_en, last_name_en, pen_name_en, summary FROM author.author WHERE STATE = 'ACTIVE' ORDER BY 1 LIMIT 10000 OFFSET %(offset)s"
        cursor.execute(sql, {'offset': offset})
        desc = cursor.description
        authors = [dict(itertools.izip([col[0].upper() for col in desc], row)) for row in cursor.fetchall()]
        for row in authors:
            fobj.write(json.dumps(row))
            fobj.write("\n")
        offset = offset + 10000
        print "write to file author - {}".format(offset)
print "done query author"

db_conn.close()
