from magicDB import *

from myExceptions import *

__version__ = "2.0.0"

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class Invoice(object):
    """
    This class holds all the information about a uploaded Receipt
    """
    def __init__(self,
                 invoiceId="",
                 invoiceNumber="",
                 invoiceClientId="",
                 invoiceClientName="",
                 invoiceDocSAP="",
                 invoiceRecordDate="",
                 invoiceHasReturn="",
                 invoiceReturnDate="",
                 remainingDays=""):

        self.invoiceId = invoiceId
        self.invoiceNumber = invoiceNumber
        self.invoiceClientId = invoiceClientId
        self.invoiceClientName = invoiceClientName

        self.invoiceDocSAP = invoiceDocSAP
        self.invoiceRecordDate = invoiceRecordDate
        self.invoiceHasReturn = invoiceHasReturn
        self.invoiceReturnDate = invoiceReturnDate

        self.remainingDays = remainingDays


###############################################################################################################################################################################

    def formatDateForDB(self, date):
        """
        This method formats the date to the format friendly to the DB
        """
  
        splitDate =  date.split("/")
        formatedDate = splitDate[2] + "-" + splitDate[1] + "-" +splitDate[0]

        return formatedDate

###############################################################################################################################################################################
   
    def insertNewInvoice(self):
        """
        This method is used to insert the new Invoice into the database
        """
        myDBConnection = DBConnection()
       
        if int(self.invoiceHasReturn) == 1:
            returnDate = "'" + self.formatDateForDB(self.invoiceReturnDate) + "'"
        else:
            returnDate = "NULL"
                
        table = "notas_fiscais"

        fields = [
            "nof_numero",
            "nof_cliente",
            "nof_doc_sap",
            "nof_data_hora_cadastro",
            "nof_com_retorno",
            "nof_data_retorno"
            ]

        values = [
            ("'" + str(self.invoiceNumber) + "'",
             "'" + str(self.invoiceClientId)  + "'",
             "'" + str(self.invoiceDocSAP) + "'",
             "NOW()",
             "'" + str(self.invoiceHasReturn) + "'",
             returnDate)
            ]

        
        inserted, insertedId = myDBConnection.insertQuery(table, fields, values)

        if not inserted:
            raise DatabaseConnectionError("Durante a inserção dos dados da nota fiscal no banco.",
                                          "Falha ao tentar executar a inserção no banco.\nContate o administrador do sistema.")
            return

        return
        

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class InvoicesContainer(object):
    """
    This class is a container that holds all the Receipts as a List
    """
    def __init__(self):
        self.__invoices = []
        self.__invoicesFromId = {}

###############################################################################################################################################################################

    def loadInvoices(self, filtering=False, filteringFields=None):
        """
        This method is used to load the invoices from clients using data passed
        as filter if it is filtering
        """
        myDBConnection = DBConnection()
        
        fields = [
            "nof_id",
            "nof_numero",
            "nof_cliente",
            "cli_nome",
            "nof_doc_sap",
            "DATE_FORMAT(nof_data_hora_cadastro, '%d/%m/%Y') AS nof_data_cadastro",
            "nof_com_retorno",
            "DATE_FORMAT(nof_data_retorno, '%d/%m/%Y') AS nof_data_hora_retorno",
            "IF(nof_data_retorno IS NOT NULL, DATEDIFF(nof_data_retorno, NOW()), 0) AS remaining_days"
            ]

        tables = [
            ("notas_fiscais", "", ""),
            ("clientes", "LEFT", "nof_cliente = cli_id")        
            ]


        if not filtering:
            where = [
                "DATE(NOW()) >=  CURDATE() - INTERVAL 1 MONTH",
                "DATE(NOW()) <=  CURDATE()"
                ]
            limit = ["1000"]
        else:
            limit = None
            where = filteringFields

        orderBy = ["nof_data_hora_cadastro DESC"]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, orderby=orderBy)

        if not querySuccess:
            raise DatabaseConnectionError("Seleção das Notas Fiscais na tela de Listagem de Notas Fiscais",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()
        
        for (
            invoiceId,
            invoiceNumber,
            invoiceClientId,
            invoiceClientName,
            invoiceDocSAP,
            invoiceRecordDate,
            invoiceHasReturn,
            invoiceReturnDate,
            remainingDays
            )in queryResult:
        
            invoice = Invoice(
                              invoiceId,
                              invoiceNumber,
                              invoiceClientId,
                              invoiceClientName,
                              invoiceDocSAP,
                              invoiceRecordDate,
                              invoiceHasReturn,
                              invoiceReturnDate,
                              remainingDays
                             )
            self.add(invoice)

###############################################################################################################################################################################


    def add(self, invoice):
        """
        This method adds a new call to the call list. Returns True if success, False if fail
        """
        if int(invoice.invoiceId) in self.__invoicesFromId.keys():
            return False

        self.__invoices.append([int(invoice.invoiceId), invoice])
        self.__invoicesFromId[int(invoice.invoiceId)] = invoice
        return True

###############################################################################################################################################################################

    def clear(self):
        self.__invoices = []
        self.__invoicesFromId = {}

###############################################################################################################################################################################

    def invoiceFromId(self, invoiceId):
        return self.__invoicesFromId[int(invoiceId)]    

###############################################################################################################################################################################

    def __iter__(self):
        for invoice in iter(self.__invoices):
            yield invoice[1]

###############################################################################################################################################################################

    def __len__(self):
        return len(self.__invoices)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class InvoiceChecker(object):
    """
    This class is used to check if an especific invoice was already uploaded
    """

    def __init__(self):
        self.uploaded = False


###############################################################################################################################################################################

    def checkInvoiceUpload(self, invoiceNumber=0, invoiceClient=0):
        """
        This method verifies if the invoice was already uploaded
        """
        myDBConnection = DBConnection()

        fields = ["nof_id"]

        tables = [
            ("notas_fiscais", "", "")
            ]

        where = [
            "nof_numero = '" + str(invoiceNumber) + "'",
            "nof_cliente = '" + str(invoiceClient) + "'"
            ]

        
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where)

        if not querySuccess:
            raise DatabaseConnectionError("Verificação de Envio da Nota Fiscal",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return
            
        if querySuccess and len(queryResult) > 0:    
            return True
        
        else:
            return False



        
