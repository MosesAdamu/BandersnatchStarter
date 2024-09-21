from os import getenv
from dotenv import load_dotenv
from certifi import where
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient


class Database:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.client = MongoClient(getenv("DB_URL"), tlsCAFile=where())
        self.db = self.client["MonsterDB"]  # Change "MonsterDB" to your database name
        self.collection = self.db["monsters"]  # "monsters" collection

    # Seed the database with a specified number of monsters
    def seed(self, amount: int):
        monsters = []
        for _ in range(amount):
            monster = Monster().to_dict()  # Generate monster data using MonsterLab
            monsters.append(monster)
        self.collection.insert_many(monsters)  # Bulk insert monsters into the database

    # Reset the database by deleting all documents in the collection
    def reset(self):
        confirm = input("Are you sure you want to reset the database? Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            self.collection.delete_many({})
            print("Database reset successfully.")
        else:
            print("Database reset canceled.")

    # Count the number of documents (monsters) in the collection
    def count(self) -> int:
        monster_count = self.collection.count_documents({})
        return monster_count

    # Return the documents (monsters) as a Pandas DataFrame
    def dataframe(self) -> DataFrame:
        monsters = list(self.collection.find({}))
        df = DataFrame(monsters)  # Convert the list of monsters to a DataFrame
        return df

    # Return the documents (monsters) as an HTML table
    def html_table(self) -> str:
        df = self.dataframe()
        if df.empty:
            return None  # Return None if there are no monsters in the collection
        return df.to_html()  # Convert the DataFrame to an HTML table


if __name__ == "__main__":
    db = Database()

    # Seed the database with 1000 monsters
    db.seed(1000)

    db.reset()
