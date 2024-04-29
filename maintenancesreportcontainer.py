import time
from magicDB import DBConnection
from myExceptions import DatabaseConnectionError


class MaintenanceContainer(object):
    """
    This class holds a set of Maintenances
    """

    def __init__(self, maintenance_log_id=None,
                 maintenance_log_observacao=None,
                 maintenance_log_inicio=None,
                 maintenance_log_duracao_total=None,
                 dispositivo_id=None,
                 dispositivo_descricao=None,
                 colaborador_nome=None):

        self.maintenance_log_id = maintenance_log_id
        self.maintenance_log_observacao = maintenance_log_observacao
        self.maintenance_log_inicio = maintenance_log_inicio
        self.maintenance_log_duracao_total = maintenance_log_duracao_total
        self.dispositivo_id = dispositivo_id
        self.dispositivo_descricao = dispositivo_descricao
        self.colaborador_nome = colaborador_nome

        self.__maintenances = []
        self.__maintenancesFromId = {}

        if maintenance_log_duracao_total is not None:
            if maintenance_log_duracao_total < 0:
                maintenance_log_duracao_total = abs(int(maintenance_log_duracao_total))
                self.maintenance_log_duracao_total = "-%02d:%02d" % (
                    maintenance_log_duracao_total // 60, maintenance_log_duracao_total % 60)
            else:
                maintenance_log_duracao_total = abs(int(maintenance_log_duracao_total))
                self.formatedTotalDuration = "%02d:%02d" % (
                    maintenance_log_duracao_total // 60, maintenance_log_duracao_total % 60)

    def loadMaintenances(self, isFiltering = False,filteringFields=None):
        """
        This method is called to load the maintenance logs from the database
        """

        # --> DATABASE CONNECTION OBJECT #
        myDBConnection = DBConnection()

        fields = [
            "lmd_id",
            "lmd_observacao",
            "DATE_FORMAT(lmd_data_hora_inicio, '%d/%m/%Y %H:%i') AS lmd_data_hora_inicio",
            "TIMESTAMPDIFF(MINUTE, lmd_data_hora_inicio, lmd_data_hora_fim) AS duracao_total",
            "dis_id",
            "dis_descricao",
            "col_nome"
        ]

        tables = [
            ("log_manutencao_dispositivo", "", ""),
            ("dispositivos", "LEFT", "lmd_dispositivo = dis_id"),
            ("colaboradores", "LEFT", "lmd_colaborador = col_id")
        ]

        orderby = [
            "lmd_id DESC"
        ]
        if not isFiltering:
            where = [
                "DATE(lmd_data_hora_fim) >=  CURDATE() - INTERVAL 1 DAY",
                "DATE(lmd_data_hora_fim) <=  CURDATE()"
            ]
            limit = ["1000"]
        else:
            limit = None
            where = filteringFields
        groupby = ["lmd_id"]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, groupby, None, orderby, limit)
        if not querySuccess:
            raise DatabaseConnectionError("Seleção dos Chamados na tela de Listagem de Chamados",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()
        for (
                maintenance_log_id,
                maintenance_log_observacao,
                maintenance_log_inicio,
                maintenance_log_duracao_total,
                dispositivo_id,
                dispositivo_descricao,
                colaborador_nome,
        ) in queryResult:
            maintenance = MaintenanceContainer(maintenance_log_id,
                                               maintenance_log_observacao,
                                               maintenance_log_inicio,
                                               maintenance_log_duracao_total,
                                               dispositivo_id,
                                               dispositivo_descricao,
                                               colaborador_nome)
            self.add(maintenance)

    def add(self, maintenance_log):
        """
        This method adds a new maintenance log to the maintenance list
        """
        self.__maintenances.append(maintenance_log)
        self.__maintenancesFromId[maintenance_log.maintenance_log_id] = maintenance_log

    def clear(self):
        self.__maintenances = []
        self.__maintenancesFromId = {}

    def maintenanceLogFromId(self, maintenance_log_id):
        return self.__maintenancesFromId.get(maintenance_log_id)

    def __iter__(self):
        for maintenance_log in self.__maintenances:
            yield maintenance_log

    def __len__(self):
        return len(self.__maintenances)

    def getMaintenanceLogsItems(self, maintenance_log_id):
        """
        Retrieves maintenance log items from the database.
        """
        db_connection = DBConnection()

        fields = [
            "ifm_descricao",
            "rif_ok",
            "rif_observacao"
        ]

        tables = [
            ("resposta_item_formulario", "", ""),
            ("itens_formulario_manutencao", "LEFT JOIN", "ifm_id = rif_item")
        ]

        where = [
            "rif_log_manutencao = '{}'".format(maintenance_log_id)
        ]

        query_success, query_result = db_connection.selectQuery(fields, tables, where)

        items = []
        if query_success and query_result:
            for result in query_result:
                item = {
                    'descricao': result['ifm_descricao'],
                    'situacao': 'OK' if result['rif_ok'] == 1 else 'NOK',
                    'observacao': result['rif_observacao']
                }
                items.append(item)

        return items
