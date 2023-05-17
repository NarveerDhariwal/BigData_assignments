import argparse
import cassandra

from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

cloud_config= {
         'secure_connect_bundle': 'secure-connect-kafka-cassandra-demo.zip'
}
auth_provider = PlainTextAuthProvider('benQFZLoDBsMhvjcvLOOYsGc', '4_nHHH3XxZjgvpQrgWnPIgiISWMElkUk7Sz69l2LXbQkswRjbDrIUhRs0_-Fm-Ctzmm,QTcgw0gFfHn7zeZ-Mv7Mugo96El3iCqNDp0BleHZHECuuu8Z3E46UzOrQcsc')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()
session.set_keyspace('employee_data')
session.set_keyspace('employee_data')

result = session.execute("select release_version from system.local")

row = result.one()

# print(row)
if row:
      print(row[0])
else:
      print("An error occurred.")

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


def main(topic):

    schema_registry_conf = schema_config()
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    # subjects = schema_registry_client.get_subjects()
    # print(subjects)
    subject = topic+'-value'

    schema = schema_registry_client.get_latest_version(subject)
    schema_str=schema.schema.schema_str

    json_deserializer = JSONDeserializer(schema_str,
                                         from_dict=Employee.dict_to_employee)

    consumer_conf = sasl_conf()
    consumer_conf.update({
                     'group.id': 'group1',
                     'auto.offset.reset': "latest"})

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    count = 0

    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            employee = json_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))

            if employee is not None:
                level = ''
                if employee.age < 16:
                    level = 'Junior'
                elif employee.age>=16 and employee.age<18:
                    level = 'Mid-level'
                else:
                    level = "Senior"
            
                try: 
                    query = "INSERT INTO employee (entry_num, id, name, age, level) "
                    query = query + " VALUES (%s, %s, %s, %s, %s) "
                    session.execute(query, (employee.entry_num, employee.id, employee.name, employee.age, level)) 
    
                    print("Values has been entered to Cassandra!!")
                except Exception as e:
                    print(f"Value filling is failed failed!! Error : {e}")
                
                print("User record {}: employee: {}\n"
                      .format(msg.key(), employee))
                count+=1
                print(count)
        except KeyboardInterrupt:
            break

    consumer.close()

main("kafka_project")