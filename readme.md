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

This application solves the problem that a user can create a private and secure account, that facilitates the access to events and ticketing options, while enabling a communication stream between users that are connected via a friendship. A user can make a post about an event that friends of that user can comment on or like. This function facilitates the communication around the event while gaging interest levels of those who a user might want to attend the event with. Furthermore, a private message platform can be arranged between friends so that details regarding an event can be discussed in private should they desire. Ticketing and seating options are also available from the app, allowing friends to pick seats next to each other but pay separately, then issued with an invoice linked to the payee. 

The app also allows users to create events with ticketing options and seating options. The user can then share the event with their friends by posting it, friends of the user making the post can also share the original post to gain more exposure. To buy a ticket a user does not have to be friends with the user who created the event should the event creator desire. This allows for the app to be used for small- and large-scale events, these can range from a small dinner at a restaurant where tickets are not required to huge concert that may require expenses like tickets, flights, accommodation, further travel, food, other events etc. 

The app can leverage revenue by suggesting any of these expenses and organising them in app for the user. For example, if you’re going to a concert that starts at 9, the app can suggest a restaurant that has 5 stars that’s walking distance to the concert venue and can arrange a taxi or uber should the user require. And what about if friends at the concert lose each other in the crowds, the app’s private message function is the perfect place to contact all attendees to meet at the kebab shop across the road of the venue.  

The app will allow users to register to create an account where they can store personal information that is protected by entering a password that is matched against a unique email address. The password is hashed using a third-party Flask library called bcrypt to ensure the integrity of the user’s data is maintained. 

Storing info in DB

Hashing passwords

Authorisation

Authentication

Validation

JWT token 

Bcrypt

---

### R2. Describe the way tasks are allocated and tracked in your project.

For this project tasks were allocated and tracked using Atlassian's project management tool 'Trello'. 

<img src="https://upload.wikimedia.org/wikipedia/en/thumb/8/8c/Trello_logo.svg/1280px-Trello_logo.svg.png" alt="Trello Logo" width="30%"/>

Public link to the applications [Trello Board](https://trello.com/invite/b/MSNeGTDP/ATTIbcf6438a9f232f88791835689a108779C4AF2FEE/event-ticketing-api).

* Friday the 12th July '24 update

Initiated board and populated all cards with required functionality.

<img src="DOCS/trello_day1.png" alt="Trello day 1" width="60%"/>

* Monday the 15th July '24 update

Completed readme requirements 1 and 2, plus models and route controllers for Users, Posts and Comments. 

<img src="DOCS/trello_15:7.png" alt="Trello 15th July" width="60%"/>

* Tuesday the 16th July '24 update

Completed the models and route controllers for Events, Attendees and Ivoices. 

<img src="DOCS/trello_16:7.png" alt="Trello 16th July" width="60%"/>

* Wednesday the 17th July '24 update

Completed the models and route controllers for likes. Completed validation and started on Authorisation.  

<img src="DOCS/trello_17:7.png" alt="Trello 17th July" width="60%"/>

* Thursday the 18th July '24 update

Today marks the mid-point of the assignment, so a holistic assessment was made regarding the importance of the cards and what would be most beneficial to the assignment and my learning outcomes. It was decided that since the code was fresh in my head, the most efficient and beneficial approach was to finish the validation and authorisation card before tackling the readme requirements that were due today. I approved this idea because I have completed easily more than half the assignment at the half-way point and wanted to continue working on the code so that it functions properly before moving onto something else. This was a good decision because I struggle moving onto a new task if the current task is not completed to a satisfactory standard. 

I therefore changed the due dates of readme requirements 4 and 5 to the 23rd of July, this will allow me plenty of time to get my code functioning without errors and with the required validation and authorisation, which is taking me longer than anticipated. 

<img src="DOCS/trello_18:7.png" alt="Trello 17th July" width="60%"/>

---

### R3 List and explain the third-party services, packages and dependencies used in this app.

### Flask

<img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/flask-logo-icon.png" alt="Flask logo" width="30%"/>

- Flask is a lightweight WSGI web application framework for Python, designed to enable quick and easy development of web applications. It follows a simple, modular design that allows developers to choose the components they need, making it highly flexible and extensible. Flask supports extensions for adding functionality like form validation, authentication, and database integration. Its simplicity and ease of use make it an ideal choice for both beginners and experienced developers looking to build scalable and maintainable web applications.

### Marshmallow
<img src="https://avatars.githubusercontent.com/u/10334301?v=4" alt="Marshmallow logo" width="30%"/>

- Marshmallow is a framework-agnostic library for serializing and deserializing complex data types, such as objects, into native Python datatypes.

### SQLAlchemy 

- SQLAlchemy is a comprehensive SQL toolkit and Object Relational Mapper (ORM) for Python, offering developers extensive power and flexibility with SQL.

### bcrypt
<img src="https://repository-images.githubusercontent.com/240517419/8d034080-4f50-11ea-95f2-1a9685536167" alt="Bcrypt logo" width="30%"/>

- Bcrypt is a cryptographic hash function designed to securely store passwords by transforming them into a fixed-length string using a one-way hash function, making it irreversible. It adds a random "salt" to each password to ensure unique hashes, and employs a "cost factor" to determine the number of iterations for hashing, enhancing security by making it computationally expensive to crack. Bcrypt is favored over faster algorithms like SHA256 for password storage due to its resistance to brute force and dictionary attacks.

### Psycopg2-binary
<img src="https://open-telemetry.github.io/opentelemetry-sqlcommenter/images/psycopg2-logo.png" alt="Psycopg2 logo" width="30%"/>

- Psycopg2-binary is a production-ready PostgreSQL adapter for Python, designed to facilitate the connection and interaction between Python applications and PostgreSQL databases. It provides efficient, high-performance database access, supporting advanced features like asynchronous communication and notification, COPY command support, and more. 

#### Flask-JWT-Extended
<img src="https://seeklogo.com/images/J/jwt-logo-11B708E375-seeklogo.com.png" alt="JWT Web Token logo" width="30%"/>

- WT-Extended is a Flask extension that provides robust support for JSON Web Tokens (JWTs), enhancing security in Flask applications by allowing developers to create, manage, and validate JWTs easily. It includes features like token refreshing, complex access control, and various token storage options, making it versatile for handling authentication and authorization in modern web applications. JWT-Extended simplifies implementing secure user authentication workflows, ensuring sensitive information is safely transmitted between clients and servers.

### python-dotenv

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHaNT3Fi8RMNUpPDk-Zddeo2FTvDN3Sye5AA&s" alt=".Env logo" width="30%"/>

- Dotenv, or .env, is a simple module that loads environment variables from a .env file into a project's environment. This file typically contains key-value pairs, such as API keys, database URLs, and other configuration settings, allowing developers to manage sensitive information and configuration details separately from the codebase. By keeping these variables in a .env file, it enhances security and makes it easier to configure different environments (e.g., development, testing, production) without altering the code.

### App Requirements not mentioned above

* blinker
* click
* Flask-Bcrypt
* flask-marshmallow
    - Flask-Marshmallow provides a thin integration layer for Flask and Marshmallow, enhancing Marshmallow with additional features tailored for Flask applications.
* Flask-SQLAlchemy
    - Flask-SQLAlchemy is an extension that simplifies the integration of SQLAlchemy into Flask applications, making database interactions more straightforward.
* itsdangerous
* Jinja2
* MarkupSafe
* marshmallow-sqlalchemy
    - Marshmallow-SQLAlchemy integrates Marshmallow's serialization and deserialization capabilities with SQLAlchemy, facilitating the conversion of SQLAlchemy models to and from Python datatypes.
* packaging
* PyJWT
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

#### Pro's

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
    - pgAdmin
    - DataGrip
    - TablePlus
    - DBeaver
    - Postbird
    - OmniDB
    - Navicat
* The database system can store and handle large amounts of data.

 
(PostgreSQL: a closer look at the object-relational database management system n.d.)


#### Con's

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

#### Initial Draft ERD 
Submitted on the 12th of July for approval.
![Draft ERD image](DOCS/music_socialmedia.drawio.png)

<br>

#### Example of an unnormalised Events Table.
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