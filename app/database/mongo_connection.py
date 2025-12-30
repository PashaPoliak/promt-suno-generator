import importlib
from config.mongo_config import mongo_settings
from config.logging_config import get_logger

logger = get_logger(__name__)

class MongoDB:
    def __init__(self):
        self.client = None
        self.database = None
        self._connected = False

    def connect(self):
        if self._connected:
            return  # Already connected
        
        try:
            motor_module = importlib.import_module('motor.motor_asyncio')
            AsyncIOMotorClient = motor_module.AsyncIOMotorClient
        except ImportError:
            raise ImportError("motor package is required but not installed. Please install it with 'pip install motor'")
        
        try:
            self.client = AsyncIOMotorClient(mongo_settings.mongodb_url)
            if self.client:
                self.database = self.client[mongo_settings.mongodb_database]
                self._connected = True
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            raise

    def disconnect(self):
        if self.client:
            self.client.close()
            self._connected = False
            self.database = None
            self.client = None
            logger.info("Disconnected from MongoDB")

    def get_collection(self, collection_name: str):
        if not self.database:
            self.connect()
        if not self.database:
            raise Exception("Failed to connect to database")
        return self.database[collection_name]

    @property
    def clips_collection(self):
        if self.database is None:
            self.connect()
        if self.database is None:
            raise Exception("Failed to connect to database")
        return self.database[mongo_settings.mongodb_clips_collection]

    @property
    def playlists_collection(self):
        if self.database is None:
            self.connect()
        if self.database is None:
            raise Exception("Failed to connect to database")
        return self.database[mongo_settings.mongodb_playlists_collection]

    @property
    def profiles_collection(self):
        if self.database is None:
            self.connect()
        if self.database is None:
            raise Exception("Failed to connect to database")
        return self.database[mongo_settings.mongodb_profiles_collection]


# Create a global instance
mongodb = MongoDB()