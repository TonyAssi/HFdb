# HFdb

HFdb is a lightweight Python module that turns a [Hugging Face Hub](https://huggingface.co/) dataset repo into a simple, private CSV-based database. It supports basic CRUD operations and works well for small, structured data where you want versioned cloud persistence.

---

## 📦 Features

- ✅ Create and manage private datasets on Hugging Face Hub
- ✅ Add, update, delete, and query rows
- ✅ Auto-syncs CSV file to the repo
- ✅ Simple Pandas-powered interface

---

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## ✨ Example Usage

```python
import HFdb

# Create a new private database
my_db = HFdb.create("username/db_name", ["key", "email", "credits"], "hf_your_token")

# Load existing database
my_db = HFdb.db("username/db_name", "hf_your_token")

# Add a row
my_db.add_row({"key": 123, "email": "tony@gmail.com", "credits": 5})

# Get row by column match
row = my_db.get_row("key", 123)

# Get entire dataset as DataFrame
df = my_db.get_df()

# Delete a row
my_db.delete_row("key", 123)

# Replace one value in a row
my_db.replace_element("key", 123, "credits", 0)

# Replace an entire row
my_db.replace_row("key", 123, {"key": 123, "email": "new@email.com", "credits": 0})

# Check if a row exists
exists = my_db.row_exists("key", 123)

# Get all column names
columns = my_db.get_columns()

```
