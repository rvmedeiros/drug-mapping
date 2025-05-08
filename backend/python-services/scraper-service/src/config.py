import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DAILYMED_BASE_URL = "https://dailymed.nlm.nih.gov/dailymed"