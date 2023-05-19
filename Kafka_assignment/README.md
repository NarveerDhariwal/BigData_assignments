**Data Extraction, Transformation, and Storage Pipeline**

This project focuses on building an efficient data pipeline for extracting, transforming, and storing data using Python, Kafka messaging, MySQL, and Cassandra. The pipeline includes data extraction from Python-generated sources, necessary transformations using Python scripting, storage in MySQL for efficient retrieval, and loading transformed data into Cassandra for further analysis and processing capabilities.

**Project Overview**

Generating the data by python code or we can also extracted data from Python-generated sources using custom scripts.

Stored the transformed data in PostgreSQL for efficient retrieval and query processing.

Utilized Kafka messaging for reliable and real-time data transfer within the pipeline.

Developed a Kafka producer for collecting and publishing data to the Kafka topics.

Implemented a Kafka consumer for performing ETL operations and transformations on the data.

Loaded the transformed data into Cassandra NoSQL database for enhanced analysis and processing capabilities.

**Project Structure**
Kafka_project_data_gen.py: Python script for generationg the data so that it can be stored into PostgreSQL database

cassandra.py: Python script for connecting to cloud cassandra and create a keyspace

kafka_project_producer.py: Python script for collecting the data from PostgreSQL and publishing data to Kafka topics.
kafka_project_consumer.py: Python script for consuming data from Kafka topics and performing tranformation and storing it to Cassandra database.

Cassandra is chosen in this project to leverage its scalability, fault tolerance, flexible data model, fast data operations, and columnar storage capabilities. These features enable efficient data loading, analysis, and processing for large-scale and real-time applications.

README.md: Project documentation and instructions.

**Getting Started**
Clone the repository: git clone [https://github.com/NarveerDhariwal/BigData_assignments/new/main/Kafka_assignment]

Install the required dependencies: pip install kafka-python postgreSQL-connector-python cassandra-driver.

Implement necessary transformations in Kafka_project_data_gen.py to prepare the data for storage.

Configure the PostgreSQL database and update the connection details in kafka_project_consumer.py.

Start the Kafka producer using kafka_Project_producer.py to collect and publish data to Kafka topics.

Configure the Cassandra NoSQL database and update the connection details in cassandra_conn.py.

Implement desired ETL operations and transformations in kafka_project_consumer.py to load the transformed data into Cassandra for analysis and processing.

**Dependencies**

Kafka Confluent: (https://www.confluent.io/lp/confluent-kafka/)
Cassandra cloud version by Datastax: [https://www.datastax.com/]

**Contributions**

Contributions to this project are welcome. Feel free to open issues or submit pull requests to enhance the functionality or documentation.
