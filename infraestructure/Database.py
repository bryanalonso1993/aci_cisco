#!/usr/env bin python3.8
import pymysql
import sys
from Logger import ControllerLogger

logger = ControllerLogger()


class ControllerMariaDB(object):
    def __init__(self, hostname, username, password, database):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database = database

    def get_connection(self):
        try:
            con = pymysql.connections.Connection(user=self.username, host=self.hostname,
                                                password=self.password, database=self.database)
            logger.set_log_app('info', 'success connection db:{}/{}'.format(self.hostname, self.database))
        except pymysql.err.InternalError as err:
            logger.set_log_app('critical', err.args)
            sys.exit(1)
        except pymysql.err.OperationalError as err:
            logger.set_log_app('critical', err.args)
            sys.exit(1)
        return con

    def operational_sql_exec_query(self, *args):
        try:
            con = self.get_connection()
            cursor = con.cursor()
            for row_sql in args:
                logger.set_log_app('info', 'execute_query {}'.format(row_sql.__str__()))
                cursor.execute(row_sql)
            cursor.close()
            con.close()
        except pymysql.err.OperationalError as err:
            logger.set_log_app('critical', err.args)
        except pymysql.err.InternalError as err:
            logger.set_log_app('critical', err.args)
        except pymysql.err.ProgrammingError as err:
            logger.set_log_app('critical', err.args)
            return None

    #: args => tuple datasets data insert
    def operational_sql_insert_rows(self, sql_query, *args):
        try:
            con = self.get_connection()
            cursor = con.cursor()
            logger.set_log_app('info', 'query : {}'.format(sql_query.__str__()))
            cursor.executemany(sql_query, args)
            con.commit()
            cursor.close()
            con.close()
        except pymysql.err.OperationalError as err:
            logger.set_log_app('critical', err.args)
        except pymysql.err.InternalError as err:
            logger.set_log_app('critical', err.args)
        except pymysql.err.ProgrammingError as err:
            logger.set_log_app('critical', err.args)
            return None

    #: args => sql set variables in args
    def operational_sql_return_data(self, *args):
        try:
            con = self.get_connection()
            cursor = con.cursor()
            logger.set_log_app('info', 'query list: {}'.format(args.__str__()))
            for row_sql in args:
                cursor.execute(row_sql)
                con.commit()
            cursor.close()
            con.close()
        except pymysql.err.OperationalError as err:
            logger.set_log_app('critical', err.args)
            return None
        except pymysql.err.InternalError as err:
            logger.set_log_app('critical', err.args)
            return None
        except pymysql.err.ProgrammingError as err:
            logger.set_log_app('critical', err.args)
            return None
        data = cursor.fetchall()
        filter_data = [row[0] for row in data]
        return filter_data
