import unittest
import mock
import xml.etree.ElementTree as ET
from context import DbCommon, DeployDb, AdaptorDb

class TestDbCommonMethods(unittest.TestCase):


    #def setUp(self):
    #   self.logger = None
    #   self.db_common = DbCommon(self.logger)
    
    @mock.patch('lib.DataBase.ET')
    def test_getSubList(self, mock_ET):
        pass
        # logger = None
        # db_common = DbCommon(logger)
        # print db_common.xmltree
        
        # #TODO = UNDERSTAND THIS
        # mock_ET.parse.find.return_value = None
        
        # test_result = db_common.xmltree.find('test_tag').text
        # print test_result

        
        
class TestDeployDbMethods(unittest.TestCase):
    pass

class TestAdaptorDbMethods(unittest.TestCase):
    pass
    
if __name__ == '__main__':

    unittest.main()