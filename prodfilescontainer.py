import sys

from openpyxl import (Workbook, load_workbook)

from myExceptions import *
from magicDB import *

__version__ = "1.5.4"
"""
1.5.3 - 2020
1.5.4 - 2024
"""


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class ProdFileOp(object):
    """
    This class holds all the informations about a specific production file.
    it will store basic informations, and detailed data about a day production
    orders that contain TEST when requested.
    """

    def __init__(self, row, client, product, quantity, beginningHour, hoursProduction, raw_product, location):
        self.row = row
        self.client = client
        self.clientId = 1
        self.product = product
        self.raw_product = raw_product
        self.productId = 1
        self.quantity = quantity
        self.beginningHour = beginningHour
        self.hoursProduction = hoursProduction
        self.location = location
        self.locationExists = False

    ###############################################################################################################################################################################

    def getClientId(self):
        """
        This method searches in the database for the id of the client, trying to match de exact name of the client
        """
        myDBConnection = DBConnection()

        fields = ["cli_id"]

        tables = [("clientes", "", "")]

        where = ["cli_nome LIKE '" + self.client + "'"]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where)

        # --> If any error during database connection #
        if not querySuccess:
            raise DatabaseConnectionError("Durante a busca do nome do Cliente ao enviar o plano de produção.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        if len(queryResult) <= 0:
            self.clientId = 1
        else:
            self.clientId = queryResult[0][0]

    ###############################################################################################################################################################################
    ###############################################################################################################################################################################

    def checkLocationExists(self):
        """
        This method checks if the location exists in the database
        """
        myDBConnection = DBConnection()

        fields = ["COUNT(*)"]
        tables = [("local_chamado", "", "")]
        where = ["loc_nome LIKE '" + self.location + "'"]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where)

        if not querySuccess:
            raise DatabaseConnectionError(
                "During the search for the name of the location when sending the production plan.",
                "Failed to execute the query in the database.\nContact the system administrator.")
            return False

        # Se o número de linhas retornadas for maior que zero, o local existe no banco
        return queryResult[0][0] > 0

    ###############################################################################################################################################################################

    def getProductId(self):
        """
        This method searches in the database for the id of the op product, trying to match the exact name
        """
        myDBConnection = DBConnection()

        fields = ["pro_id"]

        tables = [("produtos", "", "")]

        where = [
            "pro_nome LIKE '" + str(self.product) + "'",
            "pro_cliente = '" + str(self.clientId) + "'",
            "pro_ativo = '1'"]

        orderBy = ["pro_nome DESC"]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, orderby=orderBy)

        # --> If any error during database connection #
        if not querySuccess:
            raise DatabaseConnectionError("Durante a busca do nome do Produto ao enviar o plano de produção.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        if len(queryResult) <= 0:
            self.productId = 1
        else:
            self.productId = queryResult[0][0]


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class ProdFileOpContainer(object):
    """
    This class holds the information about the production plan and all its programmed production
    """

    def __init__(self):
        self.__ops = []
        self.totalProductionHours = 0
        self.totalProductionQuantity = 0
        self.productionDate = ""
        self.unformatedProductionDate = ""

    ###############################################################################################################################################################################

    def setDate(self, date):
        self.unformatedProductionDate = date
        splitDate = date.split("/")
        self.productionDate = splitDate[2] + "-" + splitDate[1] + "-" + splitDate[0]

    ###############################################################################################################################################################################

    def populateContainer(self, opList):
        """
        This method is used to create a ProdFileOp object for each operation in the production plan and add it to the prod file container.
        """
        self.totalProductionQuantity = sum(op[3] for op in opList)
        self.totalProductionHours = sum(op[5] for op in opList)

        for op in opList:
            # Extract operation information
            row = op[0]
            client = op[1]
            product = op[2]
            quantity = op[3]
            beginningHour = op[4]
            hoursProduction = op[5]
            raw_product = op[6]
            location = op[7]  # Adding operation location

            # Check if the location exists in the database
            newProdFileOp = ProdFileOp(row, client, product, quantity, beginningHour, hoursProduction, raw_product,
                                       location)
            location_exists = newProdFileOp.checkLocationExists()

            # If the location is not registered, assign it as "location not registered"
            if not location_exists:
                location = "NÃO CADASTRADO"

            # Create the ProdFileOp object
            newProdFileOp = ProdFileOp(row, client, product, quantity, beginningHour, hoursProduction, raw_product,
                                       location)

            try:
                newProdFileOp.getClientId()
                newProdFileOp.getProductId()
            except DatabaseConnectionError as error:
                raise DatabaseConnectionError(
                    "Durante a busca dos nomes do Cliente e Produto durante o envio do plano de produção.",
                    "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
                return

            # Add the ProdFileOp object to the container
            self.add(newProdFileOp)

    ###############################################################################################################################################################################

    def add(self, op):
        """
        This method inserts an OP to the ops list
        """
        self.__ops.append(op)

    ###############################################################################################################################################################################

    def flushToDatabase(self):
        """
        Inserts the data to the Database. If any problem happens raise exception
        """
        myDBConnection = DBConnection()

        table = "planos_de_producao"

        fields = [
            "pdp_data",
            "pdp_total_horas",
            "pdp_total_producao"
        ]

        values = [
            ("'" + self.productionDate + "'",
             "'" + str(self.totalProductionHours) + "'",
             "'" + str(self.totalProductionQuantity) + "'")
        ]

        inserted, insertedId = myDBConnection.insertQuery(table, fields, values)

        if not inserted:
            raise DatabaseConnectionError("Durante a inserção dos dados do plano de produção no banco.",
                                          "Falha ao tentar executar a inserção no banco.\nContate o administrador do "
                                          "sistema.")
            return

        if inserted:

            table = "ordens_de_producao"

            fields = [
                "odp_plano_de_producao",
                "odp_cliente",
                "odp_produto",
                "odp_quantidade",
                "odp_hora_inicio",
                "odp_horas_producao"
            ]

            values = []

            for op in self.__ops:
                values.append(("'" + str(insertedId) + "'",
                               "'" + str(op.clientId) + "'",
                               "'" + str(op.productId) + "'",
                               "'" + str(op.quantity) + "'",
                               "'" + op.beginningHour + "'",
                               "'" + str(op.hoursProduction) + "'"))

            inserted, insertedId = myDBConnection.insertQuery(table, fields, values)

            if not inserted:
                raise DatabaseConnectionError("Durante a inserção dos dados das ordens de produção no banco.",
                                              "Falha ao tentar executar a inserção no banco.\nContate o administrador do sistema.")
                return

    ###############################################################################################################################################################################

    def createCalls(self):
        """
        This method is called to insert into the calls table all the installation needed for the next production plan
        """
        myDBConnection = DBConnection()

        table = "chamados"

        fields = [
            "cha_tipo",
            "cha_cliente",
            "cha_produto",
            "cha_DT",
            "cha_descricao",
            "cha_status",
            "cha_data_hora_abertura",
            "cha_operador",
            "cha_plano",
            "cha_local"
        ]

        values = []

        for op in self.__ops:
            callDescription = "CHAMADO AUTOMÁTICO - INSTALAÇÃO\nDATA: " + self.unformatedProductionDate + " \nHORA: " + op.beginningHour
            callDescription += " \nCLIENTE: " + str(op.client)
            callDescription += " \nPRODUTO: " + str(op.raw_product)

            values.append((
                "'1'",
                "'" + str(op.clientId) + "'",
                "'" + str(op.productId) + "'",
                "'000000'",
                "'" + callDescription + "'",
                "'1'",
                "'" + self.productionDate + " " + op.beginningHour + "'",
                "'plano.de.producao'",
                "'1'",
                "'" + op.location + "'",
            ))

        # Debugging: Print SQL query before execution
        query = myDBConnection.insertQuery(table, fields, values, queryBuild=True)
        print("SQL Query:", query)

        inserted, insertedId = myDBConnection.insertQuery(table, fields, values)
        if not inserted:
            raise DatabaseConnectionError("Durante a inserção dos dados das ordens de produção no banco.",
                                          "Falha ao tentar executar a inserção no banco.\nContate o administrador do sistema.")
            return

    ###############################################################################################################################################################################

    def __iter__(self):
        for op in iter(self.__ops):
            yield op

    ###############################################################################################################################################################################

    def __len__(self):
        return len(self.__ops)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class ProdFileTranslator(object):
    """
    This class is used to translate the .xlsx production file and stores it
    to the database
    """

    def __init__(self, filePath):
        self.filePath = filePath
        self.workSheet = None
        self.parseList = []

        self.hourList = {}
        self.populateHourList()

        # --> Columns defines #
        self.CLIENTCOLUMN = 0
        self.PRODUCTCOLUMN = 1
        self.QUANTITYCOLUMN = 42
        self.LOCALCOLUMN = 8
        self.HASTESTCOLUNN = 10
        self.T3BEFORELUNCH = list(range(13, 15))
        self.T3AFTERLUNCH = list(range(16, 19))
        self.T1BEFORELUNCH = list(range(20, 25))
        self.T1AFTERLUNCH = list(range(26, 30))
        self.T2BEFORELUNCH = list(range(31, 35))
        self.T2AFTERLUNCH = list(range(36, 41))

        self.productionHoursList = self.T3BEFORELUNCH + self.T3AFTERLUNCH + self.T1BEFORELUNCH + self.T1AFTERLUNCH + self.T2BEFORELUNCH + self.T2AFTERLUNCH

    ###############################################################################################################################################################################

    def populateHourList(self):
        # --> T3 #
        self.hourList[13] = "00:38:00"
        self.hourList[14] = "01:00:00"
        self.hourList[15] = "02:00:00"
        self.hourList[16] = "03:00:00"
        self.hourList[17] = "04:00:00"
        self.hourList[18] = "05:00:00"

        # --> T1 #
        self.hourList[20] = "05:30:00"
        self.hourList[21] = "06:00:00"
        self.hourList[22] = "07:00:00"
        self.hourList[23] = "08:00:00"
        self.hourList[24] = "09:00:00"
        self.hourList[25] = "10:00:00"
        self.hourList[26] = "11:00:00"
        self.hourList[27] = "12:00:00"
        self.hourList[28] = "13:00:00"
        self.hourList[29] = "14:00:00"

        # --> T2 #
        self.hourList[31] = "15:18:00"
        self.hourList[32] = "16:00:00"
        self.hourList[33] = "17:00:00"
        self.hourList[34] = "18:00:00"
        self.hourList[35] = "19:00:00"
        self.hourList[36] = "20:00:00"
        self.hourList[37] = "21:00:00"
        self.hourList[38] = "22:00:00"
        self.hourList[39] = "23:00:00"
        self.hourList[40] = "23:59:59"

    ###############################################################################################################################################################################

    def parseData(self):
        """
        This method parses the data inside the worksheet loaded
        """
        i = 1

        for row in self.workSheet.rows:
            if i < 33:
                i += 1
                continue

            client = str(row[self.CLIENTCOLUMN].value).rstrip()
            aux_product = str(row[self.PRODUCTCOLUMN].value).split("RET-")[-1]
            product = aux_product.split(" - ")[0]
            raw_product = str(row[self.PRODUCTCOLUMN].value)
            location = str(row[self.LOCALCOLUMN].value.rstrip())
            quantity = row[self.QUANTITYCOLUMN].value
            hasTest = row[self.HASTESTCOLUNN].value

            beginningHour = 0

            if client is None and i > 33:
                break

            if self.isInt(quantity) and bool("COM TESTE" in str(hasTest).upper()):
                if int(quantity) > 0:
                    counter = 0
                    for index in self.productionHoursList:
                        if row[index].value is None:
                            continue

                        if self.isInt(row[index].value):
                            if int(row[index].value) > 0:
                                if counter == 0:
                                    beginningHour = index
                                counter += 1
                        else:
                            if bool("SETUP" in str(row[index].value).upper()):
                                if counter == 0:
                                    beginningHour = index
                                counter += 1

                    self.parseList.append(
                        [i, client, product, quantity, self.hourList[beginningHour], counter, raw_product, location])

            i += 1

        return self.parseList

    ###############################################################################################################################################################################

    def isInt(self, message):
        """
        This method is used to check if the number is Int or not
        """
        if message is None:
            return False
        try:
            int(message)
            return True
        except ValueError:
            return False

    ###############################################################################################################################################################################

    def loadWorksheet(self):
        """
        This method parses the file in the file path, extracting relevant
        information that will be inserted to the database later
        """
        try:
            workbook = load_workbook(self.filePath, read_only=True, data_only=True)
            self.workSheet = workbook.worksheets[0]

        except:
            print("Erro durante a abertura da planilha de produção.\n{0} ".format(sys.exc_info()[0]))
            return False

        return True


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class ProdFileOpChecker(object):
    """
    This class is used by mainwindow to check if any production plan was uploaded
    """

    def __init__(self):
        self.lastUpload = ""
        self.uploaded = False

    ###############################################################################################################################################################################

    def checkProductionUpload(self, date=""):
        """
        This method checks if there was uploaded the production plan for the "next day".
        """
        myDBConnection = DBConnection()

        fields = [
            "pdp_id"]

        tables = [
            ("planos_de_producao", "", "")
        ]

        where = [
            "pdp_data >= DATE('" + date + "')"
        ]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where)

        if not querySuccess:
            raise DatabaseConnectionError("Verificação de Envio do Plano de Produção",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        if querySuccess and len(queryResult) > 0:
            return True

        else:
            return False
