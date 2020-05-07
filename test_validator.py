import unittest
import json
from validator import ServerVerification

#URl to call REST api
URL = "https://raw.githubusercontent.com/shivam8287/HwValidation/master/test_data.json"

#File use to check the response
validationFile = "test_data.json"

class TestServerVerification(unittest.TestCase):
    
    def setUp(self):
        self.testServer = ServerVerification(URL,validationFile)

    def test_checkVariables(self):
        self.assertEqual(self.testServer.URL, URL)
        self.assertEqual(self.testServer.validationFile, validationFile)

    def test_loadJSON(self):
        response = self.testServer.loadJSON()
        self.assertEqual(response.ok, True)

    def test_loadValidationFile(self):
        with open(validationFile, 'r') as f:
            validConfig = json.load(f)
        self.testServer.loadValidationFile()
        self.assertEqual(self.testServer.validConfig, validConfig)


    def test_compareNodes(self):
        self.testServer.loadValidationFile()
        self.testServer.loadJSON()

        self.testServer.compareNodes(self.testServer.validConfig, self.testServer.serverConfig)
        self.assertEqual(self.testServer.validationSuccess, True)

if __name__ == "__main__":
    unittest.main()