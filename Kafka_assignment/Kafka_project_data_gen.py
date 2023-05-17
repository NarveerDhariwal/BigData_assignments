import psycopg2
import subprocess
import random
import names


conn = psycopg2.connect(
    host="localhost",
    database="Kafka_project_psql",
    user="postgres",
    password="Narveer@123")

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#cursor.execute("create table employee (entry_num serial, id int, name varchar(20), age int)")
#conn.commit()
i=0
while True:
    input_data=[]
    id1 = random.randint(20,5000)
    name1 = names.get_full_name()
    age1 = random.randint(1,100)
    input_data.append(id1)
    input_data.append(name1)
    input_data.append(age1)
    
    print(input_data)
    sql_insert_query = '''insert into employee(id,name,age) values(%s, %s, %s)'''
    cursor.execute(sql_insert_query,input_data)
    conn.commit()

    subprocess.run(["python", "kafka_project_producer.py"])
    #i+=1


conn.close()
