from magicDB import *

__version__ = "2.0.0"

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class Detractor(object):
    """
    This class holds the data about one detractor
    """
    def __init__(self, detId, detDescription, detTypeId=None, detTypeDesc=None, detIndicator=None):
        self.detId = detId
        self.detDescription = detDescription
        self.detTypeId = detTypeId
        self.detTypeDesc = detTypeDesc
        self.detIndicator = detIndicator


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class DetractorContainer(object):
    """
    This class will be responsible for holding all the detractors
    """

    def __init__(self):
        self.__detractors = []
        self.__detractorsFromId = {}
       
###############################################################################################################################################################################

    def loadDetractors(self, detType=None):
        """
        This method is called to load the detractors from the database.
        If the detType parameter is passed it will select the detractors
        from that type or detractors without type
        """
        myDBConnection = DBConnection()
        
        self.clear()
        
        fields = [
            "dtr_id",
            "dtr_descricao",
            "dtr_tipo",
            "tch_descricao",
            "dtr_indicador",
            ]

        tables = [
            ("detratores", "", ""),
            ("tipos_chamado", "LEFT", "dtr_tipo = tch_id")
            ]

        where = [
            "dtr_ativo = 1"
            ]

        if detType is not None:
            where.append("(dtr_tipo IS NULL OR dtr_tipo = " + str(detType)+ ")")

        orderby = ["dtr_descricao ASC"]

        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, None, None, orderby)
        
        if not querySuccess:
            raise DatabaseConnectionError("Busca pela lista de detratores",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        for detId, detDescricao, detTypeId, detTypeDesc, detIndicator in queryResult:
            detractor = Detractor(detId, detDescricao, detTypeId, detTypeDesc, detIndicator)
            self.add(detractor)

###############################################################################################################################################################################

    def add(self, detractor):
        """
        This method adds a new call to the call list. Returns True if success, False if fail
        """
        if int(detractor.detId) in self.__detractorsFromId.keys():
            return False

        self.__detractors.append([int(detractor.detId), detractor])
        self.__detractorsFromId[int(detractor.detId)] = detractor
        return True

###############################################################################################################################################################################


    def clear(self):
        self.__detractors = []
        self.__detractorsFromId = {}

###############################################################################################################################################################################
  
    def detractorFromId(self, detId):
        return self.__detractorsFromId[int(detId)]

###############################################################################################################################################################################

    def __iter__(self):
        for detractor in iter(self.__detractors):
            yield detractor[1]

###############################################################################################################################################################################

    def __len__(self):
        return len(self.__detractors)


    
