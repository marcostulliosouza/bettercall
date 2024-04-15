from magicDB import *

__version__ = "2.0.0"


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class User(object):
    """
    This class holds data about one user
    """
    def __init__(self, userId=None, userName=None, userLogin=None, userCategory=None):
        self.userId = userId
        self.userName = userName
        self.userLogin = userLogin
        self.userCategory = userCategory


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################



class UsersContainer(object):
    """
    This method holds the set of users
    """
    def __init__(self):
        self.__users = []
        self.__usersFromId = {}

###############################################################################################################################################################################

    def loadAllActiveUsers(self, idUser=None):
        """
        This method is called to load all the active users in the system 
        """
        myDBConnection = DBConnection()
        fields = [
                "col_id",
                "col_nome",
                "col_login",
                "col_categoria"
                ]
            
        tables = [("colaboradores", "", "")]
        
        where = ["col_ativo = 1"]
        
        if idUser is not None:
            where.append("col_id != '" + str(idUser) + "'")
            

        orderby = ["col_nome ASC"]
        
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, None, None, orderby)

        # --> if any error during database connection #
        if not querySuccess:
            raise DatabaseConnectionError("Durante a listagem de usuários.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()

        for userId, userName, userLogin, userCategory in queryResult:
            user = User(userId, userName, userLogin, userCategory)
            self.add(user)


###############################################################################################################################################################################

    def loadCallHelpers(self, callId, userId=None):
        """
        This method is called to load all the active users that can help in a call
        """
        myDBConnection = DBConnection()
        
        fields = [
                "col_id",
                "col_nome",
                "col_login",
                "col_categoria"
                ]
            
        tables = [
            ("colaboradores", "", ""),
            ("atendimentos_chamados", "LEFT", "col_id = atc_colaborador")
            ]

        where = [
            "col_ativo = 1",
            "col_categoria > 1",
            "col_id NOT IN(SELECT atc_colaborador FROM atendimentos_chamados WHERE atc_data_hora_termino IS NULL)",
            "col_id NOT IN(SELECT ajc_colaborador FROM ajudantes_chamados WHERE ajc_chamado = '" + str(callId) + "')"
            ]
        
        if userId is not None:
            where.append("col_id != '" + str(userId) + "'")

        groupby = ["col_id"]
       

        orderby = [
            "col_nome ASC"
            ]
        
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, groupby, None, orderby)

        # --> if any error during database connection #
        if not querySuccess:
            raise DatabaseConnectionError("Durante a listagem de usuários.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return
        
        self.clear()
               
        for userId, userName, userLogin, userCategory in queryResult:
            user = User(userId, userName, userLogin, userCategory)
            self.add(user)


###############################################################################################################################################################################


    def loadTransferCallUsers(self, userId):
        """
        This method is used to load all the users that can answer a call
        """
        myDBConnection = DBConnection()
        
        fields = [
                "col_id",
                "col_nome",
                "col_login",
                "col_categoria"
                ]
            
        tables = [
            ("colaboradores", "", ""),
            ("atendimentos_chamados", "LEFT", "col_id = atc_colaborador")
            ]

        where = [
            "col_ativo = 1",
            "col_categoria > 1",
            "col_id NOT IN(SELECT atc_colaborador FROM atendimentos_chamados WHERE atc_data_hora_termino IS NULL)"
            ]
        
        if userId is not None:
            where.append("col_id != '" + str(userId) + "'")

        groupby = ["col_id"]
       

        orderby = [
            "col_nome ASC"
            ]
        
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, groupby, None, orderby)

        # --> if any error during database connection #
        if not querySuccess:
            raise DatabaseConnectionError("Durante a listagem de usuários.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()
        
        for userId, userName, userLogin, userCategory in queryResult:
            user = User(userId, userName, userLogin, userCategory)
            self.add(user)

###############################################################################################################################################################################

    def loadAnalystsUsers(self):
        """
        This method is used to load all the users that can answer a call
        """
        myDBConnection = DBConnection()
        
        fields = [
                "col_id",
                "col_nome",
                "col_login",
                "col_categoria"
                ]
            
        tables = [
            ("colaboradores", "", "")
            ]

        where = [
            "col_ativo = 1",
            "col_categoria = 20"
            ]
        
        
        orderby = [
            "col_nome ASC"
            ]
        
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, None, None, orderby)

        # --> if any error during database connection #
        if not querySuccess:
            raise DatabaseConnectionError("Durante a listagem de usuários.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()
        
        for userId, userName, userLogin, userCategory in queryResult:
            user = User(userId, userName, userLogin, userCategory)
            self.add(user)
        
###############################################################################################################################################################################

    def add(self, user):
        """
        This method adds a new call to the call list. Returns True if success, False if fail
        """
        if int(user.userId) in self.__usersFromId.keys():
            return False

        self.__users.append([int(user.userId), user])
        self.__usersFromId[int(user.userId)] = user
        return True

###############################################################################################################################################################################

    def clear(self):
        self.__users = []
        self.__usersFromId = {}

###############################################################################################################################################################################
  
    def userFromId(self, userId):
        return self.__usersFromId[int(userId)]

###############################################################################################################################################################################

    def __iter__(self):
        for user in iter(self.__users):
            yield user[1]

###############################################################################################################################################################################

    def __len__(self):
        return len(self.__users)
