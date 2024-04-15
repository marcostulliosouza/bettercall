from magicDB import *

__version__ = "1.0.0"

class InputCategory(object):
    """
    This class holds the information about one input category
    """
    def __init__(self, inputCatId, inputCatDesc):
        self.inputCatId = int(inputCatId)
        self.inputCatDesc = inputCatDesc

        
class InputCategoryContainer(object):
    """
    This class is responsible for loading and holding all the Input Categories
    """    
    def __init__(self):
        self.__inputCategories = []
        self.__inputCategoriesFromId = {}

    def loadInputCategories(self):
        """
        This method is called to load the call types from database
        """
        self.clear()
        myConnection = DBConnection()
        myConnection.startConnection()

        fields = [
            "cai_id",
            "cai_descricao"
            ]

        tables = [("categorias_insumos", "", "")]

        orderby = ["cai_descricao ASC"]

        try:
            inputCategories = myConnection.selectQuery(fields, tables, None, None, None, orderby)
        except:
            print("Falha ao acessar o banco de dados.\n{0}".format(sys.exc_info()[0]))
            myConnection.endConnection()
            return

        for inputCatId, inputCatDescription in inputCategories:
            inputCategory = InputCategory(inputCatId, inputCatDescription)
            self.add(inputCategory)
            
        myConnection.endConnection()

    def add(self, inputCategory):
        """
        This method adds a new input Category. Returns True if success, False if fail
        """
        if int(inputCategory.inputCatId) in self.__inputCategoriesFromId.keys():
            return False

        self.__inputCategories.append([int(inputCategory.inputCatId), inputCategory])
        self.__inputCategoriesFromId[int(inputCategory.inputCatId)] = inputCategory
        return True
    

    def clear(self):
        self.__inputCategories = []
        self.__inputCategoriesFromId = {}
  
    def inputCategoryFromId(self, inputCategoryId):
        return self.__inputCategoriesFromId[int(inputCategoryId)]

    def __iter__(self):
        for inputCategories in iter(self.__inputCategories):
            yield inputCategories[1]

    def __len__(self):
        return len(self.__inputCategories)
    
