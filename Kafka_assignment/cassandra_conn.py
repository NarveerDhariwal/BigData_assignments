import cassandra

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

cloud_config= {
         'secure_connect_bundle': 'secure-connect-kafka-cassandra-demo.zip'
}
auth_provider = PlainTextAuthProvider('benQFZLoDBsMhvjcvLOOYsGc', '4_nHHH3XxZjgvpQrgWnPIgiISWMElkUk7Sz69l2LXbQkswRjbDrIUhRs0_-Fm-Ctzmm,QTcgw0gFfHn7zeZ-Mv7Mugo96El3iCqNDp0BleHZHECuuu8Z3E46UzOrQcsc')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

session.set_keyspace('employee_data')

result = session.execute("select release_version from system.local")

row = result.one()

# print(row)
if row:
      print(row[0])
else:
      print("An error occurred.")

# Creating table for query1 

create_query1 = """CREATE TABLE IF NOT EXISTS employee (entry_num int, id int, name text, age int, level text, PRIMARY KEY (entry_num))"""

try: 
    session.execute(create_query1)
    print("Table Created!!")
except Exception as e:
    print(f"Table creation failed!! Error : {e}")