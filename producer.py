import argparse
from uuid import uuid4
from six.moves import input
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
#from confluent_kafka.schema_registry import *
import pandas as pd
from typing import List
import os
import json
import glob
import time


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

def delivery_report(err, msg):
    """
    Reports the success or failure of a message delivery.
    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    """

    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))



def case_to_dict(case, ctx):
    
    return case

def read_csv(file_path):
    df = pd.read_csv(file_path)
    columns = list(df.columns)
    df = df.fillna("unknown")
    for data in df.values:
        dict_data = dict(zip(columns,data))
        yield dict_data

def main(topic):
    schema_registry_conf = schema_config()
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    # subjects = schema_registry_client.get_subjects()
    # print(subjects)
    subject = topic+'-value'

    schema = schema_registry_client.get_latest_version(subject)
    schema_str=schema.schema.schema_str

    string_serializer = StringSerializer('utf_8')
    json_serializer = JSONSerializer(schema_str, schema_registry_client, case_to_dict)

    producer = Producer(sasl_conf())

    print("Producing user records to topic {}. ^C to exit.".format(topic))
    #while True:
        # Serve on_delivery callbacks from previous calls to produce()
    producer.poll(0.0)
    i=0
    try:
        for case in read_csv(file_path=FILE_PATH):
            #print(type(case))
            
            producer.produce(topic=topic,
                                key=string_serializer(str(uuid4())),
                                value=json_serializer(case, SerializationContext(topic, MessageField.VALUE)),
                                on_delivery=delivery_report)
            
            #print(case)
        
            #break
    except KeyboardInterrupt:
        pass
    except ValueError:
        print("Invalid input, discarding record...")
        pass

    print("\nFlushing records...")
    producer.flush()

files = glob.glob("*.csv")

for i in files:
    if i == 'Case.csv':
        FILE_PATH = i
        main("Case_topic")
        print("Data successfully moved to kafka for Case_topic")
        time.sleep(15)
    elif i == 'country_wise_latest.csv':
        FILE_PATH = i
        main("country_wise_latest_topic1")
        print("Data successfully moved to kafka for country_wise_latest_topic1")
        time.sleep(15)
    elif i == 'covid_19_clean_complete.csv':
        FILE_PATH = i
        main("covid_19_clean_complete_topic")
        print("Data successfully moved to kafka for covid_19_clean_complete_topic")
        time.sleep(15)
    elif i == 'day_wise.csv':
        FILE_PATH = i
        main("day_wise_topic1")
        print("Data successfully moved to kafka for day_wise_topic1")
        time.sleep(15)
    elif i == 'Region.csv':
        FILE_PATH = i
        main("Region_topic")
        print("Data successfully moved to kafka for Region_topic")
        time.sleep(15)
    elif i == 'TimeProvince.csv':
        FILE_PATH = i
        main("TimeProvince_topic")
        print("Data successfully moved to kafka for TimeProvince_topic")
        time.sleep(15)
    else:
        continue
