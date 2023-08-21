# DequeueMessageFromQueueAzurePython
This program dequeues a messsage from a queue created in azure. In addition, it writes the output in the blob storage

#Steps to configure the dequeue
1. Create Service Bus Service in Azure
2. Create a queue within the service bus service in Azure
3. Create a blob storage in Azure
4. Create container within blob storage in Azure
5. It is created the Dequeue service using the default template dequeue within python
6. It is necessary to change the conf of the host.json
   The most important part is the version
   
   "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[2.*, 3.0.0)"
  }

7. It is necessary to configure in local.settings.json the service bus and blob storage endopoints, IF YOU WANT TO RUN THE DEQUEUE LOCALLY.
   
   If we want to run the azure function in azure, it is necessary to configure in configuration
   
   Configuration->Application Settings-> Add New Application Setting
   
   Include a key value pair for the service bus
   
   Name: Name of service bus
   
   Value: endpoint
   
   Include a key value pair for the storage
   
   Name: Name of storage
   
   Value: endpoint

8. It is necessary to change the function.json

   
   {
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "name": "msg",
      "type": "serviceBusTrigger",
      "direction": "in",
      "queueName": "Name of queue",
      "connection": "Name of connection"
    }
  ]
}


9. It is necessary to include the libraries in the requirements.txt


azure-functions

numpy

azure-servicebus

azure-storage-blob

azure-identity

requests



   
