import unittest
import os
from context import Config

class TestConfigMethods(unittest.TestCase):

    def test_is_log_format_valid(self):
        self.assertTrue(isinstance(Config.LOG_FORMAT, (str, unicode)))
        self.assertTrue(Config.LOG_FORMAT in ["pegasus", "AHTI"])
    
    def test_is_xml_message_address_valid(self):
        address = Config.XML_MESSAGE
        self.assertTrue(isinstance(address, (str, unicode)))
        self.assertTrue(os.path.isfile(address))
        self.assertTrue("messages.xml" in address)
        
    def test_is_xml_message_pegasus_address_valid(self):
        address = Config.XML_MESSAGE_PEGASUS
        self.assertTrue(isinstance(address, (str, unicode)))
        self.assertTrue(os.path.isfile(address))
        self.assertTrue("messages_pegasus.xml" in address)
    
    def test_is_pegasus_workspace_valid(self):
        address = Config.PEGASUS_WORKSPACE
        self.assertTrue(isinstance(address, (str, unicode)))
        self.assertTrue(os.path.isdir(address))
        
    def test_is_pegasus_glo_param_valid(self):
        address = Config.PEGASUS_GLO_PARAM
        self.assertTrue(isinstance(address, (str, unicode)))
        self.assertTrue(os.path.isfile(address))
        
    def test_is_pegasus_timing_param_valid(self):
        address = Config.PEGASUS_TIMING_PARAM
        self.assertTrue(isinstance(address, (str, unicode)))
        self.assertTrue(os.path.isfile(address))
        
    def test_is_pegasus_cell_param_valid(self):
        address = Config.PEGASUS_CELL_PARAM
        self.assertTrue(isinstance(address, (str, unicode)))
        self.assertTrue(os.path.isfile(address))
        
    def test_is_pegasus_tt_param_valid(self):
        address = Config.PEGASUS_TT_PARAM
        self.assertTrue(isinstance(address, (str, unicode)))
        self.assertTrue(os.path.isfile(address))
        
    def test_is_save_info_log_valid(self):
        self.assertTrue(Config.SAVE_INFO_LOG in [True, False, 0])
    
    def test_is_save_message_log_valid(self):
        self.assertTrue(Config.SAVE_MESSAGE_LOG in [True, False, 0])
    
    def test_is_log_dir_valid(self):
        address = Config.LOG_DIR
        self.assertTrue(isinstance(address, (str, unicode)))
        self.assertTrue(os.path.isdir(address))
        
    def test_is_excel_filename_for_bts_valid(self):
        self.assertTrue(Config.EXCEL_FILENAME_FOR_BTS in [1, 0, None])
    
    def test_is_excel_filename_for_tt_valid(self):
        self.assertTrue(Config.EXCEL_FILENAME_FOR_TT in [1, 0, None])
        
    def test_is_excel_sheets_valid(self):
        self.assertTrue(isinstance(Config.EXCEL_SHEETS, dict))
        for excel_sheets_element in Config.EXCEL_SHEETS.values():
            self.assertTrue(excel_sheets_element in [0, 1])
        
        
if __name__ == '__main__':

    unittest.main()