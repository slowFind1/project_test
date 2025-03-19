import  sqlite3
from common.log import  log
from settings import  DBSql

class MysqlAuto(object):
    def __init__(self):
        # 连接数据库
        self.conn = sqlite3.connect(DBSql.sql_file)
        self.cursor = self.conn.cursor() # 创建cursor 对象 ，执行sql命令
        log.info(f"Connected to database : {DBSql.sql_file}")

    def __del__(self):
        # # 资源数据库被释放时候进行触发， 释放内存
        # self.cursor.close()
        # self.conn.close()
        # #log.info(f"Disconnected to database : {DBSql.sql_file}")
        # log.info("Disconnected to database " )
        # 资源数据库被释放时触发，释放内存
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()
        if hasattr(log, 'handlers'):
            for handler in log.handlers:
                handler.close()
        log.info("Disconnected to database")

    def execute_sql(self,sql_list):
        # 执行sql语句
        # try:
        #     for i in sql_list:
        #         log.info(f"Execute sql : {i}")
        #         self.cursor.execute(i)
        #         log.debug(self.cursor.fetchall())   # 打印结果
        #     #提交事物
        #     self.conn.commit()
        #     return  self.cursor.fetchall()
        #     #log.info(f"Execute sql : {sql}")
        # except Exception as e:
        #     log.error(f"Execute sql 异常 : {e}")
        #     raise e

        results = []
        try:
            for i in sql_list:
                log.info(f"Execute sql : {i}")
                self.cursor.execute(i)
                result = self.cursor.fetchall()
                log.debug(result)
                results.extend(result)
            # 提交事物
            self.conn.commit()
            return results
        except Exception as e:
            log.error(f"Execute sql 异常 : {e}")
            raise e



    # def execute_sql(self, sql, params=None):
    #     try:
    #         log.info(f"Execute sql: {sql}")
    #         if params:
    #             self.cursor.execute(sql, params)  # 使用参数化查询
    #         else:
    #             self.cursor.execute(sql)
    #         self.conn.commit()
    #         return self.cursor.fetchall()
    #     except Exception as e:
    #         log.error(f"Execute sql 异常: {e}")
    #         raise e

    def execute(self, sql, params=None):
        try:
            log.info(f"Execute sql: {sql}")
            if params:
                self.cursor.execute(sql, params)  # 使用参数化查询
            else:
                self.cursor.execute(sql)
            self.conn.commit()
            return self.cursor.fetchall()
        except Exception as e:
            log.error(f"Execute sql 异常: {e}")

if __name__ == '__main__':
    # 创建对象
    mysql = MysqlAuto()

    #查询命令，进行简单测试sql语句命令
    #mysql.execute_sql(['select *from df_user_userinfo'])

    # 执行sql
    mysql.execute_sql(DBSql.sql_list) # 执行sql_list 中已经设定好的语句，进行初始化
    # 释放资源
    del mysql