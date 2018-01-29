import unittest
import mock
from context import XmlDatabase

class TestXmlDatabase(unittest.TestCase):

    def setUp(self):
        self.xml_database = XmlDatabase()

    @mock.patch('lib.Message.et')
    def test_parse(self, mock_et):
        
        self.xml_database.parse("test_xml_file")
        
        mock_et.parse.assert_called_once_with("test_xml_file")
    
    # @mock.patch('lib.Message.et.Element.find.text')
    # @mock.patch('lib.Message.et.ElementTree.iterfind')
    # @mock.patch('lib.Message.et.Element')
    # def test_getEnum(self, mock_element, mock_iterfind, mock_text):
        # #set up fail input tests
        # wrong_input_format = "path-has-no-period-or-underline"

        # with self.assertRaises(ValueError):
            # self.xml_database.getEnum(wrong_input_format)

        # test_input = "test_Name.test_Member"
        
        # #set up mock iterator
        # mock_text.return_value = "test_Member"
        # #mock_element.get.return_value = None
        # #mock_iterfind.return_value = iter([mock_element,mock_element,mock_element])
        # mock_iterfind.return_value = [mock_element,mock_element,mock_element]
        
        # with self.assertRaises(IOError):
            # self.xml_database.getEnum(test_input) 

        # #mock_iterfind.assert_called_once()
        # print "iterfind counts: " + str(mock_iterfind.call_count)
        # print "text counts: " + str(mock_text.call_count)
        # print "find counts: " + str(mock_element.find.call_count)
            