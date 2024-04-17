
from magicDB import *

__version__ = "2.0.0"


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class Client(object):
    """
    This class holds data about one client
    """
    def __init__(self, clientId=None, clientName=None, clientResponsible=None, clientActive=None):
        self.clientId = int(clientId)
        self.clientName = clientName
        self.clientResponsible = clientResponsible
        self.clientActive = int(clientActive)

###############################################################################################################################################################################

    def unsetAnalyst(self):
        """
        This method removes the responsible analyst from this client
        """
        
        myDBConnection = DBConnection()
        
        tables = ["clientes"]

        fieldsAndValues = [("cli_responsavel", "NULL")]

        conditions = [
            "cli_id = '" + str(self.clientId) + "'"
            ]
        
        updated, updatedId = myDBConnection.updateQuery(tables, fieldsAndValues, conditions)
        # --> If any error during database connection #
        if not updated:
            raise DatabaseConnectionError("Durante a remoção do analista responsável pelo cliente.",
                                          "Falha ao tentar executar a atualização no banco.\nContate o administrador do sistema.")
            return

        self.clientResponsible = "" 
        
###############################################################################################################################################################################

    def setAnalyst(self, analyst):
        """
        This method sets the analyst responsible for the clients
        """

        myDBConnection = DBConnection()
        
        tables = ["clientes"]

        fieldsAndValues = [("cli_responsavel", str(analyst))]

        conditions = [
            "cli_id = '" + str(self.clientId) + "'"
            ]
        
        updated, updatedId = myDBConnection.updateQuery(tables, fieldsAndValues, conditions)
        # --> If any error during database connection #
        if not updated:
            raise DatabaseConnectionError("Durante a definição do analista responsável pelo cliente.",
                                          "Falha ao tentar executar a atualização no banco.\nContate o administrador do sistema.")
            return

        self.clientResponsible = analyst 

###############################################################################################################################################################################

        
    def setActive(self, state):
        """
        This method sets the state of the client which means if the client is active or not
        """

        myDBConnection = DBConnection()
        
        tables = ["clientes"]

        if state:
            fieldsAndValues = [("cli_ativo", "1")]
        else:
            fieldsAndValues = [("cli_ativo", "0")]

        conditions = [
            "cli_id = '" + str(self.clientId) + "'"
            ]
        
        updated, updatedId = myDBConnection.updateQuery(tables, fieldsAndValues, conditions)
        # --> If any error during database connection #
        if not updated:
            raise DatabaseConnectionError("Durante a mudança de status do cliente.",
                                          "Falha ao tentar executar a atualização no banco.\nContate o administrador do sistema.")
            return
        
        if state:
            self.clientActive = 1
        else:
            self.clientActive = 0

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class ClientsContainer(object):
    """
    This class holds a set of clients
    """
    def __init__(self):
        self.__clients = []
        self.__clientsFromId = {}

###############################################################################################################################################################################

    def loadActiveClients(self):
        """
        This method is called to load all the active clients
        """

        myDBConnection = DBConnection()
        
        fields = [
                "cli_id",
                "cli_nome",
                "cli_responsavel",
                "cli_ativo"
                ]
            
        tables = [("clientes", "", "")]
        
        where = [
            "cli_id > 1",
            "cli_ativo = 1"
            ]
        
        orderby = ["cli_nome ASC"]
        
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, None, None, orderby)

        # --> if any error during database connection #
        if not querySuccess:
            raise DatabaseConnectionError("Durante a listagem de Clientes Ativos.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()

        for clientId, clientName, clientResponsible, clientActive in queryResult:
            client = Client(clientId, clientName, clientResponsible, clientActive)
            self.add(client)


###############################################################################################################################################################################


    def loadClientsWithoutAnalyst(self):
        """
        This method is called to load all the active clients that dont have an analyst related to them
        """

        myDBConnection = DBConnection()
        
        fields = [
                "cli_id",
                "cli_nome",
                "cli_responsavel",
                "cli_ativo"
                ]
            
        tables = [("clientes", "", "")]
        
        where = [
            "cli_id > 1",
            "cli_responsavel IS NULL"
            ]
        
        orderby = ["cli_nome ASC"]
        
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, None, None, orderby)

        # --> if any error during database connection #
        if not querySuccess:
            raise DatabaseConnectionError("Durante a listagem de Clientes Ativos sem Analista.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()

        for clientId, clientName, clientResponsible, clientActive in queryResult:
            client = Client(clientId, clientName, clientResponsible, clientActive)
            self.add(client)

###############################################################################################################################################################################

    def loadClientsFromAnalyst(self, analystId, onlyActives=False):
        """
        This method is called to load all the active clients that dont have an analyst related to them
        """

        myDBConnection = DBConnection()
        
        fields = [
                "cli_id",
                "cli_nome",
                "cli_responsavel",
                "cli_ativo"
                ]
            
        tables = [("clientes", "", "")]
        
        where = [
            "cli_id > 1",
            "cli_responsavel = '" + str(analystId) + "' "
            ]

        if onlyActives:
            where.append("cli_ativo = 1")
        
        orderby = ["cli_nome ASC"]
        
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, None, None, orderby)

        # --> if any error during database connection #
        if not querySuccess:
            raise DatabaseConnectionError("Durante a listagem de clientes de um analista específico.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()

        for clientId, clientName, clientResponsible, clientActive in queryResult:
            client = Client(clientId, clientName, clientResponsible, clientActive)
            self.add(client)

###############################################################################################################################################################################
    
    def add(self, client):
        """
        This method adds a new call to the call list. Returns True if success, False if fail
        """

        if int(client.clientId) in self.__clientsFromId.keys():
            return False

        self.__clients.append([int(client.clientId), client])
        self.__clientsFromId[int(client.clientId)] = client
        return True

###############################################################################################################################################################################

    def clear(self):
        self.__clients = []
        self.__clientsFromId = {}

###############################################################################################################################################################################

    def removeClient(self, clientId, client):
        for row, client in enumerate(self.__clients):
            if client[0] == clientId:
                self.__clients.pop(row)
                break
            
        del(self.__clientsFromId[clientId])

###############################################################################################################################################################################
    
    def clientFromId(self, clientId):
        return self.__clientsFromId[int(clientId)]

###############################################################################################################################################################################

    def __iter__(self):
        for client in iter(self.__clients):
            yield client[1]

###############################################################################################################################################################################

    def __len__(self):
        return len(self.__clients)
