**Real-time Data Streaming and Analysis**
This project focuses on building a real-time data pipeline using Confluent Kafka and Python to stream and analyze the COVID-19 dataset. The pipeline includes data streaming, data storage in MongoDB, and data analysis using PySpark, Spark SQL, and Spark UDFs.

**Project Overview**

Utilized Confluent Kafka and Python to implement a real-time data pipeline for streaming COVID-19 dataset.
Loaded the data into MongoDB using a Kafka consumer for efficient storage and retrieval.
Conducted comprehensive data analysis using PySpark, Spark SQL, and Spark UDFs.
Performed ETL operations such as data cleansing, filtering, sorting, and aggregation.
Developed custom Spark UDFs to enhance data manipulation and categorization.
Leveraged MongoDB as a scalable database solution for seamless data storage and retrieval.

**Project Structure**

data_pipeline.py: Python script implementing the Kafka data pipeline.
data_analysis.py: PySpark script for performing data analysis on the COVID-19 dataset.
spark_udfs.py: Spark UDF functions for custom data manipulation.
README.md: Project documentation and instructions.

**Getting Started**
Clone the repository: git clone https://github.com/your-username/real-time-data-streaming.git.
Install the required dependencies: pip install confluent-kafka pyspark pymongo.
Configure the Kafka producer to stream the COVID-19 dataset.
Start the Kafka consumer to load the data into MongoDB.
Execute the data analysis script using PySpark for in-depth exploration.
Customize and extend the analysis by modifying Spark UDFs in spark_udfs.py.

Dependencies
Confluent Kafka: Link to Confluent Kafka.
PySpark: Link to PySpark.
MongoDB: Link to MongoDB.
Contributions
Contributions to this project are welcome. Feel free to open issues or submit pull requests to enhance the functionality or documentation.

License
This project is licensed under the MIT License.
