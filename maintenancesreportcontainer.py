import time
from magicDB import DBConnection
from myExceptions import DatabaseConnectionError
from datetime import datetime


class MaintenanceContainer(object):
    """
    This class holds a set of Maintenances
    """

    def __init__(self, maintenance_log_id=None,
                 maintenance_log_observacao=None,
                 maintenance_log_inicio=None,
                 maintenance_log_fim=None,
                 maintenance_log_duracao_total=None,
                 dispositivo_id=None,
                 dispositivo_descricao=None,
                 colaborador_nome=None,
                 maintenance_response_description=None,
                 maintenance_response_situation=None,
                 maintenance_response_observation=None
                 ):

        self.maintenance_log_id = maintenance_log_id
        self.maintenance_log_observacao = maintenance_log_observacao
        self.maintenance_log_inicio = maintenance_log_inicio
        self.maintenance_log_fim = maintenance_log_fim
        self.maintenance_log_duracao_total = maintenance_log_duracao_total
        self.dispositivo_id = dispositivo_id
        self.dispositivo_descricao = dispositivo_descricao
        self.colaborador_nome = colaborador_nome
        self.maintenance_response_description = maintenance_response_description
        self.maintenance_response_situation = maintenance_response_situation
        self.maintenance_response_observation = maintenance_response_observation

        self.__maintenances = []
        self.__maintenancesFromId = {}

    def loadMaintenances(self, isFiltering=False, filteringFields=None):
        """
        This method is called to load the maintenance logs from the database
        """

        # --> DATABASE CONNECTION OBJECT #
        myDBConnection = DBConnection()

        fields = [
            "log_manutencao_dispositivo.lmd_id",
            "log_manutencao_dispositivo.lmd_observacao",
            "DATE_FORMAT(log_manutencao_dispositivo.lmd_data_hora_inicio, '%d/%m/%Y %H:%i') AS lmd_data_hora_inicio",
            "DATE_FORMAT(log_manutencao_dispositivo.lmd_data_hora_fim, '%d/%m/%Y %H:%i') AS lmd_data_hora_fim",
            "TIMESTAMPDIFF(MINUTE, log_manutencao_dispositivo.lmd_data_hora_inicio, log_manutencao_dispositivo.lmd_data_hora_fim) AS duracao_total",
            "log_manutencao_dispositivo.lmd_dispositivo",
            "dispositivos.dis_descricao",
            "colaboradores.col_nome",
            "resposta_item_formulario_1.ifm_descricao",
            "resposta_item_formulario_1.rif_ok",
            "resposta_item_formulario_1.rif_observacao"
        ]

        tables = [
            ("log_manutencao_dispositivo", "", ""),
            ("dispositivos", "LEFT", "log_manutencao_dispositivo.lmd_dispositivo = dispositivos.dis_id"),
            ("colaboradores", "LEFT", "log_manutencao_dispositivo.lmd_colaborador = colaboradores.col_id"),
            ("resposta_item_formulario AS resposta_item_formulario_1", "LEFT",
             "resposta_item_formulario_1.rif_log_manutencao = log_manutencao_dispositivo.lmd_id"),
            ("itens_formulario_manutencao", "LEFT",
             "resposta_item_formulario_1.ifm_id = itens_formulario_manutencao.ifm_id")
        ]

        orderby = [
            "log_manutencao_dispositivo.lmd_id DESC"
        ]
        if not isFiltering:
            where = [
                "DATE(log_manutencao_dispositivo.lmd_data_hora_fim) >= CURDATE() - INTERVAL 30 DAY",
                "DATE(log_manutencao_dispositivo.lmd_data_hora_fim) <= CURDATE()"
            ]
            limit = ["1000"]
        else:
            limit = None
            where = filteringFields

        groupby = ["log_manutencao_dispositivo.lmd_id"]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, groupby, None, orderby, limit)
        if not querySuccess:
            raise DatabaseConnectionError("Seleção dos Chamados na tela de Listagem de Chamados",
                                          "Falha ao tentar executar a consulta no banco. Contate o administrador do sistema.")
            return

        self.clear()
        for result in queryResult:
            (
                maintenance_log_id,
                maintenance_log_observacao,
                maintenance_log_inicio,
                maintenance_log_fim,
                maintenance_log_duracao_total,
                dispositivo_id,
                dispositivo_descricao,
                colaborador_nome,
                maintenance_response_description,
                maintenance_response_situation,
                maintenance_response_observation
            ) = result

            # Cria um objeto MaintenanceContainer
            maintenance = MaintenanceContainer(
                maintenance_log_id,
                maintenance_log_observacao,
                maintenance_log_inicio,
                maintenance_log_fim,
                maintenance_log_duracao_total,
                dispositivo_id,
                dispositivo_descricao,
                colaborador_nome,
                maintenance_response_description,
                maintenance_response_situation,
                maintenance_response_observation
            )
            # Adiciona o objeto à lista de manutenções
            self.add(maintenance)

    # def loadMaintenances(self, isFiltering=False, filteringFields=None):
    #     """
    #     This method is called to load the maintenance logs from the database
    #     """
    #
    #     # --> DATABASE CONNECTION OBJECT #
    #     myDBConnection = DBConnection()
    #
    #     fields = [
    #         "lmd_id",
    #         "lmd_observacao",
    #         "DATE_FORMAT(lmd_data_hora_inicio, '%d/%m/%Y %H:%i') AS lmd_data_hora_inicio",
    #         "DATE_FORMAT(lmd_data_hora_fim, '%d/%m/%Y %H:%i') AS lmd_data_hora_fim",
    #         "TIMESTAMPDIFF(MINUTE, lmd_data_hora_inicio, lmd_data_hora_fim) AS duracao_total",
    #         "dis_id",
    #         "dis_descricao",
    #         "col_nome"
    #     ]
    #
    #     tables = [
    #         ("log_manutencao_dispositivo", "", ""),
    #         ("dispositivos", "LEFT", "lmd_dispositivo = dis_id"),
    #         ("colaboradores", "LEFT", "lmd_colaborador = col_id")
    #     ]
    #
    #     orderby = [
    #         "lmd_id DESC"
    #     ]
    #     if not isFiltering:
    #         where = [
    #             "DATE(lmd_data_hora_fim) >=  CURDATE() - INTERVAL 30 DAY",
    #             "DATE(lmd_data_hora_fim) <=  CURDATE()"
    #         ]
    #         limit = ["1000"]
    #     else:
    #         limit = None
    #         where = filteringFields
    #     groupby = ["lmd_id"]
    #
    #     querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, groupby, None, orderby, limit)
    #     if not querySuccess:
    #         raise DatabaseConnectionError("Seleção dos Chamados na tela de Listagem de Chamados",
    #                                       "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
    #         return
    #
    #     self.clear()
    #     for (
    #             maintenance_log_id,
    #             maintenance_log_observacao,
    #             maintenance_log_inicio,
    #             maintenance_log_fim,
    #             maintenance_log_duracao_total,
    #             dispositivo_id,
    #             dispositivo_descricao,
    #             colaborador_nome,
    #     ) in queryResult:
    #         # Cria um objeto MaintenanceContainer
    #         maintenance = MaintenanceContainer(
    #             maintenance_log_id,
    #             maintenance_log_observacao,
    #             maintenance_log_inicio,
    #             maintenance_log_fim,
    #             maintenance_log_duracao_total,
    #             dispositivo_id,
    #             dispositivo_descricao,
    #             colaborador_nome
    #         )
    #         # Adiciona o objeto à lista de manutenções
    #         self.getMaintenanceLogsItems(maintenance_log_id)
    #         self.add(maintenance)
    #
    # def getMaintenanceLogsItems(self, maintenance_log_id):
    #     """
    #     Retrieves maintenance log items from the database.
    #     """
    #     db_connection = DBConnection()
    #
    #     fields = [
    #         "ifm_descricao",
    #         "rif_ok",
    #         "rif_observacao"
    #     ]
    #
    #     tables = [
    #         ("resposta_item_formulario", "", ""),
    #         ("itens_formulario_manutencao", "LEFT", "ifm_id = rif_item")
    #     ]
    #
    #     where = [
    #         "rif_log_manutencao = '{}'".format(maintenance_log_id)
    #     ]
    #     orderby = [
    #         "ifm_posicao"
    #     ]
    #     query_success, query_result = db_connection.selectQuery(fields, tables, where, None, None, orderby)
    #
    #     items = []
    #     if query_success and query_result:
    #         for (
    #                 maintenance_response_description,
    #                 maintenance_response_situation,
    #                 maintenance_response_observation
    #         ) in query_result:
    #             response = MaintenanceContainer(
    #                 maintenance_response_description,
    #                 maintenance_response_situation,
    #                 maintenance_response_observation
    #             )
    #             items.append(response)
    #
    #     return items

    def add(self, maintenance_log):
        """
        This method adds a new maintenance log to the maintenance list
        """
        if maintenance_log.maintenance_log_id in self.__maintenancesFromId.keys():
            return False

        self.__maintenances.append(maintenance_log)
        self.__maintenancesFromId[maintenance_log.maintenance_log_id] = maintenance_log

    def clear(self):
        self.__maintenances = []
        self.__maintenancesFromId = {}

    def getMaintenanceById(self, maintenance_id):
        """
        Retorna o objeto de manutenção correspondente ao ID fornecido.
        Se não encontrar, retorna None.
        """
        for maintenance in self.__maintenances:
            if maintenance.maintenance_log_id == maintenance_id:
                return maintenance
        return None
    def maintenanceLogFromId(self, maintenance_log_id):
        return self.__maintenancesFromId.get(maintenance_log_id)

    def __iter__(self):
        for maintenance_log in self.__maintenances:
            yield maintenance_log

    def __len__(self):
        return len(self.__maintenances)
