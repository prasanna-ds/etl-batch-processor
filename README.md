# etl-batch-processor

This project does ETL on hourly batches received about flats in Berlin available for rent 
for rent at immobilienscout24.de.

# Requirement

Transform and Load the hourly data batches in to Redshift.

# Assumptions

File arrives on S3 every hour

# Architecture 

The Architecture involves the following tech stack.

- AWS SQS
- AWS S3
- AWS Lambda
- Python 3.6.6

Justification on Tech Choices:

I decided to go on with the microservices architecture based on the scope of the project as it gives us better `maintanability`, `pause-resume mechanism`, `quick scale-out` and `deployability`.

 1. AWS SQS -> Though for an hourly job where we can create a schedule in a scheduler , for eg. Airflow , SQS gives us the liberty of easily moving from hourly batch processing to near-realtime processing (not of much difference already).The service can easily scale-out and scale-in with sqs. Above all, there may be chances of not receiving a file for a particular hour and receiving it later will not hamper this architecture and there wont be any failures as well because of missing files.
 2. AWS S3 -> Assuming that the input data arrives in s3, the transformed data will be also stored in S3. Storing the data (raw/clean) in s3 gives us the power of having a centralized data repository (datalake).
 3. AWS Lambda -> Lambda is a wonderful serverless service that runs in response to events and automatically manages the computing resources. I have used lambda here to load (COPY) the data from s3 into redshift on arrival of transformed hourly batches.
 
# Data Pipeline Flow

![ARCHITECTURE DIAGRAM](https://github.com/Prasannads/etl-batch-processor/blob/master/blob/master/images/Architecture.jpg)


# Additional/More Tech choices.
1.  We can add Dynamodb in the process of loading redshift to save the name of files that we load and status of the load. 
In this way , we can avoid duplicate file loads into Redshift.

2. We can write a pyspark application and schedule , run via EMR which creates transformed data in S3 and the Lambda function picks it up for loading. Spark applications can handle huge volumes of data with the help of its distributed computing framework.



# How to run this application

```sh
### Python Application to do Extract and Transform hourly batches
### Clone the repository [https://github.com/Prasannads/etl-batch-processor.git]

### First things First . Create a virtual environment and run the tests to make sure we are all set

$ virtualenv etl-batch-processor -p /usr/local/bin/python3.6
    
### and then activate the virtual environment
$ source etl-batch-processor/bin/activate

### install dependecies from Pipfile
$ pipenv install

### run the tests
$ APP_ENV=test pipenv run pytest

### Fill out the following details in /etl-batch-processor/batchprocessor/config/ for respective environments
### Output S3 Bucket
### SQS Queue Name to poll
### AWS Secret key and Access Key - Ideally, we should not be storing the credentials in the applications as it not secure and should be using IAM roles 

### Having completed the preliminary steps , create a docker image by running the following command.
$ docker build -t etl-batch-processor .

### Run the docker image.
$ docker run -d --name etl-batch-processor etl-batch-processor python app.py --env=production

### Lambda function for Loading Redshift ( This has not been tested due to time constraints)
### clone the repository for lambda function which is developed on Serverless Framework.
https://github.com/Prasannads/redshift-loader.git

### Fill out the respective details in the file Serverless.yml

### This function can be packaged and be uploaded to Lambda directly or via s3 or via Serverless commands
$ npm install -g serverless
$ sls plugin install -n serverless-python-requirements

# deploy lambda function
$ sls deploy -v --stage ${env}

```

# Screenshots

### Initial Steps

![INITIAL STEPS](https://github.com/Prasannads/etl-batch-processor/blob/master/blob/master/images/InitialSteps.png)

### Sample Running Application

![SAMPLE RUNNING APPLICATION](https://github.com/Prasannads/etl-batch-processor/blob/master/blob/master/images/RunningApplication.png)

# Data Model

Though it leads to Query Complexities, Snowflake Schema would be a better approach in this case , as with snowflake schema (normalized) we can save lot of space in the data warehouse (Redshift) and when dimension tables require a significant amount of storage space. 

![SAMPLE RUNNING APPLICATION](https://github.com/Prasannads/etl-batch-processor/blob/master/blob/master/images/DataModel.png)
