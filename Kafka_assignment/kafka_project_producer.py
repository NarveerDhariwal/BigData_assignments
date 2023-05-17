import psycopg2
import pandas as pd
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

API_KEY = 'QBIG6LYZPDX4YDPZ'
ENDPOINT_SCHEMA_URL  = 'https://psrc-5mn3g.ap-southeast-2.aws.confluent.cloud'
API_SECRET_KEY = '/XkYn3HZxaI7Z/4VbseUUCs2CNe4wUB9OOoyEBM/rqr/6911johXzPMW0b1iShvO'
BOOTSTRAP_SERVER = 'pkc-xrnwx.asia-south2.gcp.confluent.cloud:9092'
SECURITY_PROTOCOL = 'SASL_SSL'
SSL_MACHENISM = 'PLAIN'
SCHEMA_REGISTRY_API_KEY = 'BHE5VWNZBC5EB32A'
SCHEMA_REGISTRY_API_SECRET = 'n/imsRSTYEBZ+7aK2uLqah2IY9K02ULZ09iqIrk66oHU7TJjOxT7MRNbHB7GOiB4'


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


conn = psycopg2.connect(
    host="localhost",
    database="Kafka_project_psql",
    user="postgres",
    password="Narveer@123")

cursor = conn.cursor()

cursor.execute("select * from employee order by entry_num desc limit 1")
data = cursor.fetchall()
conn.commit()
conn.close()
columns = ['entry_num', 'id', 'name', 'age']

df = pd.DataFrame(data)

class Employee:
    def __init__(self,record:dict):
        for k,v in record.items():
            setattr(self,k,v)
        
        self.record=record
   
    @staticmethod
    def dict_to_employee(data:dict,ctx):
        return Employee(record=data)

    def __str__(self):
        return f"{self.record}"

def get_employee_data(df):
    for d in df.values:
        employees = []
        employee=Employee(dict(zip(columns,d)))
        employees.append(employee)
        yield employee
        print(employee)

def employee_to_dict(employee:Employee, ctx):
    """
    Returns a dict representation of a User instance for serialization.
    Args:
        user (User): User instance.
        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.
    Returns:
        dict: Dict populated with user attributes to be serialized.
    """

    # User._address must not be serialized; omit from dict
    return employee.record



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


def main(topic):
    schema_registry_conf = schema_config()
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    # subjects = schema_registry_client.get_subjects()
    # print(subjects)
    subject = topic+'-value'

    schema = schema_registry_client.get_latest_version(subject)
    schema_str=schema.schema.schema_str

    string_serializer = StringSerializer('utf_8')
    json_serializer = JSONSerializer(schema_str, schema_registry_client, employee_to_dict)

    producer = Producer(sasl_conf())

    print("Producing user records to topic {}. ^C to exit.".format(topic))
    #while True:
        # Serve on_delivery callbacks from previous calls to produce()
    producer.poll(0.0)
 #   i=0
    try:
        for employee in get_employee_data(df):
            print(employee)
            producer.produce(topic=topic,
                                key=string_serializer(str(uuid4())),
                                value=json_serializer(employee, SerializationContext(topic, MessageField.VALUE)),
                                on_delivery=delivery_report)
#            break
    except KeyboardInterrupt:
        pass
    except ValueError:
        print("Invalid input, discarding record...")
        pass

    print("\nFlushing records...")
    producer.flush()

main("kafka_project")