from src.infrastructure.database.mongo_database import Database

db_instance = Database().db

def main():
    service = MyService(db_instance)
    service.run()

if __name__ == "__main__":
    main()
