import os
import configparser
from shutil import copyfile
from ftplib import FTP

from magicDB import *
from myExceptions import *

__version__ = "2.0.0"


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class Device(object):
    """
    This class holds the information about one call type
    """
    def __init__(self,
                 deviceId,
                 deviceDescription,
                 deviceSAPCode,
                 deviceClientId,
                 deviceClientName,
                 deviceInvoiceNumber,
                 deviceStatusId,
                 deviceStatusDescription,
                 deviceDocSent,
                 deviceHasImage,
                 deviceImageExtension,
                 deviceOutInvoiceNumber,
                 deviceInOutInvoiceId,
                 deviceHasMaintenance,
                 deviceInfoMaintenance,
                 deviceFunction=None):
        
        self.deviceId = int(deviceId)
        self.deviceDescription = deviceDescription
        self.deviceSAPCode = deviceSAPCode if(deviceSAPCode) else ""

        if deviceClientId:
            self.deviceClientId = int(deviceClientId)
            self.deviceClientName = deviceClientName
        else:
            self.deviceClientId = 0
            self.deviceClientName = "HI-MIX"
            
        if deviceInvoiceNumber:
            self.deviceInvoiceNumber = int(deviceInvoiceNumber)
        else:
            self.deviceInvoiceNumber = 0

        if deviceOutInvoiceNumber:
            self.deviceOutInvoiceNumber = int(deviceOutInvoiceNumber)
        else:
            self.deviceOutInvoiceNumber = 0
        
        
        self.deviceStatusId = int(deviceStatusId)
        self.deviceStatusDescription = deviceStatusDescription
        self.deviceDocSent = deviceDocSent
        self.deviceHasImage = deviceHasImage
        self.deviceImageExtension = deviceImageExtension
        self.deviceInOutInvoiceId = deviceInOutInvoiceId
        self.deviceHasMaintenance = int(deviceHasMaintenance)
        self.deviceInfoMaintenance = int(deviceInfoMaintenance) if deviceInfoMaintenance else 0

        #field acessed just in the device - product vinculation screen
       
        self.deviceFunction = deviceFunction

        self.deviceLastMaintenance = ""

        self.vinculatedProductsList = []

###############################################################################################################################################################################

    def isInvoiceRelated(self, invoiceId):
        """
        This method returns the last Invoice ID from the device.
        If there is no invoice it returns 0

        """
        myDBConnection = DBConnection()
        
        fields = ["*"]

        tables = [("entrada_saida_equipamento", "", "")]

        where = [
                "ese_dispositivo = '" + str(self.deviceId) + "'",
                "ese_nota_fiscal_entrada = '" + str(invoiceId) + "'"
                ]

        
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where)

        if not querySuccess:
            raise DatabaseConnectionError("Durante o carregamento dos dispositivos.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        if len(queryResult):
            return True
        else:
            return False

###############################################################################################################################################################################
    def loadVinculatedProducts(self):
        """
        This method is responsible for loading the name and function of all vinculated products to this device
        """
        myDBConnection = DBConnection()

        fields = [
            "pro_nome",
            "feq_descricao"            
            ]

        tables = [
            ("vinculacao_dispositivo_produto", "", ""),
            ("produtos", "LEFT", "vdp_produto = pro_id"),
            ("funcoes_equipamento", "LEFT", "vdp_funcao_dispositivo = feq_id")
            ]

        where = [
            "vdp_dispositivo = '" + str(self.deviceId) + "'"
            ]

        orderby = ["pro_nome ASC", "feq_id ASC"]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, None, None, orderby)

        if not querySuccess:
            raise DatabaseConnectionError("Durante o carregamento dos dispositivos.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.vinculatedProductsList = []
        for productName, deviceFunction in queryResult:
            self.vinculatedProductsList.append((productName, deviceFunction))    
        
###############################################################################################################################################################################

    def loadMaintenanceData(self):
        """
        This method is used to load all the required data to be shown in the preemptive maintenance window
        """
        myDBConnection = DBConnection()
        
        fields = [
            "dis_info_manutencao",
            "dim_tipo_intervalo",
            "dim_intervalo_dias",
            "dim_intervalo_placas",
            "dim_placas_executadas",
            "dim_data_ultima_manutencao",
            "IF(dim_tipo_intervalo = 'PLACA', "\
            "   (dim_placas_executadas/dim_intervalo_placas)*100, "\
            "   (DATEDIFF(NOW(), dim_data_ultima_manutencao)/dim_intervalo_dias)*100) AS porcentagem_proxima_manutencao",
            "IF(dim_tipo_intervalo = 'PLACA', "\
            "   (dim_intervalo_placas - dim_placas_executadas), "\
            "   (dim_intervalo_dias - DATEDIFF(NOW(), dim_data_ultima_manutencao))) AS proxima_manutencao",
            ]

        tables = [
            ("dispositivos", "", ""),
            ("dispositivo_info_manutencao", "LEFT", "dis_info_manutencao = dim_id")   
            ]

        where = [
            "dis_id = '" + str(self.deviceId) + "'"
            ]

        orderby = ["porcentagem_proxima_manutencao DESC"]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, None, None, orderby)

        if not querySuccess:
            raise DatabaseConnectionError("Durante o carregamento dos dados de manutenção dispositivo.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return
        
        self.deviceInfoMaintenance = int(queryResult[0][0]) if queryResult[0][0] else 0
        self.deviceMaintenanceIntervalType = queryResult[0][1]
        self.deviceMaintenanceDaysInterval = int(queryResult[0][2]) if queryResult[0][2] else 0
        self.deviceMaintenanceBoardsInterval = int(queryResult[0][3]) if queryResult[0][3] else 0
        self.deviceBoardsRunned = int(queryResult[0][4]) if queryResult[0][4] else 0
        self.deviceLastMaintenance = str(queryResult[0][5]) if queryResult[0][5] else "NUNCA"
        self.devicePercentageMaintenance = float(queryResult[0][6]) if queryResult[0][6] else 0

        if self.deviceMaintenanceIntervalType == "PLACA":
            self.deviceNextMaintenance = "EM " + str(queryResult[0][7]) + " PLACAS."
        else:
            self.deviceNextMaintenance = "EM " + str(queryResult[0][7]) + " DIAS."
            

###############################################################################################################################################################################

    def loadAllDetailedData(self):
        """
        This method is used to load all the remaining data that wasn't loaded in the device list window
        """
        myDBConnection = DBConnection()
        
        fields = [
            "dis_descricao",
            "dis_codigo_sap",
            "nof_numero",
            "dis_status",
            "sdi_descricao",
            "dis_ciclos_de_vida",
            "dis_posicao_estoque",
            "dis_ciclos_executados",
            "dis_observacao",
            "dis_com_imagem",
            "dis_extensao_imagem",
            "dis_doc_enviado",
            "dis_com_manutencao",
            "dis_info_manutencao",
            "dim_tipo_intervalo",
            "dim_intervalo_dias",
            "dim_intervalo_placas",
            "dim_placas_executadas",
            "dim_formulario_manutencao",
            "fmp_descricao",
            "dis_data_cadastro"
            ]

        tables = [
            ("dispositivos", "", ""),
            ("entrada_saida_equipamento", "LEFT", "dis_nota_fiscal_atual = ese_id"),
            ("notas_fiscais", "LEFT", "ese_nota_fiscal_entrada = nof_id"),
            ("status_dispositivo", "LEFT", "dis_status = sdi_id"),
            ("dispositivo_info_manutencao", "LEFT", "dis_info_manutencao = dim_id"),
            ("formularios_manutencao_preventiva", "LEFT", "dim_formulario_manutencao = fmp_id")
            ]

        where = [
            "dis_id = '" + str(self.deviceId) + "'"
            ]

        orderby = ["dis_id DESC", "ese_id DESC", "nof_data_hora_cadastro DESC"]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, None, None, orderby)

        if not querySuccess:
            raise DatabaseConnectionError("Durante o carregamento dos dispositivos.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.deviceDescription = queryResult[0][0]
        self.deviceSAPCode = queryResult[0][1] if(queryResult[0][1]) else ""

        if queryResult[0][2]:
            self.deviceInvoiceNumber = int(queryResult[0][2])

        self.deviceStatusId = int(queryResult[0][3])
        self.deviceStatusDescription = queryResult[0][4]
        self.deviceLifeCicle = int(queryResult[0][5])
        self.deviceStoragePosition = queryResult[0][6]
        self.deviceRunnedCicles = queryResult[0][7]
        self.deviceObservation = queryResult[0][8]
        self.deviceHasImage = int(queryResult[0][9])
        self.deviceImageExtension = queryResult[0][10]
        self.deviceDocSent = int(queryResult[0][11])
        self.deviceHasMaintenance = int(queryResult[0][12])
        self.deviceInfoMaintenance = int(queryResult[0][13]) if queryResult[0][13] else 0
        self.deviceMaintenanceIntervalType = queryResult[0][14]
        self.deviceMaintenanceDaysInterval = int(queryResult[0][15]) if queryResult[0][15] else 0
        self.deviceMaintenanceBoardsInterval = int(queryResult[0][16]) if queryResult[0][16] else 0
        self.deviceBoardsRunned = int(queryResult[0][17]) if queryResult[0][17] else 0
        self.deviceMaintenanceFormId = int(queryResult[0][18]) if queryResult[0][18] else 0
        self.deviceMaintenanceFormDescription = queryResult[0][19]
        self.deviceRegisterDate = queryResult[0][20]


###############################################################################################################################################################################

    def removeDeviceVinculationToProduct(self, productId):
        """
        This method is used to remove the vinculation between the device and the product. It removes all the entry that contains this device in the
        vinculacao_dispositivo_produto for the indicated product Id
        """
        myDBConnection = DBConnection()
        
        tables = ["vinculacao_dispositivo_produto"]
      

        conditions = [
            "vdp_produto = '" + str(productId) + "'",
            "vdp_dispositivo = '" + str(self.deviceId) + "'"
            ]

        deleted, deletedId = myDBConnection.deleteQuery(tables, conditions)

        if not deleted:
            raise DatabaseConnectionError("Durante a remoção da vinculação de um dispositivo a um produto.",
                                          "Falha ao tentar executar a remoção no banco.\nContate o administrador do sistema.")
            return


###############################################################################################################################################################################


    def updateDeviceInformation(self, dataDictionary):
        """
        This method is used to update the device information inside the database
        """
        queryList = []
        querySuccess = False
                
        myDBConnection = DBConnection()

        ################################
        #### DEVICE HAS MAINTENANCE ####
        ################################

        #print(dataDictionary)
        
        if dataDictionary["hasMaintenance"]:
            
            #####################################################################
            #--> IF THE DEVICE DIDN'T HAVE A REGISTERED MAINTENANCE INFORMATION #
            #####################################################################
            if not self.deviceInfoMaintenance:
                table = "dispositivo_info_manutencao"
                
                if dataDictionary["maintenanceType"] == "DIA":
                    fields = ["dim_tipo_intervalo", "dim_intervalo_dias", "dim_data_ultima_manutencao", "dim_formulario_manutencao"]
                    values = [("'DIA'", dataDictionary["maintenanceInterval"], "NOW()", dataDictionary["maintenanceForm"])]
                else:
                    fields = ["dim_tipo_intervalo", "dim_intervalo_placas", "dim_formulario_manutencao"]
                    values = [("'PLACA'", dataDictionary["maintenanceInterval"], dataDictionary["maintenanceForm"])]

                queryList.append(myDBConnection.insertQuery(table, fields, values, queryBuild=True))

                #--> UPDATE THE DEVICE INFORMATION #
                fieldsAndValues = [
                    ("dis_status", dataDictionary["status"]),
                    ("dis_codigo_sap", "UPPER(" + dataDictionary["SAPCode"] + ")"),
                    ("dis_ciclos_de_vida", dataDictionary["lifecicle"]),
                    ("dis_posicao_estoque", "UPPER(" + dataDictionary["storage"] + ")"),
                    ("dis_observacao", "UPPER(" + dataDictionary["observation"] + ")"),
                    ("dis_com_manutencao", "'1'"),
                    ("dis_info_manutencao", "LAST_INSERT_ID()")
                ]

            ###########################################################
            #--> IF THE DEVICE ALREADY HAS AN MAINTENANCE INFORMATION #
            ###########################################################
            else:
                tables = ["dispositivo_info_manutencao"]

                if dataDictionary["maintenanceType"] == "DIA":
                    fieldsAndValues = [
                        ("dim_tipo_intervalo", "'DIA'"),
                        ("dim_intervalo_dias", dataDictionary["maintenanceInterval"]),
                        ("dim_data_ultima_manutencao", "NOW()"),
                        ("dim_formulario_manutencao", dataDictionary["maintenanceForm"])
                    ]
                    
                else:
                    fieldsAndValues = [
                        ("dim_tipo_intervalo", "'PLACA'"),
                        ("dim_intervalo_placas", dataDictionary["maintenanceInterval"]),
                        ("dim_placas_executadas", "'0'"),
                        ("dim_data_ultima_manutencao", "NOW()"),
                        ("dim_formulario_manutencao", dataDictionary["maintenanceForm"])
                    ]

                conditions = ["dim_id = '" + str(self.deviceInfoMaintenance) + "'"]

                queryList.append(myDBConnection.updateQuery(tables, fieldsAndValues, conditions, queryBuild=True))

                #--> UPDATE THE DEVICE INFORMATION #
                fieldsAndValues = [
                    ("dis_status", dataDictionary["status"]),
                    ("dis_codigo_sap", "UPPER(" + dataDictionary["SAPCode"] + ")"),
                    ("dis_ciclos_de_vida", dataDictionary["lifecicle"]),
                    ("dis_posicao_estoque", "UPPER(" + dataDictionary["storage"] + ")"),
                    ("dis_observacao", "UPPER(" + dataDictionary["observation"] + ")"),
                    ("dis_com_manutencao", "'1'")
                ]

        #########################################
        #### DEVICE DOESN'T HAVE MAINTENANCE ####
        #########################################
        
        else:
            ####################################
            #--> UPDATE THE DEVICE INFORMATION #
            ####################################
            fieldsAndValues = [
                ("dis_status", dataDictionary["status"]),
                ("dis_codigo_sap", "UPPER(" + dataDictionary["SAPCode"] + ")"),
                ("dis_ciclos_de_vida", dataDictionary["lifecicle"]),
                ("dis_posicao_estoque", "UPPER(" + dataDictionary["storage"] + ")"),
                ("dis_observacao", "UPPER(" + dataDictionary["observation"] + ")"),
                ("dis_com_manutencao", "'0'")
            ]

            
        tables = ["dispositivos"]
        conditions = ["dis_id = '" + str(self.deviceId) + "'"]

        queryList.append(myDBConnection.updateQuery(tables, fieldsAndValues, conditions, queryBuild=True))

        querySuccess = myDBConnection.aglutinatedQuery(queryList)
 
        if not querySuccess:
           raise DatabaseConnectionError("Durante a atualização dos dados do dispositivo.",
                                         "Falha ao tentar executar a atualização do dispositivo.\nContate o administrador do sistema.")
           return
    
###############################################################################################################################################################################

    def saveOrUpdateDeviceImage(self, newImagePath):

        myDBConnection = DBConnection()

        parser = configparser.SafeConfigParser()
        parser.read("dbconfig.ini")
        FTPPath = parser.get("ftp", "path")
        FTPUser = parser.get("ftp", "user")
        FTPPass = parser.get("ftp", "pass")

        extension = newImagePath.split(".")[-1]
        
        destinationFileName = str(self.deviceId) + "." + extension

        file = open(newImagePath, "rb")

        try:
            ftp = FTP(FTPPath)
            ftp.login(FTPUser, FTPPass)
            ftp.cwd("dis")
            ftp.storbinary("STOR " + destinationFileName, file)

            file.close()
            ftp.quit()
        except Exception as e:
            raise DatabaseConnectionError("Durante a atualização do documento de instalação do dispositivo.",
                                          "Falha ao enviar o arquivo ao FTP.\nContate o administrador do sistema.")
            return 
        

        tables = ["dispositivos"]

        fieldsAndValues = [
                ("dis_com_imagem", "'1'"),
                ("dis_extensao_imagem", "'" + extension + "'")
            ]

        conditions = ["dis_id = '" + str(self.deviceId) + "'"]

        updated, updatedId = myDBConnection.updateQuery(tables, fieldsAndValues, conditions)

        # --> If any error during database connection #
        if not updated:
            raise DatabaseConnectionError("Durante a atualização da imagem do dispositivo.",
                                          "Falha ao tentar executar a atualização no banco.\nContate o administrador do sistema.")
            return 

        self.deviceHasImage = 1
        self.deviceImageExtension = extension

###############################################################################################################################################################################

    def saveOrUpdateDeviceDoc(self, newDocPath):

        myDBConnection = DBConnection()

        parser = configparser.SafeConfigParser()
        parser.read("dbconfig.ini")
        FTPPath = parser.get("ftp", "path")
        FTPUser = parser.get("ftp", "user")
        FTPPass = parser.get("ftp", "pass")

        destinationFileName = str(self.deviceId).zfill(6) + ".pdf"
        
        file = open(newDocPath, "rb")
        
        try:
            ftp = FTP(FTPPath)
            ftp.login(FTPUser, FTPPass)
            ftp.cwd("doc")
            ftp.storbinary("STOR " + destinationFileName, file)

            file.close()
            ftp.quit()
        except Exception as e:
            raise DatabaseConnectionError("Durante a atualização do documento de instalação do dispositivo.",
                                          "Falha ao enviar o arquivo ao FTP.\nContate o administrador do sistema.")
            return 
        

        #copyfile(newDocPath, (self.destinyPath + str(self.deviceId).zfill(6) + ".pdf"))

        tables = ["dispositivos"]

        fieldsAndValues = [("dis_doc_enviado", "1")]

        conditions = ["dis_id = '" + str(self.deviceId) + "'"]

        updated, updatedId = myDBConnection.updateQuery(tables, fieldsAndValues, conditions)

        # --> If any error during database connection #
        if not updated:
            raise DatabaseConnectionError("Durante a atualização do documento de instalação do dispositivo.",
                                          "Falha ao tentar executar a atualização no banco.\nContate o administrador do sistema.")
            return 

        self.deviceDocSent = 1
        
###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class DevicesContainer(object):
    """
    This class is responsible for loading and holding all the call types
    """
    def __init__(self):
        self.__devices = []
        self.__devicesFromId = {}
        
###############################################################################################################################################################################

    def loadDevicesFunctions(self):
        """
        This method is called to load all the possible functions of a device. It returns a list of tuples containing the ID and the Description of the
        device function loaded from the database
        """
        # --> object used to communicate with the database #
        myDBConnection = DBConnection()
        
        fields = [
            "feq_id",
            "feq_descricao"
            ]

        tables = [
            ("funcoes_equipamento", "", "")   
            ]

        orderby = ["feq_descricao ASC"]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, None, None, None, orderby)

        if not querySuccess:
            raise DatabaseConnectionError("Durante o carregamento das funções possíveis dos dispositivos.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        return queryResult

###############################################################################################################################################################################


    def loadDevicesVinculatedToProduct(self, productId=None):
        """
        This method is called to load the call types from database
        """
        # --> object used to communicate with the database #
        myDBConnection = DBConnection()
        
        fields = [
            "dis_id",
            "dis_descricao",
            "dis_codigo_sap",
            "dis_cliente",
            "cli_nome",
            "nof_numero",
            "dis_status",
            "sdi_descricao",
            "dis_doc_enviado",
            "dis_com_imagem",
            "dis_extensao_imagem",
            "ese_numero_nota_fiscal_saida",
            "ese_id",
            "dis_com_manutencao",
            "dis_info_manutencao",
            "feq_descricao"
            ]

        tables = [
            ("vinculacao_dispositivo_produto", "", ""),
            ("dispositivos", "LEFT", "vdp_dispositivo = dis_id"),
            ("clientes", "LEFT", "dis_cliente = cli_id"),
            ("entrada_saida_equipamento", "LEFT", "dis_nota_fiscal_atual = ese_id"),
            ("notas_fiscais", "LEFT", "ese_nota_fiscal_entrada = nof_id"),
            ("status_dispositivo", "LEFT", "dis_status = sdi_id"),
            ("funcoes_equipamento", "LEFT", "vdp_funcao_dispositivo = feq_id")
            ]


        where = [
            "vdp_produto = '" +str(productId)+ "'"
            ]
        
        orderby = ["dis_id DESC"]
        
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, None, None, orderby)

        

        if not querySuccess:
            raise DatabaseConnectionError("Durante o carregamento dos dispositivos vinculados a um produto.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()
        
        for (
                deviceId,
                deviceDescription,
                deviceSAPCode,
                deviceClientId,
                deviceClientName,
                deviceInvoiceNumber,
                deviceStatusId,
                deviceStatusDescription,
                deviceDocSent,
                deviceHasImage,
                deviceImageExtension,
                deviceOutInvoiceNumber,
                deviceInOutInvoiceId,
                deviceHasMaintenance,
                deviceInfoMaintenance,
                deviceFunction
            ) in queryResult:
            
            device = Device(
                            deviceId,
                            deviceDescription,
                            deviceSAPCode,
                            deviceClientId,
                            deviceClientName,
                            deviceInvoiceNumber,
                            deviceStatusId,
                            deviceStatusDescription,
                            deviceDocSent,
                            deviceHasImage,
                            deviceImageExtension,
                            deviceOutInvoiceNumber,
                            deviceInOutInvoiceId,
                            deviceHasMaintenance,
                            deviceInfoMaintenance,
                            deviceFunction
                            )

            

            self.add(device)
        
###############################################################################################################################################################################


    def loadDevices(self, filtering=False, filteringFields=None):
        """
        This method is called to load the call types from database
        """
        # --> object used to communicate with the database #
        myDBConnection = DBConnection()
        
        fields = [
            "dis_id",
            "dis_descricao",
            "dis_codigo_sap",
            "dis_cliente",
            "cli_nome",
            "nof_numero",
            "dis_status",
            "sdi_descricao",
            "dis_doc_enviado",
            "dis_com_imagem",
            "dis_extensao_imagem",
            "ese_numero_nota_fiscal_saida",
            "ese_id",
            "dis_com_manutencao",
            "dis_info_manutencao"
            ]

        tables = [
            ("dispositivos", "", ""),
            ("clientes", "LEFT", "dis_cliente = cli_id"),
            ("entrada_saida_equipamento", "LEFT", "dis_nota_fiscal_atual = ese_id"),
            ("notas_fiscais", "LEFT", "ese_nota_fiscal_entrada = nof_id"),
            ("status_dispositivo", "LEFT", "dis_status = sdi_id")                
            ]

        if not filtering:
            where = None
            limit = ["1000"]
        else:
            where = filteringFields
            limit = None
        

        orderby = ["dis_id DESC", "ese_id DESC"]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, None, None, orderby, limit)

        if not querySuccess:
            raise DatabaseConnectionError("Durante o carregamento dos dispositivos.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()
        
        for (
                deviceId,
                deviceDescription,
                deviceSAPCode,
                deviceClientId,
                deviceClientName,
                deviceInvoiceNumber,
                deviceStatusId,
                deviceStatusDescription,
                deviceDocSent,
                deviceHasImage,
                deviceImageExtension,
                deviceOutInvoiceNumber,
                deviceInOutInvoiceId,
                deviceHasMaintenance,
                deviceInfoMaintenance
            ) in queryResult:
            
            device = Device(
                            deviceId,
                            deviceDescription,
                            deviceSAPCode,
                            deviceClientId,
                            deviceClientName,
                            deviceInvoiceNumber,
                            deviceStatusId,
                            deviceStatusDescription,
                            deviceDocSent,
                            deviceHasImage,
                            deviceImageExtension,
                            deviceOutInvoiceNumber,
                            deviceInOutInvoiceId,
                            deviceHasMaintenance,
                            deviceInfoMaintenance
                            )

            self.add(device)

###############################################################################################################################################################################


    def loadDevicesForMaintenance(self, filtering=False, filteringFields=None):
        """
        This method is called to load the call types from database
        """
        # --> object used to communicate with the database #
        myDBConnection = DBConnection()
        
        fields = [
            "dis_id",
            "dis_descricao",
            "dis_codigo_sap",
            "dis_cliente",
            "cli_nome",
            "nof_numero",
            "dis_status",
            "sdi_descricao",
            "dis_doc_enviado",
            "dis_com_imagem",
            "dis_extensao_imagem",
            "ese_numero_nota_fiscal_saida",
            "ese_id",
            "dis_com_manutencao",
            "dis_info_manutencao"
            ]

        tables = [
            ("dispositivos", "", ""),
            ("clientes", "LEFT", "dis_cliente = cli_id"),
            ("entrada_saida_equipamento", "LEFT", "dis_nota_fiscal_atual = ese_id"),
            ("notas_fiscais", "LEFT", "ese_nota_fiscal_entrada = nof_id"),
            ("status_dispositivo", "LEFT", "dis_status = sdi_id"),
            ("vinculacao_dispositivo_produto", "LEFT", "dis_id = vdp_dispositivo"),
            ("dispositivo_info_manutencao", "LEFT", "dis_info_manutencao = dim_id")
            ]


        if not filtering:
            where = ["vdp_id IS NOT NULL AND sdi_id = '2'"]
            limit = ["1000"]
        else:
            filteringFields.append("vdp_id IS NOT NULL")
            where = filteringFields
            limit = None

        groupby = ["dis_id"]

        #having = ["vinculacoes > 0"]
        
        orderby = ["dis_id DESC"]

        #print(myDBConnection.selectQuery(fields, tables, where, groupby, having, orderby, limit, queryBuild=True))
        
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, groupby, None, orderby, limit)


        if not querySuccess:
            raise DatabaseConnectionError("Durante o carregamento dos dispositivos.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()
        
        for (
                deviceId,
                deviceDescription,
                deviceSAPCode,
                deviceClientId,
                deviceClientName,
                deviceInvoiceNumber,
                deviceStatusId,
                deviceStatusDescription,
                deviceDocSent,
                deviceHasImage,
                deviceImageExtension,
                deviceOutInvoiceNumber,
                deviceInOutInvoiceId,
                deviceHasMaintenance,
                deviceInfoMaintenance
            ) in queryResult:
            
            device = Device(
                            deviceId,
                            deviceDescription,
                            deviceSAPCode,
                            deviceClientId,
                            deviceClientName,
                            deviceInvoiceNumber,
                            deviceStatusId,
                            deviceStatusDescription,
                            deviceDocSent,
                            deviceHasImage,
                            deviceImageExtension,
                            deviceOutInvoiceNumber,
                            deviceInOutInvoiceId,
                            deviceHasMaintenance,
                            deviceInfoMaintenance
                            )

            device.loadMaintenanceData()
            
            self.add(device)



###############################################################################################################################################################################

    def receiveDevices(self, devicesList, inInvoiceNumber):
        """
        This method is responsible for receiving the Devices from its owner. It creates a new entry in the entrada_saida_equipamento with the new invoice
        """
        myDBConnection = DBConnection()

        queryList = []

        for devId in devicesList:
            device = self.deviceFromId(devId)

            if device.deviceHasMaintenance and device.deviceInfoMaintenance and device.deviceHasImage and device.deviceDocSent:
                status = "2"
            else:
                status = "1"
        
            table = "entrada_saida_equipamento"

            fields = [
                "ese_nota_fiscal_entrada",
                "ese_dispositivo"
                ]

            values = [
                ("'" + str(inInvoiceNumber) + "'", "'" + str(device.deviceId)  + "'")
                ]

            queryList.append(myDBConnection.insertQuery(table, fields, values, queryBuild=True))

            tables = ["dispositivos"]
        
            fieldsAndValues = [
                ("dis_nota_fiscal_atual", "LAST_INSERT_ID()"),
                ("dis_status", "'" + status + "'")
                ]
         
            conditions = [
                "dis_id = '" + str(device.deviceId) + "'"
                ]
        
            queryList.append(myDBConnection.updateQuery(tables, fieldsAndValues, conditions, queryBuild=True))


        querySuccess = myDBConnection.aglutinatedQuery(queryList)
 
        if not querySuccess:
           raise DatabaseConnectionError("Durante o recebimento dos Equipamentos enviados pelo Cliente.",
                                         "Falha ao tentar executar o a inserção de nova entrada numa nota e atualização do dispositivo.\nContate o administrador do sistema.")
           return

###############################################################################################################################################################################

    def returnDevices(self, devicesList, outInvoiceNumber):
        """
        This method is responsible for making the return of an device to its owner. It sets the number of the device invoice out number and changes its status to "INATIVO"
        """
        queryList = []
        # --> object used to communicate with the database #
        myDBConnection = DBConnection()

        # --> first update table and values #
        tableOne = ["entrada_saida_equipamento"]
        fieldsAndValuesOne = [("ese_numero_nota_fiscal_saida", "'" + str(outInvoiceNumber) + "'")]

        # --> second update table and values #
        tableTwo = ["dispositivos"]
        fieldsAndValuesTwo = [("dis_status", "'3'")]
        
        for devId in devicesList:
            device = self.deviceFromId(devId)
            # --> first update the invoiceOutNumber #
            conditionsOne = ["ese_id = '" + str(device.deviceInOutInvoiceId) + "'"]
            queryList.append(myDBConnection.updateQuery(tableOne, fieldsAndValuesOne, conditionsOne, queryBuild=True))

            # --> after that updates the device status #
            conditionsTwo = ["dis_id = '" + str(device.deviceId) + "'"]
            queryList.append(myDBConnection.updateQuery(tableTwo, fieldsAndValuesTwo, conditionsTwo, queryBuild=True))
        
        querySuccess = myDBConnection.aglutinatedQuery(queryList)
 
        if not querySuccess:
           raise DatabaseConnectionError("Durante o retorno dos dispositivos aos seu cliente.",
                                         "Falha ao tentar executar atualização dos dados no banco.\nContate o administrador do sistema.")
           return 

###############################################################################################################################################################################


    def add(self, device):
        """
        This method adds a new call type to the call list. Returns True if success, False if fail
        """
        if int(device.deviceId) in self.__devicesFromId.keys():
            return False

        self.__devices.append([int(device.deviceId), device])
        self.__devicesFromId[int(device.deviceId)] = device
        return True

###############################################################################################################################################################################

    def clear(self):
        self.__devices = []
        self.__devicesFromId = {}

###############################################################################################################################################################################

  
    def deviceFromId(self, deviceId):
        return self.__devicesFromId[int(deviceId)]


###############################################################################################################################################################################
    def maintenanceSort(self):
        self.__devices = sorted(self.__devices, key=lambda dev: dev[1].devicePercentageMaintenance, reverse=True)
        return

###############################################################################################################################################################################

    def __iter__(self):
        for device in iter(self.__devices):
            yield device[1]

###############################################################################################################################################################################

    def __len__(self):
        return len(self.__devices)



###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class DevicesRecorder(object):
    """
    This class is used to insert the new devices into the database
    """
    def __init__(self, deviceData):
        self.deviceData = deviceData
        
        parser = configparser.SafeConfigParser()
        parser.read("dbconfig.ini")
        self.destinyPath = parser.get("fserver_connection", "path")
        self.destinyPath = self.destinyPath + "/dis/"

###############################################################################################################################################################################

    def registerDevice(self):
        """
        This method will create a string with all the insertion of the new
        devices inside the database. If any error occur the operation will be
        rolled back
        """
        myDBConnection = DBConnection()
        
        if len(self.deviceData["image"]) > 0:
            extension = "'" + self.deviceData["image"].split(".")[-1] + "'"
        else:
            extension = "NULL"
        
        queryList = []
        querySuccess = False

        for i in range(self.deviceData["quantity"]):
            ##################################################
            # --> if is client property the code will create #
            # --> an invoice entry related to this device    #
            ##################################################
            if self.deviceData["clientProperty"]:

                #################################
                # --> create invoice insert sql #
                #################################
                table = "entrada_saida_equipamento"

                fields = [
                    "ese_nota_fiscal_entrada",
                    "ese_numero_nota_fiscal_saida"
                    ]

                values = [
                    ("'" + str(self.deviceData["invoice"]) + "'", "NULL")
                    ]
        
                queryList.append(myDBConnection.insertQuery(table, fields, values, queryBuild=True))

                ################################
                # --> create device insert sql #
                ################################
                
                table = "dispositivos"

                fields = [
                    "dis_descricao",
                    "dis_cliente",
                    "dis_nota_fiscal_atual",
                    "dis_com_manutencao",
                    "dis_data_cadastro",
                    "dis_codigo_sap",
                    "dis_com_imagem",
                    "dis_observacao",
                    "dis_extensao_imagem"
                    ]

                values = [
                    ("'" + self.deviceData["description"] + "'",
                     "'" + str(self.deviceData["client"]) + "'",
                     "LAST_INSERT_ID()",
                     "'" + str(int(self.deviceData["maintenance"])) + "'",
                     "NOW()",
                     "'" + str(self.deviceData["SAPCode"]) + "'",
                     "'1'" if len(self.deviceData["image"]) else "'0'",
                     "'" + self.deviceData["observation"] + "'",
                     extension)
                    ]
                
                queryList.append(myDBConnection.insertQuery(table, fields, values, queryBuild=True))


                #####################################
                # --> update last invoice device id #
                #####################################

                tables = ["entrada_saida_equipamento, dispositivos"]

                fieldsAndValues = [("ese_dispositivo", "dis_id")]

                conditions = ["dis_id = LAST_INSERT_ID()", "dis_nota_fiscal_atual = ese_id"]

                queryList.append(myDBConnection.updateQuery(tables, fieldsAndValues, conditions, queryBuild=True))

                

            else:
                ################################
                # --> create device insert sql #
                ################################
                
                table = "dispositivos"

                fields = [
                    "dis_descricao",
                    "dis_com_manutencao",
                    "dis_data_cadastro",
                    "dis_codigo_sap",
                    "dis_com_imagem",
                    "dis_observacao",
                    "dis_extensao_imagem"
                    ]

                values = [
                    ("'" + self.deviceData["description"] + "'",
                     "'" + str(int(self.deviceData["maintenance"])) + "'",
                     "NOW()",
                     "'" + str(self.deviceData["SAPCode"]) + "'",
                     "'1'" if len(self.deviceData["image"]) else "'0'",
                     "'" + self.deviceData["observation"] + "'",
                     extension)
                    ]
                
                queryList.append(myDBConnection.insertQuery(table, fields, values, queryBuild=True))

        querySuccess = myDBConnection.aglutinatedQuery(queryList)
 
        if not querySuccess:
           raise DatabaseConnectionError("Durante a inserção de novo dispositivo.",
                                         "Falha ao tentar executar o cadastro dos dispositivo.\nContate o administrador do sistema.")
           return 

        insertedIds = self.getInsertedDevicesIdBySapCode(self.deviceData["SAPCode"])

        if len(self.deviceData["image"]) > 0:
            extension = self.deviceData["image"].split(".")[-1]
            for deviceId in insertedIds:
                copyfile(self.deviceData["image"], (self.destinyPath + str(deviceId) + "." + extension))
            
###############################################################################################################################################################################
            

    def getInsertedDevicesIdBySapCode(self, SAPCode):
        """
        This method retrieve the device ID from devices registered in the actual date
        this is used to move the devices images to the destination, creating one copy of the image for device ID
        """
        myDBConnection = DBConnection()
        
        fields = ["dis_id"]

        tables = [("dispositivos", "", "")]

        where = [
            "dis_codigo_sap = '" +str(SAPCode)+ "'",
            "DATE(dis_data_cadastro) = DATE(NOW())"
            ]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where)

        devicesIds = []

        for data in queryResult:
            devicesIds.append(data[0])

        return devicesIds

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class DeviceStatus(object):
    """
    This class holds the information about one device status
    """
    def __init__(self, deviceStatusId, deviceStatusDescription):
        self.deviceStatusId = deviceStatusId
        self.deviceStatusDescription = deviceStatusDescription


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class DeviceStatusContainer(object):
    """
    This class is responsible for loading and honding all the device status types
    """
    def __init__(self):
        self.__deviceStatus = []
        self.__deviceStatusFromId = {}
        
###############################################################################################################################################################################


    def loadDeviceStatus(self):
        """
        This method is called to load the call types from database
        """
        myDBConnection = DBConnection()
        
        fields = [
            "sdi_id",
            "sdi_descricao"
            ]

        tables = [("status_dispositivo", "", "")]

        orderby = ["sdi_id ASC"]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, None, None, None, orderby)

        if not querySuccess:
            raise DatabaseConnectionError("Durante o carregamento dos status dos dispositivos.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()
        
        for deviceStatusId, deviceStatusDescription in queryResult:
            deviceStatus = DeviceStatus(deviceStatusId, deviceStatusDescription)
            self.add(deviceStatus)


###############################################################################################################################################################################


    def add(self, deviceStatus):
        """
        This method adds a new call to the call list. Returns True if success, False if fail
        """
        if int(deviceStatus.deviceStatusId) in self.__deviceStatusFromId.keys():
            return False

        self.__deviceStatus.append([int(deviceStatus.deviceStatusId), deviceStatus])
        self.__deviceStatusFromId[int(deviceStatus.deviceStatusId)] = deviceStatus
        return True

###############################################################################################################################################################################

    def clear(self):
        self.__deviceStatus = []
        self.__deviceStatusFromId = {}

###############################################################################################################################################################################
  
    def deviceStatusFromId(self, deviceStatusId):
        return self.__deviceStatusFromId[int(deviceStatusId)]

###############################################################################################################################################################################

    def __iter__(self):
        for deviceStatus in iter(self.__deviceStatus):
            yield deviceStatus[1]

###############################################################################################################################################################################

    def __len__(self):
        return len(self.__deviceStatus)

        
