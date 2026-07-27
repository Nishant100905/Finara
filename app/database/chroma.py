"""
ChromaDB Configuration
"""

import chromadb
from chromadb.config import Settings

from app.config.settings import settings


class ChromaService:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH,
            settings=Settings(
                anonymized_telemetry=False
            ),
        )

    def get_collection(
        self,
        name: str = "documents",
    ):

        return self.client.get_or_create_collection(
            name=name,
        )


chroma = ChromaService()

collection = chroma.get_collection()