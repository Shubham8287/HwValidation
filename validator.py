import json
import requests

#This programs works well when JSON response and validation file share same schema.

#URl to call REST api
URL = "https://raw.githubusercontent.com/opensource-tnbt/sdv/master/platform_description_18March2020.json"

#File use to check the response
validationFile = "platform_description_18March2020.json"

class ServerVerification:
  
  def __init__(self,URL,validationFile):
    self.URL = URL
    self.validationFile = validationFile
    self.validationSuccess = True

  # function to request api call and load it
  def loadJSON(self):
    response = requests.get(self.URL)
    if(response.ok):
      #serverConfig variable store server configuration in JSON fomat
      self.serverConfig = response.json()
    else:
      print("URL not accessible")
    
    return response

  # load validaton file - file to test the response
  def loadValidationFile(self):
    with open(validationFile, 'r') as f:
      #validConfig variable store requested configuration (which is used to check server config) in JSON fomat
      self.validConfig = json.load(f)


  #recursive function to traverse all node and check correspanding key value in responsefile. 
  def compareNodes(self, serverConfig, validConfig):
  
      if type(validConfig) is dict and validConfig:
          for child_node in validConfig:
              #every key of validation file must present in response file.
              if child_node in serverConfig:
                # if current key is list or dictionary, we need to dig deeper else we can compare values 
                if type(validConfig[child_node]) not in [dict, list]:
                  if validConfig[child_node] != serverConfig[child_node]:
                    print("Mismatch found for the key '"+child_node+"'")
                    self.validationSuccess = False
                else:  
                  self.compareNodes(serverConfig[child_node], validConfig[child_node])
              else:
                  print("API response doesn't have any information for key: '",child_node,"'")
                  self.validationSuccess = False


      elif type(validConfig) is list and validConfig:
          for index in range (0,len(validConfig) ):
                # if current key is list or dictionary, we need to dig deeper else we can compare values 
                if type(serverConfig[index]) in [dict, list]:
                  self.compareNodes(serverConfig[index], validConfig[index])
                else:
                  if( serverConfig[index]!= validConfig[index]):
                    print ("Mismatch found at '",serverConfig[index],"'")
                    self.validationSuccess = False


if __name__ == "__main__":
  verifyServer  = ServerVerification(URL,validationFile)
  verifyServer.loadJSON()
  verifyServer.loadValidationFile()
  verifyServer.compareNodes(verifyServer.serverConfig, verifyServer.validConfig)
  if(verifyServer.validationSuccess):
    print ("valtion passed SUCCESSFULLY!!")
