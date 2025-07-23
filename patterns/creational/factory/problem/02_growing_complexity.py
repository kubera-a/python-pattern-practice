"""
Factory Pattern - Problem Progression 2: Growing Complexity

THE ESCALATING PROBLEM:
As your application grows, object creation becomes a NIGHTMARE. This example shows
how quickly things spiral out of control when you don't use the Factory Pattern.

Watch how each new requirement makes the code exponentially worse...
"""

# REQUIREMENT 1: "We need to support 4 database types"
# Each one has DIFFERENT constructor parameters!

class MySQLConnection:
    def __init__(self, host, port, username, password, ssl_enabled=False, 
                 connection_timeout=30, charset="utf8mb4", pool_size=5):
        # Look at all these parameters! 8 different settings!
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssl_enabled = ssl_enabled
        self.connection_timeout = connection_timeout
        self.charset = charset
        self.pool_size = pool_size
        
        ssl_param = "?sslmode=require" if ssl_enabled else ""
        self.connection_string = (
            f"mysql://{username}:{password}@{host}:{port}"
            f"{ssl_param}&charset={charset}&timeout={connection_timeout}"
        )
    
    def connect(self):
        print(f"MySQL: Establishing connection pool of size {self.pool_size}")
        print(f"MySQL: SSL {'enabled' if self.ssl_enabled else 'disabled'}")
        return "MySQL connection established"
    
    def execute_query(self, query):
        return f"Executing MySQL query: {query}"


class PostgreSQLConnection:
    def __init__(self, host, port, username, password, database, 
                 ssl_mode="prefer", connection_timeout=30, 
                 application_name="", pool_size=10, max_overflow=20):
        # PostgreSQL has DIFFERENT parameters! 10 of them!
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database  # MySQL doesn't have this!
        self.ssl_mode = ssl_mode  # Different from MySQL's ssl_enabled!
        self.connection_timeout = connection_timeout
        self.application_name = application_name  # Unique to PostgreSQL!
        self.pool_size = pool_size
        self.max_overflow = max_overflow  # MySQL doesn't have this!
        
        app_param = f"&application_name={application_name}" if application_name else ""
        self.connection_string = (
            f"postgresql://{username}:{password}@{host}:{port}/{database}"
            f"?sslmode={ssl_mode}&connect_timeout={connection_timeout}{app_param}"
        )
    
    def connect(self):
        print(f"PostgreSQL: Connecting to database '{self.database}'")
        print(f"PostgreSQL: Pool size: {self.pool_size}, max overflow: {self.max_overflow}")
        return "PostgreSQL connection established"
    
    def execute_query(self, query):
        return f"Executing PostgreSQL query: {query}"


class MongoDBConnection:
    def __init__(self, host, port, username, password, auth_source="admin",
                 replica_set=None, read_preference="primary", 
                 write_concern=1, connection_timeout=30000):
        # MongoDB has COMPLETELY DIFFERENT parameters! NoSQL is different!
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.auth_source = auth_source  # MongoDB specific!
        self.replica_set = replica_set  # MongoDB specific!
        self.read_preference = read_preference  # MongoDB specific!
        self.write_concern = write_concern  # MongoDB specific!
        self.connection_timeout = connection_timeout  # In milliseconds, not seconds!
        
        replica_param = f"?replicaSet={replica_set}" if replica_set else ""
        self.connection_string = (
            f"mongodb://{username}:{password}@{host}:{port}/{auth_source}"
            f"{replica_param}&readPreference={read_preference}"
        )
    
    def connect(self):
        print(f"MongoDB: Connecting with read preference '{self.read_preference}'")
        if self.replica_set:
            print(f"MongoDB: Using replica set '{self.replica_set}'")
        return "MongoDB connection established"
    
    def execute_query(self, query):
        return f"Executing MongoDB query: {query}"


class RedisConnection:
    def __init__(self, host, port, password=None, db=0, 
                 decode_responses=True, connection_pool_kwargs=None):
        # Redis is even MORE different! It's a key-value store!
        self.host = host
        self.port = port
        self.password = password  # Optional, unlike others!
        self.db = db  # Redis uses numeric databases!
        self.decode_responses = decode_responses  # Redis specific!
        self.connection_pool_kwargs = connection_pool_kwargs or {}
        
        pwd_param = f":{password}@" if password else ""
        self.connection_string = f"redis://{pwd_param}{host}:{port}/{db}"
    
    def connect(self):
        print(f"Redis: Connecting to database {self.db}")
        return "Redis connection established"
    
    def execute_query(self, query):
        return f"Executing Redis command: {query}"


# REQUIREMENT 2: "We need different configurations for dev/staging/production"
# Now we have to create DIFFERENT functions for EACH environment!

def create_development_database(db_type):
    """Create database connection for development environment
    
    PROBLEM: Look at this massive if-elif chain! It knows:
    - Every database class
    - Every parameter for each class
    - The specific values for development
    """
    if db_type == "mysql":
        return MySQLConnection(
            host="localhost",
            port=3306,
            username="dev_user",
            password="dev_pass",
            ssl_enabled=False,  # Dev doesn't need SSL
            connection_timeout=10,  # Short timeout for dev
            charset="utf8mb4",
            pool_size=2  # Small pool for dev
        )
    elif db_type == "postgresql":
        return PostgreSQLConnection(
            host="localhost",
            port=5432,
            username="dev_user",
            password="dev_pass",
            database="dev_db",  # PostgreSQL needs database name!
            ssl_mode="disable",  # Different SSL handling than MySQL!
            connection_timeout=10,
            application_name="dev_app",
            pool_size=5,
            max_overflow=10
        )
    elif db_type == "mongodb":
        return MongoDBConnection(
            host="localhost",
            port=27017,
            username="dev_user",
            password="dev_pass",
            auth_source="admin",
            replica_set=None,  # No replica set in dev
            read_preference="primary",
            write_concern=1,  # Low write concern for dev
            connection_timeout=10000  # Note: milliseconds!
        )
    elif db_type == "redis":
        return RedisConnection(
            host="localhost",
            port=6379,
            password=None,  # No password in dev
            db=0,
            decode_responses=True,
            connection_pool_kwargs={"max_connections": 10}
        )
    else:
        raise ValueError(f"Unknown database type: {db_type}")


def create_production_database(db_type):
    """Create database connection for production environment
    
    PROBLEM: This is ALMOST IDENTICAL to the dev function, but with different values!
    Massive code duplication!
    """
    if db_type == "mysql":
        return MySQLConnection(
            host="prod-mysql.company.com",  # Different host
            port=3306,
            username="prod_user",  # Different credentials
            password="strong_prod_password_123!",
            ssl_enabled=True,  # Production NEEDS SSL!
            connection_timeout=30,  # Longer timeout
            charset="utf8mb4",
            pool_size=20  # Bigger pool for production
        )
    elif db_type == "postgresql":
        return PostgreSQLConnection(
            host="prod-postgres.company.com",
            port=5432,
            username="prod_user",
            password="strong_prod_password_456!",
            database="prod_db",
            ssl_mode="require",  # SSL required in production!
            connection_timeout=30,
            application_name="prod_app",
            pool_size=25,  # Much bigger pool
            max_overflow=50  # Higher overflow limit
        )
    elif db_type == "mongodb":
        return MongoDBConnection(
            # Production MongoDB uses multiple hosts for replica set!
            host="prod-mongo-1.company.com,prod-mongo-2.company.com,prod-mongo-3.company.com",
            port=27017,
            username="prod_user",
            password="strong_prod_password_789!",
            auth_source="admin",
            replica_set="prod-replica-set",  # Production uses replica sets!
            read_preference="secondaryPreferred",  # Different read strategy!
            write_concern=3,  # Higher write concern for data safety!
            connection_timeout=30000
        )
    elif db_type == "redis":
        return RedisConnection(
            host="prod-redis.company.com",
            port=6379,
            password="redis_prod_password",  # Production has password!
            db=0,
            decode_responses=True,
            connection_pool_kwargs={"max_connections": 100}  # 10x more connections!
        )
    else:
        raise ValueError(f"Unknown database type: {db_type}")


# REQUIREMENT 3: "We also need staging environment"
# Oh no! Do we create ANOTHER function with the SAME if-elif structure?
# def create_staging_database(db_type): ...

# REQUIREMENT 4: "We need to support region-specific databases"
# def create_us_east_database(db_type): ...
# def create_eu_west_database(db_type): ...
# def create_asia_pacific_database(db_type): ...

# REQUIREMENT 5: "We need test configurations for unit tests"
# def create_test_database(db_type): ...


def main():
    print("=== The Growing Complexity Problem ===\n")
    
    # Now our main code has NESTED if-elif chains!
    environment = "development"
    db_type = "mysql"
    
    print("PROBLEM 1: Nested decision logic!")
    print(f"Creating {db_type} for {environment}...\n")
    
    # First if-elif: Choose environment
    if environment == "development":
        connection = create_development_database(db_type)
    elif environment == "production":
        connection = create_production_database(db_type)
    # What about staging? testing? regional deployments?
    else:
        raise ValueError(f"Unknown environment: {environment}")
    
    print(connection.connect())
    print(connection.execute_query("SELECT * FROM users"))
    
    # Let's try production MongoDB
    environment = "production"
    db_type = "mongodb"
    
    print(f"\nCreating {db_type} for {environment}...\n")
    
    # THE SAME nested if-elif logic repeated!
    if environment == "development":
        connection = create_development_database(db_type)
    elif environment == "production":
        connection = create_production_database(db_type)
    else:
        raise ValueError(f"Unknown environment: {environment}")
    
    print(connection.connect())
    print(connection.execute_query("db.users.find({})")
    
    print("\n" + "="*60)
    print("PROBLEM SUMMARY:")
    print("1. CONSTRUCTOR CHAOS - Each database has different parameters")
    print("2. ENVIRONMENT EXPLOSION - Each environment needs its own function")
    print("3. DUPLICATION DISASTER - Same if-elif logic EVERYWHERE")
    print("4. PARAMETER PROLIFERATION - Client code knows EVERYTHING")
    print("5. MAINTENANCE MAYHEM - Adding features requires changing MANY places")
    
    print("\n" + "="*60)
    print("IMAGINE THESE SCENARIOS:")
    print("- 'Add support for CassandraDB' - Update EVERY environment function!")
    print("- 'Add staging environment' - Create new function with ALL databases!")
    print("- 'Add regional databases' - Multiply everything by number of regions!")
    print("- 'Change MySQL connection pooling' - Find and update EVERYWHERE!")
    print("- 'Add connection retry logic' - Good luck adding that everywhere!")
    
    print("\n" + "="*60)
    print("THE CORE PROBLEMS:")
    print("1. No separation of concerns - Creation mixed with configuration")
    print("2. No single source of truth - Configuration scattered everywhere")
    print("3. No abstraction - Client knows all implementation details")
    print("4. No flexibility - Hard-coded everything")
    print("5. No testability - Can't mock or substitute easily")
    
    print("\nThe Factory Pattern would:")
    print("- Centralize all creation logic in one place")
    print("- Hide constructor complexity from clients")
    print("- Make adding new types trivial")
    print("- Separate configuration from creation")
    print("- Enable easy testing with mock factories")


if __name__ == "__main__":
    main()