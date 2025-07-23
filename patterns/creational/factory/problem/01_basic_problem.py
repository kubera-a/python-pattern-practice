"""
Factory Pattern - Problem Progression 1: Basic Object Creation

THE PROBLEM:
When you create objects directly in your code (using 'new' or direct class instantiation),
you create "tight coupling" between your code and the specific classes. This means:

1. Your code MUST know about every single class it might need to create
2. Adding new types requires changing existing code (violates Open/Closed Principle)
3. The same creation logic gets duplicated everywhere you need these objects
4. Testing becomes harder because you can't easily substitute mock objects

Let's see this problem in action with a database connection system...
"""

class MySQLConnection:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection_string = f"mysql://{username}:{password}@{host}:{port}"
    
    def connect(self):
        print(f"Connecting to MySQL database at {self.host}:{self.port}")
        return "MySQL connection established"
    
    def execute_query(self, query):
        return f"Executing MySQL query: {query}"


class PostgreSQLConnection:
    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    
    def connect(self):
        print(f"Connecting to PostgreSQL database '{self.database}' at {self.host}:{self.port}")
        return "PostgreSQL connection established"
    
    def execute_query(self, query):
        return f"Executing PostgreSQL query: {query}"


class MongoDBConnection:
    def __init__(self, host, port, username, password, auth_source="admin"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.auth_source = auth_source
        self.connection_string = f"mongodb://{username}:{password}@{host}:{port}/{auth_source}"
    
    def connect(self):
        print(f"Connecting to MongoDB at {self.host}:{self.port}")
        return "MongoDB connection established"
    
    def execute_query(self, query):
        return f"Executing MongoDB query: {query}"


def main():
    print("=== The Direct Instantiation Problem ===\n")
    
    # PROBLEM 1: The client code must know about ALL database classes
    print("PROBLEM 1: Look at all the imports we need!")
    print("We imported MySQLConnection, PostgreSQLConnection, MongoDBConnection")
    print("What if we add 10 more database types? 10 more imports!\n")
    
    # PROBLEM 2: Creation logic is mixed with business logic
    db_type = "mysql"
    print(f"PROBLEM 2: Creating a {db_type} connection...")
    
    # Look at this messy if-elif chain that will grow forever!
    if db_type == "mysql":
        connection = MySQLConnection("localhost", 3306, "root", "password")
    elif db_type == "postgresql":
        connection = PostgreSQLConnection("localhost", 5432, "postgres", "password", "mydb")
    elif db_type == "mongodb":
        connection = MongoDBConnection("localhost", 27017, "admin", "password")
    else:
        raise ValueError(f"Unknown database type: {db_type}")
    
    print(connection.connect())
    print(connection.execute_query("SELECT * FROM users"))
    
    # PROBLEM 3: The SAME if-elif logic is duplicated everywhere!
    print("\nPROBLEM 3: Now we need another connection elsewhere in our code...")
    print("Watch us duplicate the EXACT SAME if-elif chain:\n")
    
    db_type = "postgresql"
    # This is the EXACT SAME code as above - pure duplication!
    if db_type == "mysql":
        connection = MySQLConnection("localhost", 3306, "root", "password")
    elif db_type == "postgresql":
        connection = PostgreSQLConnection("localhost", 5432, "postgres", "password", "mydb")
    elif db_type == "mongodb":
        connection = MongoDBConnection("localhost", 27017, "admin", "password")
    else:
        raise ValueError(f"Unknown database type: {db_type}")
    
    print(connection.connect())
    print(connection.execute_query("SELECT * FROM products"))
    
    # PROBLEM 4: Adding new database types requires modifying ALL these if-elif chains
    print("\n" + "="*60)
    print("IMAGINE: Your boss says 'We need to support Redis now!'")
    print("You must:")
    print("1. Import RedisConnection class")
    print("2. Find EVERY place in your code with these if-elif chains")
    print("3. Add 'elif db_type == \"redis\":' to EACH one")
    print("4. Hope you didn't miss any!")
    print("\nThis violates the Open/Closed Principle:")
    print("- Code should be OPEN for extension")
    print("- But CLOSED for modification")
    print("We're modifying existing code instead of extending it!")
    
    # PROBLEM 5: Each class has different constructor parameters
    print("\n" + "="*60)
    print("PROBLEM 5: Each database has DIFFERENT parameters:")
    print("- MySQL: host, port, username, password")
    print("- PostgreSQL: host, port, username, password, database")  
    print("- MongoDB: host, port, username, password, auth_source")
    print("The client code must know these details for EVERY database type!")
    
    # PROBLEM 6: Testing nightmare
    print("\n" + "="*60)
    print("PROBLEM 6: How do you test this code?")
    print("- You can't easily mock the database connections")
    print("- Your tests will actually try to connect to databases!")
    print("- You can't test the creation logic separately")
    
    print("\n" + "="*60)
    print("SUMMARY: Why is this bad?")
    print("1. TIGHT COUPLING - Your code is 'glued' to specific classes")
    print("2. DUPLICATION - Same if-elif logic everywhere")
    print("3. HARD TO EXTEND - Adding types means changing existing code")
    print("4. HARD TO TEST - Can't easily substitute test doubles")
    print("5. VIOLATES SINGLE RESPONSIBILITY - Mixing creation with usage")
    print("\nThe Factory Pattern solves ALL these problems!")

if __name__ == "__main__":
    main()