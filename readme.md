_____________________
Project description

api_bonds is an RESTful APi to allow user different types of transactions involving the bonds transactions.

The api was developed in Flask to achieve an easy deployment.

Also it was implemented a database made in sqlite to facilitate the deployment and installation of the project in different environments because of it's serverless attributes.

The bonds and user modules are contained in the app/main folder.
Each of the parts of the bonds and user modules were divided in controllers, services and models to let us expand our api as much as we want with the desired modularity to maintain the quality and organization of the project.

To make the project flexible and organized it was implemented a blueprint arquitecture to register each developed module in their own separated environment.

Also swagger was implemented to maintain the documentation of the endpoints that are under develop.
______________
Installation

First of all, you should make a virtual environment

$virtualenv env

Then, activate it with

$source env/bin/activate

Now, to install the project dependencies you can run the command make install

$make install

___________
Run

To deploy the project follow the next steps:
Build the docker image
$make build

Finally run the docker image
$make run

If succedeed it should be accessible from the URL: http://localhost:7000/

_______________
REST API

The api documentation of endpoints can be viewed at http://localhost:7000/

_______________
Getting started

To make a complete use of the api, it is needed to create a user, for this we're going to use the following endpoint:

http://localhost:7000/user/register 

Method: POST

request:
{
    "user": String,
    "password": String
}

response:
{
    "message": String
}

Once we've created our new user, we need to login to the api to get our token to access to the others api's services, for this we should make a call to the login service and send our authorization credentials through the headers, (if usng postman "Authorization->Basic Auth"):

http://localhost:7000/user/login 

Method: POST

{
    "message": String
    "token": String
}

Now we are going to be able to call to any of the others services just by sending our token through the "x-access-tokens" header.

