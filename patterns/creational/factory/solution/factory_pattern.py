"""
Factory Pattern Solution

The Factory Pattern solves:
1. Decouples object creation from usage
2. Centralizes complex creation logic
3. Makes it easy to add new types
4. Enables configuration-based object creation
5. Supports different creation strategies (dev/prod)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class DatabaseConnection(ABC):
    """Abstract base class for all database connections"""
    
    @abstractmethod
    def connect(self) -> str:
        pass
    
    @abstractmethod
    def execute_query(self, query: str) -> str:
        pass
    
    @abstractmethod
    def disconnect(self) -> str:
        pass


class MySQLConnection(DatabaseConnection):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection_string = self._build_connection_string()
    
    def _build_connection_string(self) -> str:
        cfg = self.config
        ssl_param = "?sslmode=require" if cfg.get('ssl_enabled', False) else ""
        return (
            f"mysql://{cfg['username']}:{cfg['password']}@"
            f"{cfg['host']}:{cfg['port']}{ssl_param}"
        )
    
    def connect(self) -> str:
        pool_size = self.config.get('pool_size', 5)
        ssl_enabled = self.config.get('ssl_enabled', False)
        return (
            f"MySQL: Connected to {self.config['host']}:{self.config['port']}\n"
            f"MySQL: Pool size: {pool_size}, SSL: {'enabled' if ssl_enabled else 'disabled'}"
        )
    
    def execute_query(self, query: str) -> str:
        return f"MySQL executed: {query}"
    
    def disconnect(self) -> str:
        return "MySQL connection closed"


class PostgreSQLConnection(DatabaseConnection):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection_string = self._build_connection_string()
    
    def _build_connection_string(self) -> str:
        cfg = self.config
        return (
            f"postgresql://{cfg['username']}:{cfg['password']}@"
            f"{cfg['host']}:{cfg['port']}/{cfg['database']}?"
            f"sslmode={cfg.get('ssl_mode', 'prefer')}"
        )
    
    def connect(self) -> str:
        return (
            f"PostgreSQL: Connected to database '{self.config['database']}' "
            f"at {self.config['host']}:{self.config['port']}"
        )
    
    def execute_query(self, query: str) -> str:
        return f"PostgreSQL executed: {query}"
    
    def disconnect(self) -> str:
        return "PostgreSQL connection closed"


class MongoDBConnection(DatabaseConnection):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection_string = self._build_connection_string()
    
    def _build_connection_string(self) -> str:
        cfg = self.config
        auth_source = cfg.get('auth_source', 'admin')
        replica_set = cfg.get('replica_set', '')
        replica_param = f"?replicaSet={replica_set}" if replica_set else ""
        
        return (
            f"mongodb://{cfg['username']}:{cfg['password']}@"
            f"{cfg['host']}:{cfg['port']}/{auth_source}{replica_param}"
        )
    
    def connect(self) -> str:
        replica_set = self.config.get('replica_set')
        msg = f"MongoDB: Connected to {self.config['host']}:{self.config['port']}"
        if replica_set:
            msg += f"\nMongoDB: Using replica set '{replica_set}'"
        return msg
    
    def execute_query(self, query: str) -> str:
        return f"MongoDB executed: {query}"
    
    def disconnect(self) -> str:
        return "MongoDB connection closed"


class RedisConnection(DatabaseConnection):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection_string = self._build_connection_string()
    
    def _build_connection_string(self) -> str:
        cfg = self.config
        pwd = cfg.get('password')
        pwd_param = f":{pwd}@" if pwd else ""
        return f"redis://{pwd_param}{cfg['host']}:{cfg['port']}/{cfg.get('db', 0)}"
    
    def connect(self) -> str:
        return f"Redis: Connected to {self.config['host']}:{self.config['port']}"
    
    def execute_query(self, query: str) -> str:
        return f"Redis executed: {query}"
    
    def disconnect(self) -> str:
        return "Redis connection closed"


class DatabaseFactory:
    """Factory class for creating database connections"""
    
    _connection_classes = {
        'mysql': MySQLConnection,
        'postgresql': PostgreSQLConnection,
        'mongodb': MongoDBConnection,
        'redis': RedisConnection
    }
    
    @classmethod
    def register_connection_class(cls, db_type: str, connection_class: type):
        """Register a new database connection type"""
        cls._connection_classes[db_type] = connection_class
    
    @classmethod
    def create_connection(cls, db_type: str, config: Dict[str, Any]) -> DatabaseConnection:
        """Create a database connection based on type and configuration"""
        if db_type not in cls._connection_classes:
            raise ValueError(
                f"Unknown database type: {db_type}. "
                f"Available types: {list(cls._connection_classes.keys())}"
            )
        
        connection_class = cls._connection_classes[db_type]
        return connection_class(config)


class ConfigurationManager:
    """Manages database configurations for different environments"""
    
    _configurations = {
        'development': {
            'mysql': {
                'host': 'localhost',
                'port': 3306,
                'username': 'dev_user',
                'password': 'dev_pass',
                'ssl_enabled': False,
                'pool_size': 2
            },
            'postgresql': {
                'host': 'localhost',
                'port': 5432,
                'username': 'dev_user',
                'password': 'dev_pass',
                'database': 'dev_db',
                'ssl_mode': 'disable',
                'pool_size': 5
            },
            'mongodb': {
                'host': 'localhost',
                'port': 27017,
                'username': 'dev_user',
                'password': 'dev_pass',
                'auth_source': 'admin',
                'read_preference': 'primary'
            },
            'redis': {
                'host': 'localhost',
                'port': 6379,
                'db': 0
            }
        },
        'production': {
            'mysql': {
                'host': 'prod-mysql.company.com',
                'port': 3306,
                'username': 'prod_user',
                'password': 'strong_prod_password_123!',
                'ssl_enabled': True,
                'pool_size': 20
            },
            'postgresql': {
                'host': 'prod-postgres.company.com',
                'port': 5432,
                'username': 'prod_user',
                'password': 'strong_prod_password_456!',
                'database': 'prod_db',
                'ssl_mode': 'require',
                'pool_size': 25
            },
            'mongodb': {
                'host': 'prod-mongo.company.com',
                'port': 27017,
                'username': 'prod_user',
                'password': 'strong_prod_password_789!',
                'auth_source': 'admin',
                'replica_set': 'prod-replica-set',
                'read_preference': 'secondaryPreferred'
            },
            'redis': {
                'host': 'prod-redis.company.com',
                'port': 6379,
                'password': 'redis_prod_password',
                'db': 0
            }
        }
    }
    
    @classmethod
    def get_config(cls, environment: str, db_type: str) -> Dict[str, Any]:
        """Get configuration for specific environment and database type"""
        if environment not in cls._configurations:
            raise ValueError(f"Unknown environment: {environment}")
        
        if db_type not in cls._configurations[environment]:
            raise ValueError(
                f"No configuration for {db_type} in {environment} environment"
            )
        
        return cls._configurations[environment][db_type]


class DatabaseConnectionManager:
    """High-level manager that combines factory and configuration"""
    
    def __init__(self, environment: str):
        self.environment = environment
        self._connections: Dict[str, DatabaseConnection] = {}
    
    def get_connection(self, db_type: str) -> DatabaseConnection:
        """Get or create a database connection"""
        if db_type not in self._connections:
            config = ConfigurationManager.get_config(self.environment, db_type)
            self._connections[db_type] = DatabaseFactory.create_connection(
                db_type, config
            )
        return self._connections[db_type]
    
    def close_all_connections(self):
        """Close all open connections"""
        for db_type, connection in self._connections.items():
            print(f"Closing {db_type}: {connection.disconnect()}")
        self._connections.clear()


def demonstrate_factory_pattern():
    """Demonstrate the Factory Pattern in action"""
    
    print("=== Factory Pattern Demonstration ===\n")
    
    # Development environment
    dev_manager = DatabaseConnectionManager('development')
    
    mysql_conn = dev_manager.get_connection('mysql')
    print(mysql_conn.connect())
    print(mysql_conn.execute_query("SELECT * FROM users"))
    print()
    
    mongo_conn = dev_manager.get_connection('mongodb')
    print(mongo_conn.connect())
    print(mongo_conn.execute_query("db.users.find({}"))
    print()
    
    # Production environment
    prod_manager = DatabaseConnectionManager('production')
    
    postgres_conn = prod_manager.get_connection('postgresql')
    print(postgres_conn.connect())
    print(postgres_conn.execute_query("SELECT * FROM products"))
    print()
    
    # Clean up
    print("\n=== Cleanup ===")
    dev_manager.close_all_connections()
    prod_manager.close_all_connections()


def demonstrate_extensibility():
    """Demonstrate how easy it is to add new database types"""
    
    print("\n=== Demonstrating Extensibility ===\n")
    
    # Define a new database type
    class CassandraConnection(DatabaseConnection):
        def __init__(self, config: Dict[str, Any]):
            self.config = config
        
        def connect(self) -> str:
            return f"Cassandra: Connected to cluster at {self.config['host']}"
        
        def execute_query(self, query: str) -> str:
            return f"Cassandra executed CQL: {query}"
        
        def disconnect(self) -> str:
            return "Cassandra connection closed"
    
    # Register the new type
    DatabaseFactory.register_connection_class('cassandra', CassandraConnection)
    
    # Use it immediately
    cassandra_config = {
        'host': 'cassandra.company.com',
        'port': 9042,
        'keyspace': 'my_keyspace'
    }
    
    cassandra_conn = DatabaseFactory.create_connection('cassandra', cassandra_config)
    print(cassandra_conn.connect())
    print(cassandra_conn.execute_query("SELECT * FROM users"))
    print(cassandra_conn.disconnect())


if __name__ == "__main__":
    demonstrate_factory_pattern()
    demonstrate_extensibility()