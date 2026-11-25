from src.database import Base, engine
from src.research_models import FacilityResearch

Base.metadata.create_all(bind=engine)

print("Facility research table is ready.")