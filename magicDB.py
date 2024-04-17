import sys
import configparser
import MySQLdb


from datetime import datetime

__version__ = "2.0.0"


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class DBConnection(object):
    """
    Class created to manage the DB access, making the DB commands accesss easier to use
    """
    def __init__(self, parent=None):
        super(DBConnection, self).__init__()

        #read database information from dbconfig.ini
        parser = configparser.SafeConfigParser()
        parser.read("dbconfig.ini")
        self.connectionData = {}
        self.connectionData["host"] = parser.get("db_connection", "host")
        self.connectionData["user"] = parser.get("db_connection", "user")
        self.connectionData["passwd"] = parser.get("db_connection", "passwd")
        self.connectionData["db"] = parser.get("db_connection", "db")

###############################################################################################################################################################################

    def selectQuery(self, fields, tables=None, where=None, groupby=None, having=None, orderby=None, limit=None, queryBuild=False):
        """
        This method builds the query to retrieve data from the database through the SELECT command
        """
        # --> executing datetime #
        queryDatetime = datetime.now()
        dbCon = None
        
        # --> firstly builds the SELECT statement #
        sqlString = []
        sqlString.append("SELECT")
        sqlString.append(", ".join(fields))
        sqlString.append("FROM")

        # --> builds up the "FROM" part of the SELECT statement #
        if tables is not None:
            firstTable, joinType, condition = tables.pop(0)
            tablesString = []
            tablesString.append(firstTable)
            for table, joinType, condition in tables:
                if joinType:
                    tablesString.append(joinType)
                tablesString.append("JOIN")
                tablesString.append(table)
                tablesString.append("ON")
                tablesString.append(condition)
            
            sqlString.append(" ".join(tablesString))

        # --> builds the "WHERE" part of the SELECT statement #
        if where is not None:
            sqlString.append("WHERE")
            sqlString.append(" AND ".join(where))

        # --> builds the "GROUP BY" part of the SELECT statement #
        if groupby is not None:
            sqlString.append("GROUP BY")
            sqlString.append(", ".join(groupby))
            
        # --> builds the "HAVING" part of the SELECT statement #
        if having is not None:
            sqlString.append("HAVING")
            sqlString.append(" AND ".join(having))

        # --> builds the "ORDER BY" part of the SELECT statement #
        if orderby is not None:
            sqlString.append("ORDER BY")
            sqlString.append(", ".join(orderby))

        # --> builds the "LIMIT" part of the SELECT statement #
        if limit is not None:
            sqlString.append("LIMIT")
            sqlString.append(", ".join(limit))
        
        query = " ".join(sqlString)

        if queryBuild:
            return query

        statusDBCommand = False
        result = []
        
        try:
            dbCon = MySQLdb.connect(host = self.connectionData["host"],
                                user = self.connectionData["user"],
                                passwd = self.connectionData["passwd"],
                                db = self.connectionData["db"])
            dbCursor = dbCon.cursor()
            dbCursor.execute(query)
            statusDBCommand = True
            result = dbCursor.fetchall()
            
        except MySQLdb.Error as err:
            errorMsg = str(queryDatetime) + " -> " + query + " ==> " + str(err)         
            with open("output.txt", "a+") as text_file:
                print(errorMsg, file=text_file, end="\n\n")
            
            

        finally:
            if dbCon:
                dbCursor.close()
                dbCon.close()

        return (statusDBCommand, result)
       

###############################################################################################################################################################################

        
    def updateQuery(self, tables, fieldsAndValues, conditions=None, queryBuild=False):
        """
        This method builds the query to update the data at the database through the UPDATE command.
        The query will be executed using commit/rollback, making the update process atomic, preventing any
        data lost during update
        """
        # --> executing datetime #
        queryDatetime = datetime.now()

        # --> firstly builds the UPDATE statement string #
        sqlString = []
        sqlString.append("UPDATE")
        sqlString.append(", ".join(tables))
        sqlString.append("SET")


        # --> builds the strings with the updating values #
        fieldsString = []
        for field, value in fieldsAndValues:
            fieldsString.append("%s = %s" % (field, value))

        sqlString.append(", ".join(fieldsString))


        # --> builds the "WHERE" part of the UPDATE statement #
        if conditions is not None:
            sqlString.append("WHERE")
            sqlString.append(" AND ".join(conditions))

        query = " ".join(sqlString)

        if queryBuild:
            return query
        
        statusDBCommand = False
        updateId = 0
        
        try:
            dbCon = MySQLdb.connect(host = self.connectionData["host"],
                                user = self.connectionData["user"],
                                passwd = self.connectionData["passwd"],
                                db = self.connectionData["db"])
            dbCon.autocommit(False)
            dbCursor = dbCon.cursor()
            dbCursor.execute(query)
            updateId = dbCursor.lastrowid
            statusDBCommand = True
            

        except MySQLdb.Error as err:
            if dbCon:
                dbCon.rollback()
            errorMsg = str(queryDatetime) + " -> " + query + " ==> " + str(err)         
            with open("output.txt", "a+") as text_file:
                print(errorMsg, file=text_file, end="\n\n")

        finally:
            if dbCon:
                if statusDBCommand:
                    dbCon.commit()
                dbCursor.close()
                dbCon.close()
        
        return (statusDBCommand, updateId)
        

###############################################################################################################################################################################

    def deleteQuery(self, tables, conditions, queryBuild=False):
        """
        This method builds a query to delete the data at the database through the DELETE command
        """
        # --> executing datetime #
        queryDatetime = datetime.now()
        
        sqlString = []
        sqlString.append("DELETE FROM")
        sqlString.append(", ".join(tables))
        sqlString.append("WHERE")

        sqlString.append(" AND ".join(conditions))

        query = " ".join(sqlString)

        if queryBuild:
            return query

                
        statusDBCommand = False
        insertedId = 0
        
        try:
            dbCon = MySQLdb.connect(host = self.connectionData["host"],
                                user = self.connectionData["user"],
                                passwd = self.connectionData["passwd"],
                                db = self.connectionData["db"])
            dbCon.autocommit(False)
            dbCursor = dbCon.cursor()
            dbCursor.execute(query)
            insertedId = dbCursor.lastrowid
            statusDBCommand = True
            
        except MySQLdb.Error as err:
            if dbCon:
                dbCon.rollback()
            errorMsg = str(queryDatetime) + " -> " + query + " ==> " + str(err)         
            with open("output.txt", "a+") as text_file:
                print(errorMsg, file=text_file, end="\n\n")

        finally:
            if dbCon:
                if statusDBCommand:
                    dbCon.commit()
                dbCursor.close()
                dbCon.close()
        
        return (statusDBCommand, insertedId)

       
        

###############################################################################################################################################################################

     
    def insertQuery(self, table, fields, values, queryBuild=False):
        """
        This method builds the query to insert the data at the database through the INSERT command.
        The query will be executed using commit/rollback, making the insert process atomic, preventing any
        data lost during insert
        """
        # --> executing datetime #
        queryDatetime = datetime.now()
        
        # --> firstly builds the INSERT statement string #
        sqlString = []
        sqlString.append("INSERT INTO")
        sqlString.append(table)
        sqlString.append("(")
        sqlString.append(", ".join(fields))
        sqlString.append(")")
        sqlString.append("VALUES")

        # --> build a list with all the values that will be inserted into the database
        valuesString = []
        for insertValue in values:
            valuesString.append("(" + ", ".join(insertValue) + ")")

        sqlString.append(", ".join(valuesString))

        query = " ".join(sqlString)

        if queryBuild:
            return query
        
        statusDBCommand = False
        insertId = 0
        
        try:
            dbCon = MySQLdb.connect(host = self.connectionData["host"],
                                user = self.connectionData["user"],
                                passwd = self.connectionData["passwd"],
                                db = self.connectionData["db"])
            dbCon.autocommit(False)
            dbCursor = dbCon.cursor()
            dbCursor.execute(query)
            insertId = dbCursor.lastrowid
            statusDBCommand = True
            
        except MySQLdb.Error as err:
            if dbCon:
                dbCon.rollback()
            errorMsg = str(queryDatetime) + " -> " + query + " ==> " + str(err)         
            with open("output.txt", "a+") as text_file:
                print(errorMsg, file=text_file, end="\n\n")

        finally:
            if dbCon:
                if statusDBCommand:
                    dbCon.commit()
                dbCursor.close()
                dbCon.close()

        return (statusDBCommand, insertId)

###############################################################################################################################################################################

    def aglutinatedQuery(self, queryList):
        """
        This method was created to atomize the query operation. If there is any action in the system that demands
        more than one sql query this method must be called
        """
        # --> executing datetime #
        queryDatetime = datetime.now()

        statusDBCommand = False
        
        try:
            dbCon = MySQLdb.connect(host = self.connectionData["host"],
                                user = self.connectionData["user"],
                                passwd = self.connectionData["passwd"],
                                db = self.connectionData["db"])
            dbCon.autocommit(False)
            dbCursor = dbCon.cursor()
            for query in queryList:
                dbCursor.execute(query)
            statusDBCommand = True
            
        except MySQLdb.Error as err:
            if dbCon:
                dbCon.rollback()
            errorMsg = str(queryDatetime) + " -> " + query + " ==> " + str(err)         
            with open("output.txt", "a+") as text_file:
                print(errorMsg, file=text_file, end="\n\n")

        finally:
            if dbCon:
                if statusDBCommand:
                    dbCon.commit()
                dbCursor.close()
                dbCon.close()

        return statusDBCommand
