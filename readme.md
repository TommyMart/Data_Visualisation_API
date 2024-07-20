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

This application addresses several key issues related to event management and social interactions around events. The primary problem it solves is providing a secure and efficient platform for users to manage event access, ticketing, and communication with friends.

### Problem and Solution Overview:

**Secure Account Creation and Event Access:**

Problem: Users need a secure way to create accounts and manage their personal information while accessing events and ticketing options. <br>
Solution: The app allows users to create private, secure accounts protected by hashed passwords using the bcrypt library. Users can log in with their credentials, and a JWT token is issued for secure session management. This token verifies the user's identity for all interactions, ensuring data integrity and privacy.

**Event Communication and Engagement:**

Problem: Users need a platform to discuss events, gauge interest, and communicate with friends.<br>
Solution: Users can post about events, and friends can comment and like these posts, facilitating communication and interest gauging. Additionally, a private messaging feature allows friends to discuss event details securely.

**Integrated Ticketing and Seating Management:**

Problem: Users want to purchase tickets and select seats, often wanting to sit together but pay separately.<br>
Solution: The app provides ticketing and seating options, allowing users to select seats next to their friends while handling payments individually. An invoice linked to the payee is issued, streamlining the process.

**Event Creation and Sharing:**

Problem: Users need a way to create events, manage ticketing, and share events with a broader audience.<br>
Solution: Users can create events with ticketing and seating options and share these events with their friends through posts. Friends can further share the posts, increasing event exposure. The app supports both small and large-scale events, making it versatile for various event types.

**Revenue Generation through Recommendations:**

Problem: Users often need assistance planning additional aspects of their event experience, such as dining and transportation.<br>
Solution: The app suggests related expenses and services, such as nearby restaurants, transportation options, and other activities. For instance, if a user is attending a concert, the app might recommend a highly-rated restaurant nearby and arrange a taxi or Uber if needed.

**User-Friendly Search and Interaction:**

Problem: Users need an efficient way to find friends and events without needing exact spellings.<br>
Solution: The app allows partial string searches, returning results that include any part of the search input. For example, searching for 'my' would return 'Tommy', 'Amy', 'Sammy', etc.

**Comprehensive Data Management:**

Problem: Users and admins need to manage various data types related to events, posts, comments, and more.<br>
Solution: Users can create, view, update, and delete data they have created, with admins having full authorization to manage the app's data. Data validation ensures that the correct information is stored, such as validating email formats and password strength.

**Seating Section and Ticket Limits:**

Problem: Users need to choose specific seating sections and ensure ticket limits are enforced.<br>
Solution: The app provides different seating sections (General Admission, Section C, B, A, VIP) and enforces limits on ticket sales per section. A CLI function allows checking the total tickets sold for an event.

This comprehensive application effectively addresses the needs of users looking to manage events, communicate with friends, and handle ticketing in a secure and user-friendly manner. Furthermore, not all functionalities mentioned in the above solutions will be implemented in the initial API route design due on the 28th of July. These include the AI suggestions, seat number selection, dynamic total cost invoices, and private messaging.

---

### R2. Describe the way tasks are allocated and tracked in your project.

For this project tasks were allocated and tracked using Atlassian's project management tool 'Trello'. 

<img src="https://upload.wikimedia.org/wikipedia/en/thumb/8/8c/Trello_logo.svg/1280px-Trello_logo.svg.png" alt="Trello Logo" width="30%"/>

Public link to the applications [Trello Board](https://trello.com/invite/b/MSNeGTDP/ATTIbcf6438a9f232f88791835689a108779C4AF2FEE/event-ticketing-api).

* Friday the 12th of July '24 update

Initiated board and populated all cards with required functionality.

<img src="DOCS/trello_day1.png" alt="Trello day 1" width="60%"/>

* Monday the 15th of July '24 update

Completed readme requirements 1 and 2, plus models and route controllers for Users, Posts and Comments. 

<img src="DOCS/trello_15:7.png" alt="Trello 15th July" width="60%"/>

* Tuesday the 16th of July '24 update

Completed the models and route controllers for Events, Attendees and Ivoices. 

<img src="DOCS/trello_16:7.png" alt="Trello 16th July" width="60%"/>

* Wednesday the 17th of July '24 update

Completed the models and route controllers for likes. Completed validation and started on Authorisation.  

<img src="DOCS/trello_17:7.png" alt="Trello 17th July" width="60%"/>

* Thursday the 18th of July '24 update

Today marks the mid-point of the assignment timeline, so I assessed the importance of the tasks and what would be most beneficial for the assignment and overall learning outcome. Since the code was fresh in my mind, I decided that the most efficient and beneficial approach was to finish the validation and authorisation tasks before tackling the README requirements due today. This decision was approved because I have completed more than 60% of the assignment at the half-way point and wanted to continue working on the code until it functions as desired. This was a good decision because I struggle to move on to a new task if the current task is not completed to a satisfactory standard, which can then be detrimental to the new task.

I, therefore, changed the due dates of README requirements 4 and 5 to the 23rd of July. This will allow me plenty of time to get my code functioning without errors and with the required validation and authorisation, which is taking longer than anticipated.

<img src="DOCS/trello_18:7.png" alt="Trello 17th July" width="60%"/>

* Saturday the 20th of July '24 update

After talking with my lecturer Simon via Zoom in the morning, I made a new 'search' card for the Trello board. It required a search function so that the client can search for either a user_name or event_name via the url. The search also needed to be a partial search and return a list should their be multiple matches to the search input. This functionality was completed shortly after and the card was moved to the renamed 'completed' column of the board. Aditionally, readme requirement 4 was moved to completed and a new card for readme requirement 8 was made due to it being missed during the initation stage of the project management process. 

<img src="DOCS/trello_20:7.png" alt="Trello 20th July" width="60%"/>

---

### R3 List and explain the third-party services, packages and dependencies used in this app.

### Flask

<img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/flask-logo-icon.png" alt="Flask logo" width="30%"/>

Flask is a lightweight WSGI web application framework for Python, designed to enable quick and easy development of web applications. It follows a simple, modular design that allows developers to choose the components they need, making it highly flexible and extensible. Flask supports extensions for adding functionality like form validation, authentication, and database integration. Its simplicity and ease of use make it an ideal choice for both beginners and experienced developers looking to build scalable and maintainable web applications.

### Marshmallow
<img src="https://avatars.githubusercontent.com/u/10334301?v=4" alt="Marshmallow logo" width="30%"/>

Marshmallow is a framework-agnostic library for serializing and deserializing complex data types, such as objects, into native Python datatypes. It simplifies data validation and transformation, enabling seamless conversion between Python objects and data formats like JSON. Marshmallow's flexibility and ease of use make it an invaluable tool for managing data in web APIs, database integrations, and other data-intensive applications.

### SQLAlchemy 

SQLAlchemy is a comprehensive SQL toolkit and Object Relational Mapper (ORM) for Python, offering developers extensive power and flexibility with SQL. It allows for full control over SQL statements, supports complex queries, and facilitates the management of database schemas. By bridging the gap between Python objects and relational database tables, SQLAlchemy streamlines database interactions, making it easier to build and maintain scalable applications.

### bcrypt
<img src="https://repository-images.githubusercontent.com/240517419/8d034080-4f50-11ea-95f2-1a9685536167" alt="Bcrypt logo" width="30%"/>

Bcrypt is a cryptographic hash function designed to securely store passwords by transforming them into a fixed-length string using a one-way hash function, making it irreversible. It adds a random "salt" to each password to ensure unique hashes, and employs a "cost factor" to determine the number of iterations for hashing, enhancing security by making it computationally expensive to crack. Bcrypt is favored over faster algorithms like SHA256 for password storage due to its resistance to brute force and dictionary attacks.

### Psycopg2-binary
<img src="https://open-telemetry.github.io/opentelemetry-sqlcommenter/images/psycopg2-logo.png" alt="Psycopg2 logo" width="30%"/>

Psycopg2-binary is a production-ready PostgreSQL adapter for Python, designed to facilitate the connection and interaction between Python applications and PostgreSQL databases. It provides efficient, high-performance database access, supporting advanced features like asynchronous communication and notification, COPY command support, and more. 

#### Flask-JWT-Extended
<img src="https://seeklogo.com/images/J/jwt-logo-11B708E375-seeklogo.com.png" alt="JWT Web Token logo" width="30%"/>

JWT-Extended is a Flask extension that provides robust support for JSON Web Tokens (JWTs), enhancing security in Flask applications by allowing developers to create, manage, and validate JWTs easily. It includes features like token refreshing, complex access control, and various token storage options, making it versatile for handling authentication and authorization in modern web applications. JWT-Extended simplifies implementing secure user authentication workflows, ensuring sensitive information is safely transmitted between clients and servers.

### python-dotenv

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHaNT3Fi8RMNUpPDk-Zddeo2FTvDN3Sye5AA&s" alt=".Env logo" width="30%"/>

Dotenv, or .env, is a simple module that loads environment variables from a .env file into a project's environment. This file typically contains key-value pairs, such as API keys, database URLs, and other configuration settings, allowing developers to manage sensitive information and configuration details separately from the codebase. By keeping these variables in a .env file, it enhances security and makes it easier to configure different environments (e.g., development, testing, production) without altering the code.

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
    - Jinja2 is a fast, extensible templating engine for Python, designed to generate HTML, XML, and other markup formats by combining static templates with dynamic data.
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

**Pro's**

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


**Con's**

* Documentation can be more difficult to find than some other competing database systems and expandable documentation is often only in English.
* The configuration method can be confusing to some. 
* In the case of large operations, the speed of execution may slow. 

(Arsenault 2017)

Given these pros and cons, postgrSQL is an ideal database system for those with a limited budget, who may want to scale at some point in the future, value being able to choose their interface, or, for those who want to use the JSON. 

---

### R5. Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app.

Firstly, lets define what an Object Relational Model (ORM) is. 

According to freecodecamp.com, ‘Object Relational Mapping (ORM) is a technique used in creating a "bridge" between object-oriented programs and, in most cases, relational databases (Abba 2022).’

For example, here is a query in SQL that retrieves data about a user. 

<img src="DOCS/SQL_example.png" alt="SQLAlchemy logo" width="70%"/>

While using an ORM tool the same query can be written like this:  

<img src="DOCS/ORM_example.png" alt="SQLAlchemy logo" width="70%"/>

### Some popular Python ORM’s include
-	Django
-	Web2py
-	SQLObject
-	SQLAlchemy

The Object Relational Mapping system or ORM used for this application is SQLAlchemy. 

<img src="https://miro.medium.com/v2/resize:fit:1400/0*msfsws06ImMSJYop.jpg" alt="SQLAlchemy logo" width="70%"/>

And put in a way relating to our API application, SQLAlchemy is the layer that interacts with the Postgres relational database using SQL language via its own querying methods and an object-oriented programming language like Python. 

#### Some of its main features include:

- **SQL Expression Language**: SQLAlchemy provides a comprehensive suite of well-known enterprise-level persistence patterns, designed to facilitate efficient and high-performing database access. It enables the creation of SQL queries in a Pythonic way, abstracting the complexities of SQL while offering a powerful and flexible way to interact with databases.

- **ORM**: The Object-Relational Mapper (ORM) offers a high-level API for working with database records as Python objects, making it easier to interact with the database using Python code. It supports complex object relationships, lazy loading, and polymorphic inheritance, allowing developers to work with data in a more intuitive and object-oriented manner.

- **Database Connectivity**: SQLAlchemy supports a wide range of major relational databases, including PostgreSQL, MySQL, SQLite, Oracle, and Microsoft SQL Server. This ensures broad compatibility and flexibility, allowing developers to choose the database that best fits their needs without worrying about compatibility issues.

- **Schema Generation**: Automatically generating database schemas from Python classes reduces the need for manual schema creation. This feature ensures that the database schema is always in sync with the application's data models, simplifying development and maintenance.

- **Schema Migration**: SQLAlchemy integrates with Alembic, a lightweight database migration tool for handling database migrations. This integration makes it easy to manage schema changes over time, ensuring that the database evolves with the application without manual intervention.

- **Transactions**: Full support for database transactions ensures data integrity and consistency. SQLAlchemy allows developers to manage transactions easily, providing control over the commit and rollback operations to handle data safely and effectively.

- **SQL Compilation**: SQLAlchemy compiles Python expressions into SQL statements, offering a powerful and expressive way to generate SQL queries. This feature allows developers to write complex queries using Python syntax, making the code more readable and maintainable.

- **Performance**: SQLAlchemy optimizes database access through various techniques such as connection pooling, which reuses database connections, and query caching, which stores the results of frequently executed queries. These optimizations enhance the performance and scalability of database interactions.

- **Extensibility**: Designed with extensibility in mind, SQLAlchemy allows developers to customize and extend its functionality as needed. It provides hooks and plugins for adding new behaviors and integrating with other tools, ensuring that it can adapt to the unique requirements of different projects.

- **Community and Documentation**: SQLAlchemy is backed by a large and active community, providing a wealth of resources, support, and contributions. Comprehensive documentation, including tutorials, guides, and API references, helps developers learn how to use SQLAlchemy effectively and troubleshoot any issues they may encounter.

(Features - SQLAlchemy n.d.)

Now let’s look at how the apps code uses the features, purpose and functionalities of SQLAlchemy. 

For this application SQLAlchemy was assigned to 'db', `db = SQLAlchemy()`, and therfore for the code examples every time we see 'db' we are accessing the SQLAlchemy library features. For further understanding of the SQLAlchemy methods used in the following code, such as commit, select, session, filter_by etc. please refer to the end of this answer for a brief explanation. 

**Models** - when creating a table we use an SQLAlchemy class called ‘Model’, `class User(db.Model):`, creates a model class named ‘users’, that represents a table in the database. 


Table Names - we can then assign a name to the Model class, or table, using `__tablename__ = "users"`, that sets the name to ‘users.

**Columns** – we then create the table columns, or attributes, assigning them individual datatypes and constraints. Examples of the datatypes used in the app are:
-	String
-	Integer
-	Date
-	Float
-	Boolean

And examples of the constraints used in the app are:
-	Primary key
-	Foreign key 
-	Unique 
-	Default
-	Nullable

`id = db.Column(db.Integer, primary_key=True)`
Where ‘id’ is a column of the table, with a datatype of integer and is the primary key of the table. 
`user_id = db.Column(db.Integer, db.ForeignKey('users.id')`
Where 'name' is a column of a table, with a datatype of integer, and is a foriegn key of the 'id' attribute from the users table.
`name = db.Column(db.String, nullable=False)`
Where ‘name’ is a column of the table, with a datatype of string and cannot be null. 

**Relationships** - define how different tables or models relate to each other. 

`‘posts = db.relationship("Post", back_populates="user", cascade="all, delete")’`

Let’s break this code down…
-	`db.relationship` is a function that defines that there is a relationship.
-	`”Post”` is the name of the related model.
-	`back_populates=”user”` - specifies the attribute on the related model that points back to the current model. This indicates that the ‘Post’ model has an attribute ‘user’ that points back to the ‘User’ model.
-	` cascade="all, delete"` - determines that all related objects are deleted when the parent object is deleted. For example, when a user is deleted so are the users posts and comments. 

This code connects the Post model and the user field, a user can make multiple posts, but a post can only be created by one user. 

**Database Interaction**

Next is fetching data from the database, first a SQL statement that determines what data is to be fetched, `db.select(User).filter_by(id=user_id)`, in this case it is a User iteration based on the id passed in the route URL. Then we execute the statement and retrieve the selected data and store it in a variable such as 'user - `user = db.session.scalar(stmt)`. Scalar executes a query that returns a single result, while scalars can return multiple results. Then, if the data is found, it is serialised and returned to the client in the form of JSON - ` return user_schema.dump(user)`. If it is not found, an error message and status code is returned to the client in JSON instead - ` return {"error": f"User with id {user_id} not found"}, 404`.



Here are a few of the more common SQLAlchemy methods, most of which are used in this app but not all, and their purpose:

- **commit**: db.session.commit(): Commits the current transaction, saving all changes made during the transaction to the database.

- **delete**: db.session.delete(instance): Marks an instance (record) for deletion from the database. The change is finalized when commit() is called.

- **session**: db.session: Represents the database session used to manage and persist operations on objects and transactions. It's the main interface for interacting with the database.

- **select**: db.select([columns]): Constructs a SQL SELECT statement to query data from the database. It's used to retrieve records based on certain criteria.

- **add**: db.session.add(instance): Adds a new instance (record) to the session to be inserted into the database upon commit.

- **query**: db.session.query(Model): Creates a query object for the specified model, allowing you to retrieve data from the database using various filtering and ordering methods.

- **filter**: query.filter(condition): Adds filtering conditions to a query, returning only the records that match the specified condition.

- **filter_by**: query.filter_by(**kwargs): Adds filtering conditions to a query using keyword arguments to specify column-value pairs.

- **scalar**: query.scalar(): Executes the query and returns a single scalar result, which is the first column of the first row in the result set.

- **scalars**: query.scalars(): Executes the query and returns an iterator of scalar results, which are the values of the first column for all rows in the result set.

- **all**: query.all(): Executes the query and returns all results as a list of instances.

- **first**: query.first(): Executes the query and returns the first result, or None if no result is found.

- **update**: query.update(values): Performs a bulk update operation on the records that match the query's filter conditions, setting the specified column values.

- **rollback**: db.session.rollback(): Rolls back the current transaction, undoing any changes made during the transaction.

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

### Authentication

***Login*** <br>
URL Path: http://localhost:8080/auth/login <br>
Method: POST <br>
Authorisation: NA <br>
Description: A user can login using their existing email and password. If a match is found in the database, the user is provided with a JWT token to perform queries that is valid for 24hrs. <br>
Payload & Response: <br>
<img src="DOCS/insomnia_login.png" alt="Insomnia Login" width="70%"/>

***Register*** <br>
URL Path: http://localhost:8080/auth/register <br>
Method: POST <br>
Authorisation: NA <br>
Description: A user can register to the app, creating their own account with data, including a password and email that is used to create a JWT token that provides them the authority to interact with the app. <br>
Payload & Response: <br>
<img src="DOCS/insomnia_register.png" alt="Insomnia Register" width="70%"/>

### Users

***Fetch Users*** <br>
URL Path: http://localhost:8080/user <br>
Method: GET <br>
Authorisation: JWT Token <br>
Description:  <br>
Payload & Response: <br>
<img src="DOCS/fetch_users.png" alt="Insomnia Register" width="70%"/>

***Fetch A Specific User*** <br>
URL Path: http://localhost:8080/user/1 <br>
Method: GET <br>
Authorisation: JWT Token <br>
Description:  <br>
Payload & Response: <br>
<img src="DOCS/fetch_a_user.png" alt="Insomnia Register" width="70%"/>
