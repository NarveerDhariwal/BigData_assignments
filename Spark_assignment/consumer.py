import argparse
import json
import time
from bson import BSON
from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from bson.objectid import ObjectId

from pymongo.mongo_client import MongoClient

uri = "mongodb://localhost:27017/"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client["Kafka_data"]

API_KEY = 'SMVPQFYBQJG73XTT'
API_SECRET_KEY = 'PpwLhHokOo1DVJvOSGu1eBsf28esPTuUb+XXNMAZlrzcEp3IeQQ4RlfBDxSVepT8'
BOOTSTRAP_SERVER = 'pkc-41p56.asia-south1.gcp.confluent.cloud:9092'
SECURITY_PROTOCOL = 'SASL_SSL'
SSL_MACHENISM = 'PLAIN'
ENDPOINT_SCHEMA_URL  = 'https://psrc-znpo0.ap-southeast-2.aws.confluent.cloud'
SCHEMA_REGISTRY_API_KEY = 'JHDOPQN2YVYWVFYM'
SCHEMA_REGISTRY_API_SECRET = 'OzSKr2HLOrbjeXrd0kkA1EHHiY44pxeFO6oYRyM8fa7DprpH9HWesFalgkg258jz'


def sasl_conf():

    sasl_conf = {'sasl.mechanism': SSL_MACHENISM,
                 # Set to SASL_SSL to enable TLS support.
                #  'security.protocol': 'SASL_PLAINTEXT'}
                'bootstrap.servers':BOOTSTRAP_SERVER,
                'security.protocol': SECURITY_PROTOCOL,
                'sasl.username': API_KEY,
                'sasl.password': API_SECRET_KEY
                }
    return sasl_conf



def schema_config():
    return {'url':ENDPOINT_SCHEMA_URL,
    
    'basic.auth.user.info':f"{SCHEMA_REGISTRY_API_KEY}:{SCHEMA_REGISTRY_API_SECRET}"

    }

class Case:
    def __init__(self,record:dict):
        for k,v in record.items():
            setattr(self,k,v)

    @staticmethod
    def dict_to_case(data:dict,ctx):
        return Case(record=data)
    
    @staticmethod
    def dict_to_case1(data:dict,ctx):
        return data
     

def main(topic):

    schema_registry_conf = schema_config()
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    # subjects = schema_registry_client.get_subjects()
    # print(subjects)
    subject = topic+'-value'

    schema = schema_registry_client.get_latest_version(subject)
    schema_str=schema.schema.schema_str

    json_deserializer = JSONDeserializer(schema_str,
                                         from_dict=Case.dict_to_case1)

    consumer_conf = sasl_conf()
    consumer_conf.update({
                     'group.id': 'group1',
                     'auto.offset.reset': "earliest"})

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    count = 0
    timeout = time.time() + 60*0.5 # 30 sec exit

    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)
            if msg is None:
                if time.time() > timeout:
                    print("There is no message for long time hence existing")
                    break
                else:
                    continue

            case = json_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
                
            if case is not None:
                print("User record {}: case: {}\n"
                      .format(msg.key(), case))
                count+=1
                #case_dict = case.__dict__
                #print(type(case_dict))
                #print(case_dict)
                #coll = db["Cases"]
                print(count)
                try:
                    #coll.insert_one(case_dict)
                    coll.insert_one(case)
                    print(f"Data inserted to Mongodb database {db} into collection {coll}")
                except Exception as err:
                    print(err)
       
                
        except KeyboardInterrupt:
            break

    consumer.close()

topic_list = ["Case_topic", "country_wise_latest_topic1", "covid_19_clean_complete_topic", "day_wise_topic1",
"Region_topic","TimeProvince_topic"]

for i in topic_list:
    if i == "Case_topic":
        coll = db['Case_data']
        print("Starting filling Case_data")
        main(i)
        print("Filled Case_data")
        time.sleep(15)
    elif i == "country_wise_latest_topic1":
        coll = db['country_wise_latest_data']
        print("Starting filling country_wise_latest_data")
        main(i)
        print("Filled country_wise_latest_data")
        time.sleep(25)
    elif i == "covid_19_clean_complete_topic":
        coll = db['covid_19_clean_complete_data']
        print("Starting filling covid_19_clean_complete_data")
        main(i)
        print("Filled covid_19_clean_complete_data")
        time.sleep(15)
    elif i == "day_wise_topic1":
        coll = db['day_wise_data']
        print("Starting filling day_wise_data")
        main(i)
        print("Filled day_wise_data")
        time.sleep(15)
    elif i == "Region_topic":
        coll = db['Region_data']
        print("Starting filling Region_data")
        main(i)
        print("Filled Region_data")
        time.sleep(15)
    elif i == "TimeProvince_topic":
        coll = db['TimeProvince_data']
        print("Starting filling TimeProvince_data")
        main(i)
        print("Filled TimeProvince_data")
        time.sleep(15)
    else:
        print("All data is stored in DBs")
        break