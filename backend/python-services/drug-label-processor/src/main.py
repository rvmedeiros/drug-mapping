from application.services.mapper_service import MapperService
from infrastructure.database.mongo_database import DatabaseConnections
from infrastructure.repositories.mongo_drug_label_repository import MongoDrugRepository
from application.services.ai_agent_service import Phi2IndicationMapper


def main():
    db_conn = DatabaseConnections()
    repository = MongoDrugRepository(db_conn.mongo_db)
    phi2IndicationMapper = Phi2IndicationMapper()
    service = MapperService(repository, phi2IndicationMapper, interval_seconds=10)

    try:
        service.run()
    except KeyboardInterrupt:
        print("Shutting down gracefully...")

if __name__ == "__main__":
    main()
