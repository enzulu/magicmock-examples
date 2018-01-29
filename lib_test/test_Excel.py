import unittest
import mock
from context import Excel

class TestExcelMethods(unittest.TestCase):
    
    @mock.patch('lib.Excel.Excel')
    @mock.patch('lib.Excel.path')
    def test_init(self, mock_Excel, mock_path):
    #    mock_Excel.LOG = "test"
    #    mock_path.isfile.return_value = False
    #    
    #    with self.assertRaises(IOError):
    #        test = Excel('any_filename', 'all', 6)
        pass
    #def test_load(self,mock_Excel, mock_xlrd):
    #    # set-up mocks
    #    mock_xlrd.open_workbook.side_effect = IOError("Directory does not exist")
    #    
    #    with self.assertRaises(IOError):
    #        mock_Excel.__load()
