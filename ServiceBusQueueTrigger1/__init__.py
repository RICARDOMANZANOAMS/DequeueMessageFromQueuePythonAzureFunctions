import logging
import json
import time
from azure.servicebus import ServiceBusClient, ServiceBusReceiver
import requests
from azure.storage.blob import BlobClient,BlobServiceClient,ContainerClient

MAX_CONCURRENT_CALLS=1
DYNAMIC_CONCURRENCY_ENABLED=False

connection_string_blob = "Paste connection string from blob storage"
container_name='Paste container name'
blob_service_client=BlobServiceClient.from_connection_string(connection_string_blob)
container_client=blob_service_client.get_container_client(container_name)



connstr ='Paste connection string form queue'
queue_name ='Paste name of the queue'

with ServiceBusClient.from_connection_string(connstr) as client:   #create client
    with client.get_queue_receiver(queue_name, max_concurrent_calls=MAX_CONCURRENT_CALLS, dynamic_concurrency_enabled=DYNAMIC_CONCURRENCY_ENABLED) as receiver:  #We configure to dequeue only 1 message at a time. We configure dynamic concunrency since we can replicate this service automatically
        for msg in receiver:   #Read the message received
            properties=msg.application_properties   #Obtain properties of the message
           
            string_dict={}                  #Dict to store the necessary info
            for key,value in properties.items():  #Extract info from message properties
                key_decode=key.decode("utf-8")   #Decode the message
                if key_decode=='RequestGUID':     #Extract RequesGUID.
                    guid=value.decode("utf-8")+".txt"  #Decode and create the name of the file that we will write on the blobstorage
                    print("guid")
                    print(guid)
                    break
                        
           
            string_message=str(msg)           #Transform the message receive from the queue message to string
            encode_text=string_message.encode('utf-8')  #encode the message       
            try:
                url='https://ricardoexample.azurewebsites.net'  #this is the endopoint that processes the input
                #url='http://172.17.0.2:5000'
                headers={'Content-type':'text/plain'}   #Specify the headers of the message
                response=requests.request("POST",url,headers=headers,data=encode_text) #Get the response 
                data=response.json()  #Transform the response to JSon
                data=str(data)    #Transform the data to string
            except:
                data="Api"
            
            
            
            blob_client=container_client.get_blob_client(guid)   #Get the blob container
            blob_client.upload_blob(data,overwrite=True)     #Upload the file 
            receiver.complete_message(msg)   # We ack that we process the message successfully
            

        