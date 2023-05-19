**Real-time Data Streaming and Analysis**
This project focuses on building a real-time data pipeline using Confluent Kafka and Python to stream and analyze the COVID-19 dataset. 
The pipeline includes data streaming, data storage in MongoDB, and data analysis using PySpark, Spark SQL, and Spark UDFs.

**Project Overview**

Utilized Confluent Kafka and Python to implement a real-time data pipeline for streaming COVID-19 dataset.

Loaded the data into MongoDB using a Kafka consumer for efficient storage and retrieval.

Conducted comprehensive data analysis using PySpark, Spark SQL, and Spark UDFs.

Performed ETL operations such as data cleansing, filtering, sorting, and aggregation.

Developed custom Spark UDFs to enhance data manipulation and categorization.

Leveraged MongoDB as a scalable database solution for seamless data storage and retrieval.

**Project Structure**

producer.py: Python script implementing the Kafka data pipeline. It is reading the csv files and sending it to kafka producer.

consumer.py: Reading the data from producer and dumping it into MongoDB. Here, we can also perform the multiple transformation before sending data into mongoDB.

spark_analysis.txt: Contains spark code (due to my system configuration i couldn't connect my mongoDB with spark so i direct did the analysis on csv file)

README.md: Project documentation and instructions.

**Getting Started**
Clone the repository: git clone [https://github.com/NarveerDhariwal/BigData_assignments/tree/main/Spark_assignment]

Install the required dependencies: pip install confluent-kafka pyspark pymongo.

Configure the Kafka producer to stream the COVID-19 dataset.

Start the Kafka consumer to load the data into MongoDB.

Execute the data analysis script using PySpark for in-depth exploration.

**Dependencies**

Confluent Kafka: https://www.confluent.io/confluent-cloud/pricing/

PySpark: Can be installed as docker image https://hub.docker.com/r/jupyter/pyspark-notebook

MongoDB: https://www.mongodb.com/try/download/community

**Contributions**

Contributions to this project are welcome. Feel free to open issues or submit pull requests to enhance the functionality or documentation.

