import unittest
import mock
import subprocess

from context import HwConfigForFsmr4BtsAndFsmr3TT_4x


class TestHWConfigMethods(unittest.TestCase):
    
    @mock.patch('Common.HwConfigForFsmr4BtsAndFsmr3TT_4x.subprocess.check_call')
    @mock.patch('Common.HwConfigForFsmr4BtsAndFsmr3TT_4x.Init.logger')
    def test_svn_revert(self, mock_logger, mock_check_call):
        """
        Test three exception handling conditions for svn_revert:
        1) Generic Error (catch-all)
        2) OSError (file not found, other OS-related errors)
        3) CalledProcessError (SVN reported a failure)
        """
        #mock up the three error conditions.
        # side_effect() will use them one after the other.
        mock_check_call.side_effect = [Exception('generic_error_msg'),
                                       OSError(1, 'os_error_msg'),
                                       subprocess.CalledProcessError(1, 'svn', None)]

        # case 1: generic exception
        with self.assertRaises(Exception) as test1:
            HwConfigForFsmr4BtsAndFsmr3TT_4x.svn_revert('some_file')
        self.assertTrue('generic_error_msg' in test1.exception,
                        "Unexpected generic exception message")
        self.assertTrue('exceptions.Exception' in str(mock_logger.error.call_args),
                        "Init.logger.error() did not report exception message")
        mock_logger.error.reset_mock()
        
        # case 2: OSError
        with self.assertRaises(OSError) as test2:
            HwConfigForFsmr4BtsAndFsmr3TT_4x.svn_revert('some_file')
        self.assertTrue('os_error_msg' in test2.exception,
                        "OSError report was not found")
        self.assertTrue('[Errno 1] os_error_msg' in str(mock_logger.error.call_args),
                        "Init.logger.error() did not report OSError message")
        mock_logger.error.reset_mock()
        
        # case 3: CalledProcessError
        with self.assertRaises(subprocess.CalledProcessError) as test3:
            HwConfigForFsmr4BtsAndFsmr3TT_4x.svn_revert('some_file')
        self.assertTrue('svn' in str(test3.exception),
                        "SVN not mentioned in CalledProcessError")
        self.assertTrue('svn' in str(mock_logger.error.call_args),
                        "Init.logger.error() did not report SVN error")

        self.assertEquals(mock_check_call.call_count, 3,
                          "SVN revert command was not called enough times")
        


        
        
        