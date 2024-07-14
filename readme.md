# T2A2: API Webserver

## Work in Progress

## Event Ticketing & Communication RESTful API Application

The main tech-stack used for this application includes:

* Python
* Flask
* PostgrsSQL
* SQLAlchemy

![Flask, Postgres and SQLAlechemy logos](https://miro.medium.com/v2/resize:fill:320:214/1*DmGeEpZpQgApXWuINqHghQ.png)
---

### R1. Explain the problem that this app will solve, and explain how this app solves or addresses the problem.

The problem this application solves is to provide an event goer with the ability to purchase tickets and communicate with friends surrounding everything related to the event. The app will allow users to make posts related to events to gage whether their friends are interested in attending. If so, a user will be able to purchase tickets in app including seating arrangements next to their friends. The app will also provide a private messaging platform for friends to organise all aspects surrounding the event, such as dinner, transport, and flights and accommodation for interstate or international events. 

For this assignment the app will only handle the API routes and payloads, but the finished product will include AI suggested dinner locations, transport, and more. Which will be used to ultimaetly leverage revenue for the app. Plus in app api routes to all major ticketing services for users to purchase from. 

---

### R2. Describe the way tasks are allocated and tracked in your project.

For this project tasks were allocated and tracked using Atlassian's project management tool 'Trello'. 

<img src="https://upload.wikimedia.org/wikipedia/en/thumb/8/8c/Trello_logo.svg/1280px-Trello_logo.svg.png" alt="Trello Logo" width="30%"/>

Public link to the applications [Trello Board](https://trello.com/invite/b/MSNeGTDP/ATTIbcf6438a9f232f88791835689a108779C4AF2FEE/event-ticketing-api).

* 12th July '24

Initiated board and populated all cards with required functionality.

<img src="DOCS/trello_day1.png" alt="drawing" width="60%"/>

---

### R3 List and explain the third-party services, packages and dependencies used in this app.

#### Marshmallow
<img src="https://avatars.githubusercontent.com/u/10334301?v=4" alt="Marshmallow logo" width="30%"/>

#### Bcrypt
<img src="https://repository-images.githubusercontent.com/240517419/8d034080-4f50-11ea-95f2-1a9685536167" alt="Bcrypt logo" width="30%"/>

Used for the hashing of passwords. 

#### Psycopg2-binary
<img src="https://open-telemetry.github.io/opentelemetry-sqlcommenter/images/psycopg2-logo.png" alt="Psycopg2 logo" width="30%"/>

#### JWT Web Token
<img src="https://seeklogo.com/images/J/jwt-logo-11B708E375-seeklogo.com.png" alt="JWT Web Token logo" width="30%"/>

#### .Env

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHaNT3Fi8RMNUpPDk-Zddeo2FTvDN3Sye5AA&s" alt=".Env logo" width="30%"/>



* bcrypt
* blinker
* click
* Flask-Bcrypt
* Flask-JWT-Extended
* flask-marshmallow
* Flask-SQLAlchemy
* itsdangerous
* Jinja2
* MarkupSafe
* marshmallow
* marshmallow-sqlalchemy
* packaging
* psycopg2-binary
* PyJWT
* python-dotenv
* SQLAlchemy
* typing_extensions
* Werkzeug

---

### R4. Explain the benefits and drawbacks of this app’s underlying database system.

There were a few different database management systems (DBMS), both free and paid, that could have been used as the underlying database for this API project. A few of these include:

* Oracle Database
* MySQL
* PostgreSQL
* Redis
* SQLite
* MongoDB
* Elasticsearch
* IBM Db2
* Microsoft Access

As you can probably see by the name, most of the databases listed above use the SQL language, to create, populate, retrieve, delete and update the data stored in their database. In each case of these different databases that use the SQL language, their basic syntax may differ slightly. 

For this question we will be discussing the pro and cons of PostgreSQL, because it was used for this app's underlying database system. 

![Image of PostgreSQL logo](/DOCS/0_vwcP0i8cGx1TKAte.png)

PostgreSQL was one of the first DBMS’s to be created and is still used frequently for web databases found in industry today. It is a free, open-source database, that allows users to control structured and unstructured data. It is a highly flexible database and is used across many industries and scenarios. It is an object relational database, which means that it includes both relational and object-orientated databases. It also can communicate with other modern frameworks such as Ruby on Rails, Node.js or Django. (Object-Relational Database Management System n.d.). A postgreSQL environment can be hosted virtually, physically and in the cloud, and can be used on most operating systems and platforms (such as Linux) (Arsenault 2017). 

##### PROS

* The engine of the database system is scalable. 
* The software is open source.
* Large variety of supported languages (C++, C, PHP, Perl, Java, and of course Python).
* The database supports the commonly used JSON language to communicate with APIs. 
* The database system is cross platform.
* The database system comes with many premade functions to simplify interaction with the database. 
* The database uses a ‘multi-model’ system that works with Semi-Structured Data (JSON, XML), Structured Data (SQL), Key-Value and Spatial Data. 
* It comes as the standard database for any Mac running OSX Lion 10.7 or higher.
* The software uses around only 20 MB. 
* The database is accessible via the terminal.
* There are many Graphical User Interfaces (GUI) that aid in the ease of interaction with the database system. Some of these include:
* pgAdmin
* DataGrip
* TablePlus
* DBeaver
* Postbird
* OmniDB
* Navicat
* The database system can store and handle large amounts of data.

 
(PostgreSQL: a closer look at the object-relational database management system n.d.)


##### CONS 

* Documentation can be more difficult to find than some other competing database systems and expandable documentation is often only in English.
* The configuration method can be confusing to some. 
* In the case of large operations, the speed of execution may slow. 

(Arsenault 2017)

Given these pros and cons, postgrSQL is an ideal database system for those with a limited budget, who may want to scale at some point in the future, value being able to choose their interface, or, for those who want to use the JSON. 

---

### R5. Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app.

The Object Relational Mapping system or ORM used for this application is SQLAlchemy. 

<img src="https://miro.medium.com/v2/resize:fit:1400/0*msfsws06ImMSJYop.jpg" alt="SQLAlchemy logo" width="70%"/>

---

### R6. Design an entity relationship diagram (ERD) for this app’s database, and explain how the relations between the diagrammed models will aid the database design.

Talk in database terms, normalisation, relations - one to many etc, 

##### Initial Draft ERD 
Submitted on the 12th of July for approval.
![Draft ERD image](DOCS/music_socialmedia.drawio.png)

<br>

##### Unnormalised Events Table 
![Unnormalised Events table](DOCS/Unnormalised_events_table.png)

---

### R7. Explain the implemented models and their relationships, including how the relationships aid the database implementation.

SQLAlchemy terms - back populates, cascade
Reasoning behind any changes to the ERD

---

### R8. Explain how to use this application’s API endpoints. Each endpoint should be explained, including the following data for each endpoint:

Explain each endpoint / routes.

Include these for each:
* HTTP verb (get, post, patch, put)
* Path or route ("/posts/1/comments/1" etc)
* Any required body or header data - what the payload will look like (get or delete don't require body), authorisation header - 
* Response - structure of a sample resoonse with examples

Finally (in-code): All queries to the database must be commented with an explanation of how they work and the data they are intended to retrieve 

All images in readme go in DOCS, all source code go into DOCS