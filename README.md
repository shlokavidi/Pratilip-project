# Pratilipi-project
Dockerized Django app (backend) for user, content and interaction CRUD and other APIs 


## Built With
* Python
* MySQL
* Django
* Dockers
* Postman (for testing)

# Getting Started
You can get this project running by following these steps

## Prerequisites
* Docker-compose
* Postman

## Installation and running
1. Clone the repo
```
git clone https://github.com/shlokavidi/Pratilipi-project
```
2. Start Dockers
4. Go to `docker_django_pratilipi` and build docker-compose
```
docker-compose build
```
5. Run docker-compose
```
docker-compose up
```
6. If you want to run in background use
```
docker-compose up -d
```

## Usage
IMPORTANT: When docker runs the application, it does not have any databases and tables. I have automated creation of databases and tables, and data ingestion using Postman form-data. Steps to follow:
1. Open Postman
3. Type your URL
```
http://<ip_address>:9092/proj1/
```
3. Using Data Ingestion API:
  - NOTE: Please refer to the [API Document](https://docs.google.com/document/d/1YhkWb0Zs0tW5r4JXX3E806JOytEsdPrSEtpB2iICXNg/edit?usp=sharing) for information on how to use all APIs
  - In Postman, go to Body > form-data:
    - Fill key as ‘csv_file’ and choose type as ‘File’ and upload the csv file in value
    - Fill key as ‘file_type’ and fill value as ‘user_data’, ‘content_data’ or ‘interaction_data’ based on which data you are uploading

4. Using Operational APIs:
  - In Postman, go to Body > raw:
  - As an example type the following in the raw text field. 
  ```
  {
   "user_api" : "get_user",
   "user_id" : 1,
   "firstname":"John",
   "lastname": "Glenden",
   "email": "JG@gmail.com",
   "phone_number": "123467890",
   "content_id": 3,
   "title": "Lean In",
   "story": "story----------------7",
   "date_published": "2022-01-04",
   "last_accessed": "2022-02-04",
   "limit": 5
  }

  ```
5. Refer to the [API document](https://docs.google.com/document/d/1YhkWb0Zs0tW5r4JXX3E806JOytEsdPrSEtpB2iICXNg/edit?usp=sharing) on how to use all APIs
6. Links to sample CSV files:
* [user_data](https://drive.google.com/file/d/198MT2cCjwFkkanQTtpL_bog-1VaBk4XX/view?usp=sharing)
* [content_data](https://drive.google.com/file/d/1YtGvpvz5iwZoICvUsvOgk6QaQCnaFBzN/view?usp=sharing)
* [interaction_data](https://drive.google.com/file/d/1BSSFADDq5Luzv1hd0dxMWD7r0eub3kXL/view?usp=sharing)
