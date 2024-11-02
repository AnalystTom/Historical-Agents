import os
from typing import Dict, List
from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDBDataRetriever:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_URI"))
        self.db = self.client[os.getenv("MONGODB_DATABASE")]
        self.profiles_collection = self.db["profiles"]
        self.contexts_collection = self.db["contexts"]

    def get_profile(self, figure_id: str) -> Dict:
        # Implement the logic to retrieve a historical figure's profile from MongoDB
        pass

    def get_contexts(self, figure_id: str) -> List[Dict]:
        # Implement the logic to retrieve a historical figure's associated contexts from MongoDB
        pass
    

from .mongodb_data_retriever import MongoDBDataRetriever

class PromptBuilder:
    def __init__(self):
        self.mongodb_retriever = MongoDBDataRetriever()

    def build_prompt(self, figure_id: str, query: str) -> str:
        profile = self.mongodb_retriever.get_profile(figure_id)
        contexts = self.mongodb_retriever.get_contexts(figure_id)

        prompt = f"""
        Role: {profile['name']}
        Key traits: {', '.join(profile['characterTraits'])}
        Known associates: {', '.join([rel['name'] for rel in profile['relationships']])}

        Historical context:
        {'\n'.join([f'- {context["date"]}: {context["location"]} - {", ".join(context["keyEvents"])}' for context in contexts])}

        Query: {query}
        """
        return prompt