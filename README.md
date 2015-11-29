# court-case-viewer
This is an Android application designed to view the scheduled court cases for a particular day's session of the Indian Supreme Court.
Primary URL : http://http://52.24.198.10
( This url will give 404 as there is nothing directly there.)

We have 2 main apps inside the main application. 
Home, Cases
Please go through the models.py file and api.py file in the code base for the above apps. 


1. Home : Following models : judge, lawyers, userprofile, user. 

You can do the crud operations on each of these models via the api. ( create update and delete)

E.g.
Get data
http://http://52.24.198.10/home/api/judge/?format=json

Will give all the judges available. 

Create Judge( This class/Model has 2 fields. User and Type. )
Post request to :  http://http://52.24.198.10/home/api/judge/ 

data = {"user":"/home/api/user/1/","type":"Supreme Court"}
Using this data you can send a post request to the above urla nd it will create a new judge object. 

"user":"/home/api/user/1/" : This indicates that a the user with id 1 and which can be found via rest api at the above url is the foreign key in the judge model/class/table

To access individual objects http://http://52.24.198.10/home/api/user/1/?format=jsonn

The same can be used for every model/class in the above apps. 

2. Cases : Following models are available. Court, CaseSearch, Cases, CaseFilter

All of these will be exactly same as the above except the urls will be different. 
e.g.
 http://http://52.24.198.10/cases/api/court/?format=json
