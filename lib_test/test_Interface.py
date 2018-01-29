import unittest
import os
import mock
import socket
from context import FTP, TCP, UDP, SSH, Telnet, globalTimeout

#NOTE: each test suite is divided per class in Interface.py
class TestFTP(unittest.TestCase):
    
    #NOTE: setUp is used for code reuse - no need to set-up per test method
    #NOTE: mock patching can be done in the setUp method
    def setUp(self):
        patcher = mock.patch('lib.Interface.ftplib.FTP')
        patcher.start()
        self.addCleanup(patcher.stop)
        self.FTP_client = FTP('test_ip', 'test_username', 'test_password')

    @mock.patch('lib.Interface.os.path')
    def test_upload_error_handling(self, mock_path):
        #NOTE: with mock_path, we can manipulate FTP.upload's behavior
        #NOTE: we manipulate behavior, then test if results are expected.
    
        #set up mocks for invalid local file
        mock_path.isfile.return_value = False
        
        with self.assertRaises(IOError) as context:
            self.FTP_client.upload('test_local_file', 'test_remote_file')
        self.assertTrue('test_local_file not found.' in context.exception)
        mock_path.isfile.assert_called_once_with('test_local_file')
        
        #set up mocks for invalid remote file
        mock_path.reset_mock()
        mock_path.isfile.return_value = True
        self.FTP_client.ftp.cwd.side_effect = Exception('Invalid_remote_file')

        with self.assertRaises(Exception) as context:
            self.FTP_client.upload('test_local_file', 'test_remote_file')
        self.assertTrue('Invalid_remote_file' in context.exception)
        
        mock_path.isfile.assert_called_once_with('test_local_file')
        self.FTP_client.ftp.cwd.assert_called_once_with(os.path.dirname('test_remote_file'))
        
    @mock.patch('lib.Interface.os.path')
    @mock.patch('__builtin__.open')
    def test_upload_is_called(self, mock_open, mock_path):
        
        #NOTE: I decided to separate FTP.upload() error checking and
        #       FTP.upload() successful uploading, to make it easier to understand
        #       no hard and fast rules
        
        #set up mocks for valid files
        mock_path.isfile.return_value = True
        mock_path.dirname.return_value = 'valid_file_name'
        
        #test for asciiMode=False
        self.FTP_client.upload('test_local_file', 'test_remote_file', False)
        mock_open.assert_called_once_with('test_local_file', 'rb')
        self.FTP_client.ftp.storbinary.assert_called_once()
        
        mock_open.reset_mock()
        
        #test for asciiMode=True
        self.FTP_client.upload('test_local_file', 'test_remote_file', True)
        mock_open.assert_called_once_with('test_local_file', 'r')
        self.FTP_client.ftp.storlines.assert_called_once()
    
    def test_delete_if_remote_not_found(self):

        self.FTP_client.ftp.delete.side_effect = Exception('Invalid_remote_file')
        
        with self.assertRaises(Exception) as context:
            self.FTP_client.delete('test_file')
        self.assertTrue('Invalid_remote_file' in context.exception)
        self.FTP_client.ftp.delete.assert_called_once_with('test_file')
    
    def test_delete_is_called(self):
    
        self.FTP_client.delete('test_file')
        self.FTP_client.ftp.delete.assert_called_once()
        
    def test_close_is_called(self):

        self.FTP_client.close()
        self.FTP_client.ftp.close.assert_called_once()

class TestTCP(unittest.TestCase):

    def setUp(self):
        mock_logger = mock.patch('lib.Interface.Logger')
        mock_socket = mock.patch('lib.Interface.socket')
        mock_logger.start()
        mock_socket.start()
        self.addCleanup(mock_logger.stop)
        self.addCleanup(mock_socket.stop)
        
        self.test_port = 1000 #arbitrary
        self.TCP_client = TCP('test_ip', self.test_port)
    
    def test_TCP_init(self):
        
        #NOTE: unit testing helps to expose bad design in the SUT.
        #      is it good design to test during initialization?
        #      is it better to open a socket connection in a separate method?
        #      well-designed code is easily-testable code.
        
        #TODO: test exception if socket.timeout occurs.
        # challenging to mock because exception handling is
        # in the __init__
        self.TCP_client.sock.connect.assert_called_once_with(('test_ip', self.test_port))
        
    @mock.patch('lib.Interface.Message')
    def test_TCP_send_messageSetValue_flags(self, mock_message):

        # fake input
        testBoardRecv = 1
        testCpuRev =    2
        testTaskRecv =  3        
        testBoardSent = 4
        testCpuSent =   5
        testTaskSent =  6

        self.TCP_client.send(mock_message, 
                        testBoardRecv, 
                        testCpuRev, 
                        testTaskRecv,
                        None, #Note: why is 'delay' in the middle of the arguments? :(
                        testBoardSent, 
                        testCpuSent, 
                        testTaskSent)
        
        mock_message.setValue.assert_any_call('rec_board', testBoardRecv)
        mock_message.setValue.assert_any_call('rec_cpu', testCpuRev)
        mock_message.setValue.assert_any_call('rec_task', testTaskRecv)
        mock_message.setValue.assert_any_call('send_board', testBoardSent)
        mock_message.setValue.assert_any_call('send_cpu', testCpuSent)
        mock_message.setValue.assert_any_call('send_task', testTaskSent)
        
    @mock.patch('lib.Interface.Message')
    def test_TCP_send_messageLength_checking(self, mock_message):
        
        #mock length to be positive
        mock_message.getMessageLength.return_value = 1
        
        self.TCP_client.send(mock_message)
        self.TCP_client.sock.sendall.assert_called_with(mock_message.encode())
        
        self.TCP_client.sock.sendall.reset_mock()
        
        #mock length to be zero
        mock_message.getMessageLength.return_value = 0
        
        self.TCP_client.send(mock_message)
        self.TCP_client.sock.sendall.assert_not_called()
        
    @mock.patch('lib.Interface.Message')
    @mock.patch('lib.Interface.time')
    def test_TCP_send_delay(self, mock_time, mock_message):

        testDelay = 1
        self.TCP_client.send(mock_message, 
                             None, 
                             None, 
                             None, 
                             testDelay, 
                             None, 
                             None,
                             None)
        
        mock_time.sleep.assert_called_once_with(testDelay)
        mock_time.reset_mock()
        
        testDelay = 0
        self.TCP_client.send(mock_message, 
                             None, 
                             None, 
                             None, 
                             testDelay, 
                             None, 
                             None,
                             None)
        
        mock_time.sleep.assert_not_called()
    
    @mock.patch('lib.Interface.Message')
    @mock.patch('__builtin__.int')
    def test_TCP_recv(self, mock_int, mock_message):

        #test message header not received 
        mock_message.MESSAGE_HEADER_LENGTH = 16
        self.TCP_client.sock.recv.side_effect = Exception('not_recieved')
       
        with self.assertRaises(Exception) as context:
            self.TCP_client.recv('some_message')
        self.assertTrue('not_recieved' in context.exception)
        #print mock_message.MESSAGE_HEADER_LENGTH.call_count
        self.TCP_client.sock.recv.assert_called_once()
        
        self.TCP_client.sock.recv.side_effect = None
        self.TCP_client.sock.recv.reset_mock()
        
        #test message header length != MESSAGE_HEADER_LENGTH
        self.TCP_client.sock.recv.return_value = '' #length=8
        pass
        #with self.assertRaises(Exception) as context:
        #self.TCP_client.recv('some_message')
        #self.assertTrue('not_recieved' in context.exception)
















    