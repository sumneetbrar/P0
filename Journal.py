import csv
import json
from datetime import datetime

class JournalEntry:
    def __init__(self, entry_id, date, title, content, tags=None):
        self.id = entry_id
        self.date = date
        self.title = title
        self.content = content
        self.tags = tags if tags else []

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "title": self.title,
            "content": self.content,
            "tags": ",".join(self.tags)
        }

    @staticmethod
    def from_dict(data):
        return JournalEntry(
            entry_id=data["id"],
            date=data["date"],
            title=data["title"],
            content=data["content"],
            tags=data["tags"].split(",") if data["tags"] else []
        )

class JournalManager:
    def __init__(self):
        self.entries = []
        self.file_path = "journal_entries.json"

    def add_entry(self, title, content, tags=None):
        entry_id = len(self.entries) + 1
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = JournalEntry(entry_id, date, title, content, tags)
        self.entries.append(entry)

    def view_entries(self):
        return [entry.to_dict() for entry in self.entries]

    def view_titles(self):
        return [(entry.id, entry.title) for entry in self.entries]

    def open_entry(self, entry_id):
        for entry in self.entries:
            if entry.id == entry_id:
                return entry.to_dict()
        return None

    def delete_entry(self, entry_id):
        self.entries = [entry for entry in self.entries if entry.id != entry_id]

    def merge_entries(self, entry_ids, new_title, new_content, new_tags=None):
        self.entries = [entry for entry in self.entries if entry.id not in entry_ids]
        self.add_entry(new_title, new_content, new_tags)

    def export_entries(self, file_name="exported_entries.txt"):
        with open(file_name, "w") as file:
            for entry in self.entries:
                file.write(f"ID: {entry.id}\nDate: {entry.date}\nTitle: {entry.title}\nContent: {entry.content}\nTags: {', '.join(entry.tags)}\n\n")

    def analytics(self):
        return {
            "total_entries": len(self.entries),
            "unique_tags": len(set(tag for entry in self.entries for tag in entry.tags))
        }

    def save_to_file(self):
        with open(self.file_path, "w") as file:
            json.dump([entry.to_dict() for entry in self.entries], file)

    def load_from_file(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                self.entries = [JournalEntry.from_dict(entry) for entry in data]
        except FileNotFoundError:
            self.entries = []

if __name__ == "__main__":
    jm = JournalManager()
    jm.load_from_file()

    while True:
        print("\nJournal CLI Application")
        print("1. Create a new entry")
        print("2. View stats")
        print("3. View titles of all old entries")
        print("4. Open an old entry")
        print("5. Delete an entry")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter the title of your entry: ")
            content = input("Write your entry: ")
            tags = input("Enter tags (comma-separated): ").split(",")
            jm.add_entry(title, content, tags)
            jm.save_to_file()
            print("Entry added successfully.")
        elif choice == "2":
            stats = jm.analytics()
            print("Stats:", stats)
        elif choice == "3":
            titles = jm.view_titles()
            for entry_id, title in titles:
                print(f"ID: {entry_id}, Title: {title}")
        elif choice == "4":
            entry_id = int(input("Enter the entry ID to open: "))
            entry = jm.open_entry(entry_id)
            if entry:
                print("\nEntry Details:")
                print(f"ID: {entry['id']}\nDate: {entry['date']}\nTitle: {entry['title']}\nContent: {entry['content']}\nTags: {entry['tags']}")
            else:
                print("Entry not found.")
        elif choice == "5":
            entry_id = int(input("Enter the entry ID to delete: "))
            jm.delete_entry(entry_id)
            jm.save_to_file()
            print("Entry deleted successfully.")
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")