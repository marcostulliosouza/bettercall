from magicDB import *
from myExceptions import *

__version__ = "2.0.0"


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MaintenanceFormItem(object):
    """
    This method holds information about a single form item
    """
    def __init__(self, itemId=None, itemForm=None, itemDescription=None, itemPosition=None):
        self.itemId = int(itemId)
        self.itemForm = itemForm
        self.itemDescription = itemDescription
        self.itemPosition = itemPosition
               

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MaintenanceFormItemsContainer(object):
    """
    This method holds a set of items from an especific maintenance form
    """
    def __init__(self, formId):
        self.__formId = int(formId)
        self.__maintenanceFormItems = []
        self.__maintenanceFormItemsFromId = {}

###############################################################################################################################################################################

    def loadItemsFromMaintenanceForm(self):
        """
        This method loads all the items from a given form
        """
        myDBConnection = DBConnection()
        
        fields = [
                "ifm_id",
                "ifm_formulario",
                "UPPER(ifm_descricao)",
                "ifm_posicao"
                ]
            
        tables = [
            ("itens_formulario_manutencao", "", "")
            ]

        where = [
            "ifm_formulario = '" + str(self.__formId) + "'"
            ]
        
                
        orderby = ["ifm_posicao ASC"]
        
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, None, None, orderby)

        
        # --> if any error during database connection #
        if not querySuccess:
            raise DatabaseConnectionError("Durante a listagem dos Ítens do Formulário de Manutenção Selecionado.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()
        for formItemId, formId, formItemDescription, formItemPosition in queryResult:
            maintenanceFormItem = MaintenanceFormItem(formItemId, formId, formItemDescription, formItemPosition)
            self.add(maintenanceFormItem)


###############################################################################################################################################################################
    
    def add(self, maintenanceFormItem):
        """
        This method adds a new form to the maintenance form list. Returns True if success, False if fail
        """

        if int(maintenanceFormItem.itemId) in self.__maintenanceFormItemsFromId.keys():
            return False

        self.__maintenanceFormItems.append([int(maintenanceFormItem.itemId), maintenanceFormItem])
        self.__maintenanceFormItemsFromId[int(maintenanceFormItem.itemId)] = maintenanceFormItem
        return True

###############################################################################################################################################################################

    def clear(self):
        self.__maintenanceFormItems = []
        self.__maintenanceFormItemsFromId = {}

###############################################################################################################################################################################
    
    def maintenanceFormItemFromId(self, itemId):
        return self.__maintenanceFormItemsFromId[int(itemId)]

###############################################################################################################################################################################

    def __iter__(self):
        for maintenanceFormItem in iter(self.__maintenanceFormItems):
            yield maintenanceFormItem[1]

###############################################################################################################################################################################

    def __len__(self):
        return len(self.__maintenanceFormItems)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MaintenanceForm(object):
    """
    This method holds data and methods from a single maintenance form
    """
    def __init__(self, formId=None, formDescription=None, formLastModification=None, formModifier=None):
        self.formId = 0
        self.formDescription = formDescription
        self.formLastModification = formLastModification
        self.formModifier = formModifier
        self.formItemsList = []

        if formId:
            self.formId = int(formId)
            self.formItemsList = MaintenanceFormItemsContainer(formId)

    def insertNewForm(self, formDescription, modifierUser, itemsInsertList):
        queryList = []
        myDBConnection = DBConnection()

        table = "formularios_manutencao_preventiva"
                    
        fields = [
                "fmp_descricao",
                "fmp_data_ultima_modificacao",
                "fmp_modificador"
                ]

        values = [("UPPER('" + str(formDescription) + "')", "NOW()", "'" + str(modifierUser) + "'")]
           
                
        queryList.append(myDBConnection.insertQuery(table, fields, values, queryBuild=True))


        table = "itens_formulario_manutencao"
                    
        fields = [
                "ifm_formulario",
                "ifm_descricao",
                "ifm_posicao"
                ]

        values = []
            
        for item in itemsInsertList:
            values.append(("LAST_INSERT_ID()", "UPPER('"+item[0]+"')", "'" + str(item[1]) + "'"))
                
        queryList.append(myDBConnection.insertQuery(table, fields, values, queryBuild=True))
        
        querySuccess = myDBConnection.aglutinatedQuery(queryList)
 
        if not querySuccess:
            raise DatabaseConnectionError("Durante a criação de um novo formulário.",
                                          "Falha ao tentar executar a inserção no banco.\nContate o administrador do sistema.")
            return

        
    def updateFormItems(self, newDescription, modifierUser, itemsInsertList, itemsUpdateList, itemsDeleteList):
        """
        Method used to update the form itens
        """
        
        queryList = []
        myDBConnection = DBConnection()

        # --> create the insert query
        if len(itemsInsertList):
            
            table = "itens_formulario_manutencao"
                    
            fields = [
                    "ifm_formulario",
                    "ifm_descricao",
                    "ifm_posicao"
                    ]

            values = []
            
            for item in itemsInsertList:
                values.append(("'" + str(self.formId) + "'", "UPPER('"+item[0]+"')", "'" + str(item[1]) + "'"))
                
            queryList.append(myDBConnection.insertQuery(table, fields, values, queryBuild=True))

        if len(itemsUpdateList):

            # --> create the update query
            tables = ["itens_formulario_manutencao"]

            for item in itemsUpdateList:
                fieldsAndValues = [
                    ("ifm_formulario", "'" + str(self.formId) + "'"),
                    ("ifm_descricao", "'" + item[1] + "'"),
                    ("ifm_posicao", "'" + str(item[2]) + "'")
                    ]

                where = ["ifm_id = '" + str(item[0]) + "'"]

                queryList.append(myDBConnection.updateQuery(tables, fieldsAndValues, where, queryBuild=True))
            
        # --> create the delete query
        if len(itemsDeleteList):

            table = ["itens_formulario_manutencao"]
            
            for itemId in itemsDeleteList:
                condition = ["ifm_id = '" + str(itemId) + "'"]

                queryList.append(myDBConnection.deleteQuery(table, condition, queryBuild=True))

        # --> create the update query for the form information
        tables = ["formularios_manutencao_preventiva"]

        fieldsAndValues = [
            ("fmp_descricao", "UPPER('" + newDescription + "')"),
            ("fmp_data_ultima_modificacao", "NOW()"),
            ("fmp_modificador", "'" + str(modifierUser) + "'")
            ]

        where = ["fmp_id = '" + str(self.formId) + "'"]

        queryList.append(myDBConnection.updateQuery(tables, fieldsAndValues, where, queryBuild=True))
        
        querySuccess = myDBConnection.aglutinatedQuery(queryList)
 
        if not querySuccess:
            raise DatabaseConnectionError("Durante a atualização dos dados do Formulário.",
                                          "Falha ao tentar executar a inserção no banco.\nContate o administrador do sistema.")
            return

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class MaintenanceFormsContainer(object):
    """
    This class holds a set of maintenance forms
    """
    def __init__(self):
        self.__maintenanceForms = []
        self.__maintenanceFormsFromId = {}

###############################################################################################################################################################################
    def loadMaintenanceForms(self):
        """
        This method is used to load all the registered forms
        """
        myDBConnection = DBConnection()
        
        fields = [
                "fmp_id",
                "fmp_descricao",
                "DATE_FORMAT(fmp_data_ultima_modificacao, '%d/%m/%Y') as fmp_data_ultima_modificacao",
                "col_nome"
                ]
            
        tables = [
            ("formularios_manutencao_preventiva", "", ""),
            ("colaboradores", "LEFT", "fmp_modificador = col_id")
            ]
        
                
        orderby = ["fmp_descricao ASC"]
        
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, None, None, None, orderby)

        # --> if any error during database connection #
        if not querySuccess:
            raise DatabaseConnectionError("Durante a listagem dos Formularios de Manutenção Preventiva.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()
        for formId, formDescription, formLastModification, formModifier in queryResult:
            maintenanceForm = MaintenanceForm(formId, formDescription, formLastModification, formModifier)
            self.add(maintenanceForm)



###############################################################################################################################################################################
    
    def add(self, maintenanceForm):
        """
        This method adds a new form to the maintenance form list. Returns True if success, False if fail
        """

        if int(maintenanceForm.formId) in self.__maintenanceFormsFromId.keys():
            return False

        self.__maintenanceForms.append([int(maintenanceForm.formId), maintenanceForm])
        self.__maintenanceFormsFromId[int(maintenanceForm.formId)] = maintenanceForm
        return True

###############################################################################################################################################################################

    def clear(self):
        self.__maintenanceForms = []
        self.__maintenanceFormsFromId = {}

###############################################################################################################################################################################
    
    def maintenanceFormFromId(self, formId):
        return self.__maintenanceFormsFromId[int(formId)]

###############################################################################################################################################################################

    def __iter__(self):
        for maintenanceForm in iter(self.__maintenanceForms):
            yield maintenanceForm[1]

###############################################################################################################################################################################

    def __len__(self):
        return len(self.__maintenanceForms)
