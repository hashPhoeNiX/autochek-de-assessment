# Data Engineering Technical Assessment

## Getting Started

### Dependencies
* Docker
* docker compose
* Jupyter notebook
* Python
* IDE (e.g. VSCode)

### Installation Guide
* Download and set up docker from the [official page](https://docs.docker.com/get-docker/)
* Install [docker compose](https://docs.docker.com/compose/install/)
* [Optional] Download [Anaconda](https://www.anaconda.com/products/distribution) for easy access to most data science libraries and Jupyter Notebook
* [Postgres](https://hub.docker.com/_/postgres/) docker image
* [pgAdmin 4](https://hub.docker.com/r/dpage/pgadmin4/) docker container
* Install the requirements.txt in the [task_1](task_1) folder using the following commands <\br> ```pip install -r requirements.txt```

## Executing the programs
### Problem statement 1 solution:
* Open the [task_1](task_1) subfolder and run ```docker compose up``` to start the container. 
  > The [docker-compose.yaml](task_1/docker-compose.yaml) file has 2 services postgres and pgadmin.
* Open Jupyter Notebook and run the [upload_data](task_1/upload_data.ipynb) notebook to load the data from the CSV files in the [data](task_1/data) subdirectory directly to the postgres database created from docker-compose.
* The [SQL query](task_1/solution_1.sql) for the expected result in problem statement 1 can can be executed by starting up the pgadmin docker container installed or directly from the [solution](task_1/solution.ipynb) notebook.

### Problem statement 2 solution:
An airflow services was created following the guidelines from the [Running Airflow in docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html) documentation page.
* Open the [airflow](airflow) subdirectory
* Run ```docker compose up``` command in your terminal
* Create a ```.env``` file in the dags folder container the environment variables __API_KEY__ and __API_ID__ required by the [XE  API](https://www.xe.com/xecurrencydata/)
* The code scheduled to run at 1AM and 11PM daily can be found in the [dags](airflow/dags) subdirectory
* The airflow webserver can be accessed through > localhost:8080
* The result from the scheduled execution of the code can be found in the [results](airflow/results) subdirectory
