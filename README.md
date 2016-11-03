# proj6-mongo
Simple list of dated memos kept in MongoDB database
AUTHOR: Brian Leeson, bel@cs.uoregon.edu  
Skeleton code created by instructor: Michael Young

## What is here

A simple Flask app that can create, delete and display dated memos in a MongoDB database and servers them to the user.

## Installation and running
Project only runnable with client_secrets.py, not included in the repo.

The user must have mongodb and pyenv installed:  
sudo apt-get update  
sudo apt-get upgrade  
sudo apt-get install mongodb-server  
sudo apt-get install python3-venv  

git clone <URL> 
cd to the cloned repository  

Run mongod server: mongod --dbpath ~/\<pathToDB> --port 27333

create the database: python3 create_db.py

In a separate window (keep mongod running) on the same machine: 
make configure  
make run  

The default port is 5000. If your are on your own machine connect at localhost:5000.
If the server is running another machine connect at :5000.

## Testing the application

Test this server by following the RUNNING instructions and attempt to connect to the server.

To run automated tests:
make test


