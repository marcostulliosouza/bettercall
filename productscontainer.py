from magicDB import *

__version__ = "2.0.0"



###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class Product(object):
    """
    This class holds data about one client
    """
    def __init__(self, productId=None, productName=None, productClientId=None, prodIsActive=None, prodHasTest=None):
        self.productId = int(productId)
        self.productName = productName
        self.productClientId = int(productClientId)
        self.prodIsActive = int(prodIsActive)
        self.prodHasTest = int(prodHasTest)

###############################################################################################################################################################################

    def updateHasTest(self, prodHasTest):
        """
        This method updates if the product has test or not based on the prodHasTest parameter
        """
        
        myDBConnection = DBConnection()

        tables = ["produtos"]

        fieldsAndValues = [("pro_com_teste", "'" + str(prodHasTest) + "'")]

        conditions = ["pro_id = '" + str(self.productId) + "'"]
        
        updated, updatedId = myDBConnection.updateQuery(tables, fieldsAndValues, conditions)
        # --> If any error during database connection #
        if not updated:
            raise DatabaseConnectionError("Durante a atualização do campo de teste de um produto.",
                                          "Falha ao tentar executar a atualização no banco.\nContate o administrador do sistema.")
            return
        
        self.prodHasTest = prodHasTest

###############################################################################################################################################################################

    def addDeviceToProduct(self, deviceId, deviceFunction):
        """
        This method is used to vinculate a device to a product.
        It inserts a register into the vinculacao_dispositivo_produto table
        """
        myDBConnection = DBConnection()
        
        table = "vinculacao_dispositivo_produto"

        fields = ["vdp_dispositivo", "vdp_produto", "vdp_funcao_dispositivo"]

        values = [("'" + str(deviceId) + "'", "'" + str(self.productId) + "'", "'" + str(deviceFunction) + "'")]

        inserted, insertedId = myDBConnection.insertQuery(table, fields, values)

        if not inserted:
            raise DatabaseConnectionError("Durante a vinculação de um dispositivo a um produto.",
                                          "Falha ao tentar executar a inserção no banco.\nContate o administrador do sistema.")
            return 

###############################################################################################################################################################################

    def deactivateProduct(self):
        """
        This method is called after a confirmation to update the field "pro_ativo" setting its value to 0. After that the product
        won't appear anymore in the product list.
        """
        myDBConnection = DBConnection()

        tables = ["produtos"]

        fieldsAndValues = [("pro_ativo", "'0'")]

        conditions = ["pro_id = '" + str(self.productId) + "'"]
        
        updated, updatedId = myDBConnection.updateQuery(tables, fieldsAndValues, conditions)
        # --> If any error during database connection #
        if not updated:
            raise DatabaseConnectionError("Durante a desativação de um produto.",
                                          "Falha ao tentar executar a atualização no banco.\nContate o administrador do sistema.")
            return
        

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class ProductsContainer(object):
    """
    This class holds a set of products
    """

    def __init__(self):
        self.__products = []
        self.__productsFromId = {}

###############################################################################################################################################################################

    def loadProductsFromClient(self, clientId, onlyActives=False):
        """
        This method is called to load all the active clients that dont have an analyst related to them
        """
        myDBConnection = DBConnection()
        
        fields = [
                "pro_id",
                "pro_nome",
                "pro_cliente",
                "pro_ativo",
                "pro_com_teste"
                ]
            
        tables = [("produtos", "", "")]
        
        where = [
            "pro_id > 1",
            "pro_cliente = '" + str(clientId) + "' "
            ]

        if onlyActives:
            where.append("pro_ativo = 1")
        
        orderby = ["pro_nome ASC"]
        
        querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, None, None, orderby)
        # --> if any error during database connection #
        if not querySuccess:
            raise DatabaseConnectionError("Durante a listagem de produtos de um cliente específico.",
                                          "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
            return

        self.clear()

        for productId, productName, productClientId, prodIsActive, prodHasTest in queryResult:
            product = Product(productId, productName, productClientId, prodIsActive, prodHasTest)
            self.add(product)

###############################################################################################################################################################################

    def add(self, product):
        """
        This method adds a new call to the call list. Returns True if success, False if fail
        """
        if int(product.productId) in self.__productsFromId.keys():
            return False

        self.__products.append([int(product.productId), product])
        self.__productsFromId[int(product.productId)] = product
        return True

###############################################################################################################################################################################

    def clear(self):
        self.__products = []
        self.__productsFromId = {}

###############################################################################################################################################################################

    def removeProduct(self, productId, product):
        for row, product in enumerate(self.__products):
            if product[0] == productId:
                self.__products.pop(row)
                break
            
        del(self.__productsFromId[productId])

###############################################################################################################################################################################
    
    def productFromId(self, productId):
        return self.__productsFromId[int(productId)]

###############################################################################################################################################################################

    def __iter__(self):
        for product in iter(self.__products):
            yield product[1]

###############################################################################################################################################################################

    def __len__(self):
        return len(self.__products)
