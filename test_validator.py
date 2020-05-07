import unittest
import json
from validator import ServerVerification

#URl to call REST api
URL = "https://raw.githubusercontent.com/opensource-tnbt/sdv/master/platform_description_18March2020.json"

#File use to check the response
validationFile = "test_data.json"

class TestServerVerification(unittest.TestCase):
    
    def setUp(self):
        self.testServer = ServerVerification(URL,validationFile)

    def test_createObject(self):
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


if __name__ == "__main__":
    unittest.main()