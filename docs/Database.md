# Database

We use postgresql as our database, which is run through docker [[Docker]].

## Database Class

The Database class in src/utils is a wrapper around the psycopg2 library. It is used to connect to the database and execute queries. It also has a few helper functions to make it easier to work with the database. All methods are static and run directly on the class. This means they are called like `Database.execute()` not `Database().execute()` The main methods are as follows

### Database.connect()
Used only once at the start of the program to connect to the database.

### Database.init()
Used only once at the start of the program to initialize the database. This is further explained in the Initialisation section.

### Database.execute(query, *vars)
Used to execute a query on the database. The query is passed as a string and any arguments are passed after. The method returns a cursor object which can be used to fetch results etc.

```python
Database.execute("SELECT * FROM users WHERE first_name = %s AND last_name = %s", "Joe", "Mama")
```

### Database.execute_and_commit(query, *vars)
Used to execute a query on the database. The query is passed as a string and any arguments are passed after. The method returns nothing. This method also commits the changes to the database. This is used for queries that change the database.

### Database.execute_and_fetchone(query, *vars)
Used to execute a query on the database. The query is passed as a string and any arguments are passed after. The method returns the first row of the result. This is used for queries that fetch from the database.

### Database.execute_and_fetchall(query, *vars)
Used to execute a query on the database. The query is passed as a string and any arguments are passed after. The method returns all rows of the result. This is used for queries that fetch from the database.

### Database.cursor()
Returns a cursor object.

### Database.commit()
Commits changes to the database.

### Database.close()
Closes the connection to the database should be run at the end of the program.


## Initialisation
During the call to `Database.init()` all files in `src/init_sql` are run. Any sql to create tables or perform other initialisation steps e.g. creating an admin user should go there. 

## PGAdmin
PGAdmin is a web interface for postgresql. It is similar to MySQL Workbench if slightly more confusing. It is run with the test-watch script and can be accessed at `localhost:5050`. The email is `admin@admin.com` and the password `root`. 

### Adding the database to PGAdmin
1. Open PGAdmin
2. Right click on Servers and select Register > Server
3. Set name as desired
4. Under connection tab
   1. Set host name/address to `db`
   2. Set username to `postgres`
   3. Set password to `postgres`


### Viewing tables
1. Under databases
2. Expand `horizon`
3. Schemas > public > Tables



## Creating Tables
To create a table add the corresponding sql to `src/init_sql/<table_name>.sql`. If you need help converting your ERD to sql ask me.
