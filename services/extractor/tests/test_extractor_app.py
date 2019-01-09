import unittest
import mock
from mock import call, Mock

from . import context
import app
from ftpclient import FtpClient
from messagebroker import MessageBroker
from worker import Worker

class ExtractorAppTestCase(unittest.TestCase):


    @mock.patch('app.os.path')
    @mock.patch('app.os')
    def test_create_work_paths_success(self, mock_os, mock_path):
        """Tests if create_work_paths function works"""

        # set to return NOT EXIST path
        mock_path.isdir.return_value = False

        app.create_work_paths("extracted/", "download/")
        
        calls = [call("extracted/"), call("download/")]

        # create_work_paths should verify (isdir)
        mock_os.path.isdir.assert_has_calls(calls, any_order=True)

        # create_work_paths should create (mkdir)
        mock_os.mkdir.assert_has_calls(calls, any_order=False)


    @mock.patch('app.os.path')
    @mock.patch('app.os')
    def test_create_work_paths_fail(self, mock_os, mock_path):
        """Tests if create_work_paths function fails correctly"""

        # set to return EXIST path
        mock_path.isdir.return_value = True

        app.create_work_paths("extracted/", "download/")
        
        calls = [call("extracted/"), call("download/")]

        # create_work_paths should verify (isdir)
        mock_os.path.isdir.assert_has_calls(calls, any_order=True)

        # create_work_paths should NOT create existing paths (mkdir)
        mock_os.mkdir.assert_not_called()


    @mock.patch('app.os.path')
    def test_pre_execute_success(self, mock_path):
        """Tests if pre_execute works"""

        # make path always exist
        mock_path.isdir.return_value = True

        class fakeConfig:
            GENERAL = {"extracted_path" : "path/to/extracted"}
            DATASOURCES = {"ftp_ds" : {"local_path":"path/to/download"}}

        self.assertTrue(app.pre_execute(fakeConfig))


    @mock.patch('app.os.path')
    def test_pre_execute_fail(self, mock_path):
        """Tests if create_work_paths function fails correctly"""

        # make paths not exist
        mock_path.isdir.return_value = False

        class fakeConfig:
            GENERAL = {"extracted_path" : "path/to/extracted"}
            DATASOURCES = {"ftp_ds" : {"local_path":"path/to/download"}}

        self.assertFalse(app.pre_execute(fakeConfig))


    @mock.patch('ftpclient.FtpClient')
    @mock.patch('messagebroker.MessageBroker')
    @mock.patch('worker.Worker')
    def test_worker_sucess(self, mock_ftp, mock_message, mock_worker):
        """Tests if worker function works"""
        
        app.worker(mock_ftp, mock_message, mock_worker, loop=False)

        mock_ftp.download_files.assert_called()
        mock_worker.extract.assert_called()
        mock_message.warn_transformer.assert_called()


    @mock.patch('ftpclient.FtpClient')
    @mock.patch('messagebroker.MessageBroker')
    @mock.patch('worker.Worker')
    def test_worker_fail(self, mock_ftp, mock_message, mock_worker):
        """Tests if worker function fails correctly"""

        # make ftp raise a exception
        mock_ftp.download_files.side_effect = Exception('some exception') 

        app.worker(mock_ftp, mock_message, mock_worker, loop=False)

        mock_ftp.download_files.assert_called()
        mock_worker.extract.assert_not_called()
        mock_message.warn_transformer.assert_not_called()




if __name__ == '__main__':
    unittest.main()
