from datetime import datetime, timedelta
from magicDB import *

__version__ = "2.0.0"



###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class MaintenanceLog(object):
    """
    This class holds all the needed information about a maintenance
    """
    def __init__(self,
                 maintenanceLogId=None,
                 maintenanceLogDevice=None,
                 maintenanceLogBeginDate=None,
                 maintenanceLogEndDate=None,
                 maintenanceLogType=None,
                 maintenanceLogLastMaintenance=None,
                 maintenanceLogIntervalType=None,
                 maintenanceLogDaysInterval=None,
                 maintenanceLogBoardsInterval=None,
                 maintenanceLogBoardsRunned=None,
                 maintenanceLogTotalBoardsRunned=None,
                 maintenanceLogObservation=None,
                 maintenanceLogUser=None,
                 maintenanceLogStatusId=None                 
                 ):
        self.maintenanceLogId = maintenanceLogId
        self.maintenanceLogDevice = maintenanceLogDevice
        self.maintenanceLogBeginDate = maintenanceLogBeginDate
        self.maintenanceLogEndDate = maintenanceLogEndDate
        self.maintenanceLogType = maintenanceLogType
        self.maintenanceLogLastMaintenance = maintenanceLogLastMaintenance
        self.maintenanceLogIntervalType = maintenanceLogIntervalType
        self.maintenanceLogDaysInterval = maintenanceLogDaysInterval
        self.maintenanceLogBoardsInterval = maintenanceLogBoardsInterval
        self.maintenanceLogBoardsRunned = maintenanceLogBoardsRunned
        self.maintenanceLogTotalBoardsRunned = maintenanceLogTotalBoardsRunned
        self.maintenanceLogObservation = maintenanceLogObservation
        self.maintenanceLogUser = maintenanceLogUser
        self.maintenanceLogStatusId = maintenanceLogStatusId

        

###############################################################################################################################################################################
    def maintenanceDuration(self):
        myDBConnection = DBConnection()

        tables = [("log_manutencao_dispositivo", "", "")]

        fields = ["TIMESTAMPDIFF(MINUTE, lmd_data_hora_inicio, NOW())"]

        where = ["lmd_id = '" + str(self.maintenanceLogId) + "'"]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where)

        if not querySuccess:
            raise DatabaseConnectionError("Durante o carregamento da duração da manutenção.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        return queryResult[0][0]

###############################################################################################################################################################################

    def endMaintenance(self, maintenanceInformation, itemAnswerList):
        """
        This method is called to end a maintenance. It inserts all the form items answers, update the maintenance log information (end date, observation and status)
        and updates the device maintenance info, setting the last maintenance to NOW() and setting to 0 the tested boards.
        """
        myDBConnection = DBConnection()

        queryList = []
        
        #################################
        #### MAINTENANCE ITEM INSERT ####
        #################################
        
        table = "resposta_item_formulario"
                    
        fields = [
                "rif_item",
                "rif_log_manutencao",
                "rif_ok",
                "rif_observacao"
                ]
        values = []

        for itemId, maintenanceLogId, itemOk, itemObservation in itemAnswerList:
            values.append((
                "'" + str(itemId) + "'",
                "'" + str(maintenanceLogId) + "'",
                "'" + str(itemOk) + "'",
                "UPPER('" + itemObservation + "')"
                ))
               
                
        queryList.append(myDBConnection.insertQuery(table, fields, values, queryBuild=True))

        ############################################
        #### UPDATE THE DEVICE INFO MAINTENANCE ####
        ############################################

        tables = ["dispositivo_info_manutencao"]
        
        fieldsAndValues = [
            ("dim_placas_executadas", "'0'"),
            ("dim_data_ultima_manutencao", "NOW()")
            ]
         
        conditions = [
            "dim_id = '" + str(maintenanceInformation["deviceInfoMaintenance"]) + "'"
            ]
        
        queryList.append(myDBConnection.updateQuery(tables, fieldsAndValues, conditions, queryBuild=True))

        ###############################################
        #### UPDATE DE MAINTENANCE LOG INFORMATION ####
        ###############################################
        tables = ["log_manutencao_dispositivo"]
        
        fieldsAndValues = [
            ("lmd_data_hora_fim", "NOW()"),
            ("lmd_observacao", "UPPER('" + maintenanceInformation["observation"] + "')"),
            ("lmd_status", "'2'")
            ]
         
        conditions = [
            "lmd_id = '" + str(self.maintenanceLogId) + "'"
            ]
        
        queryList.append(myDBConnection.updateQuery(tables, fieldsAndValues, conditions, queryBuild=True))
        

        querySuccess = myDBConnection.aglutinatedQuery(queryList)
 
        if not querySuccess:
           raise DatabaseConnectionError("Durante a Finalização do Log de Manutenção.",
                                         "Falha ao tentar executar a query composta.\nContate o administrador do sistema.")
           return
       
        

###############################################################################################################################################################################

    def startMaintenance(self):
        """
        This method starts the maintenance 
        """
        myDBConnection = DBConnection()

        table = "log_manutencao_dispositivo"
                    
        fields = [
                "lmd_dispositivo",
                "lmd_data_hora_inicio",
                "lmd_tipo_manutencao",
                "lmd_ciclos_totais_executados",
                "lmd_data_hora_ultima_manutencao",
                "lmd_tipo_intervalo_manutencao",
                "lmd_intervalo_dias",
                "lmd_intervalo_placas",
                "lmd_placas_executadas",
                "lmd_colaborador",
                "lmd_status"
                ]

        values = [(
            "'" + str(self.maintenanceLogDevice) + "'",
            "NOW()",
            "'PREVENTIVA'",
            "'" + str(self.maintenanceLogTotalBoardsRunned) + "'",
            "'" + str(self.maintenanceLogLastMaintenance) + "'",
            "'" + str(self.maintenanceLogIntervalType) + "'",
            "'" + str(self.maintenanceLogDaysInterval) + "'",
            "'" + str(self.maintenanceLogBoardsInterval) + "'",
            "'" + str(self.maintenanceLogBoardsRunned) + "'",
            "'" + str(self.maintenanceLogUser) + "'",
            "'1'"
            )]
           
                
        querySuccess, insertId = myDBConnection.insertQuery(table, fields, values)

        if not querySuccess:
            raise DatabaseConnectionError("Durante a inicialização do log de Manutenção.",
                                          "Falha ao tentar executar a inserção no banco.\nContate o administrador do sistema.")
            return

        self.maintenanceLogId = insertId


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MaintenanceLogsContainer(object):
    """
    This class holds a set of products
    """

    def __init__(self):
        self.__maintenanceLogs = []
        self.__maintenanceLogsFromId = {}



###############################################################################################################################################################################

    def verifyAnyOpenedMaintenance(self, userId):
        myDBConnection = DBConnection()

        fields = ["lmd_dispositivo, lmd_id"]

        tables = [("log_manutencao_dispositivo", "", "")]

        where = [
                "lmd_colaborador = '" + str(userId) + "'",
                "lmd_status = '1'"
                ]
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where)

        if not querySuccess:
            raise DatabaseConnectionError("Durante o carregamento dos dispositivos.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        if len(queryResult):
            return(queryResult[0])
        else:
            return (None, None)
        
###############################################################################################################################################################################

    def add(self, maintenanceLog):
        """
        This method adds a new call to the call list. Returns True if success, False if fail
        """
        if int(maintenanceLog.maintencanceLogId) in self.__maintenanceLogsFromId.keys():
            return False

        self.__maintenanceLogs.append([int(maintenanceLog.maintencanceLogId), maintenanceLog])
        self.__maintenanceLogsFromId[int(maintenanceLog.maintencanceLogId)] = maintenanceLog
        return True

###############################################################################################################################################################################

    def clear(self):
        self.__maintenanceLogs = []
        self.__maintenanceLogsFromId = {}


###############################################################################################################################################################################
    
    def maintenanceLogFromId(self, maintenanceLogId):
        return self.__maintenanceLogsFromId[int(maintenanceLogId)]

###############################################################################################################################################################################

    def __iter__(self):
        for maintenanceLog in iter(self.__maintenanceLogs):
            yield maintenanceLog[1]

###############################################################################################################################################################################

    def __len__(self):
        return len(self.__maintenanceLogs)
