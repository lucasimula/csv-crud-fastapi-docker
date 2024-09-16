from fastapi import FastAPI
import csv
from dataclasses import dataclass

app = FastAPI()

@dataclass
class Record():
  id: int
  nome: str
  cognome: str
  codice_fiscale: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

# create new record
@app.post("/items/", response_model=Record)
async def create_record(item: Record):
    item_write = [item.id, item.nome, item.cognome, item.codice_fiscale]
    with open('records.csv', 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(item_write)

    return {"id": item.id, "nome": item.nome, "cognome": item.cognome, "codice_fiscale": item.codice_fiscale}

# get all records
@app.get("/items/", response_model=list[Record])
async def get_records():
    with open('records.csv', 'r', newline='') as csvfile:
      records = []
      reader = csv.reader(csvfile)
      for row in reader:
        records.append({"id": row[0], "nome": row[1], "cognome": row[2], "codice_fiscale": row[3]})

    return records

# count items
@app.get("/items/count")
async def get_number_of_records():
    row_count = 0
    with open('records.csv', 'r', newline='') as csvfile:
      reader = csv.reader(csvfile)
      row_count = sum(1 for row in reader)
    
    return {"count": row_count}

# get single record
@app.get("/items/{id}", response_model=Record)
async def get_single_record(id: int):
    record = {}
    with open('records.csv', 'r', newline='') as csvfile:
      reader = csv.reader(csvfile)
      for row in reader:
        if row[0] == str(id):
          record = {"id": row[0], "nome": row[1], "cognome": row[2], "codice_fiscale": row[3]}

    return record

# update record
@app.put("/items/{id}", response_model=Record)
async def update_record(id: int, item: Record):
    records = []
    with open('records.csv', 'r', newline='') as csvfile:
      reader = csv.reader(csvfile)
      for row in reader:
        records.append({"id": row[0], "nome": row[1], "cognome": row[2], "codice_fiscale": row[3]})
    
    edited_item = {}
    for i, record in enumerate(records):
      if record["id"] == str(id):
         records[i] = {"id": item.id, "nome": item.nome, "cognome": item.cognome, "codice_fiscale": item.codice_fiscale}
         edited_item = records[i]
    
    with open('records.csv', 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      for record in records:
        writer.writerow([record['id'], record['nome'], record['cognome'], record['codice_fiscale']])
    
    return edited_item

# delete record
@app.delete("/items/{id}")
async def delete_item(id: int):
    records = []
    with open('records.csv', 'r', newline='') as csvfile:
      reader = csv.reader(csvfile)
      for row in reader:
        records.append({"id": row[0], "nome": row[1], "cognome": row[2], "codice_fiscale": row[3]})
    
    for i, record in enumerate(records):
      if record["id"] == str(id):
         records.remove(records[i])
    
    with open('records.csv', 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      for record in records:
        writer.writerow([record['id'], record['nome'], record['cognome'], record['codice_fiscale']])
    
    return {"message": "Item deleted successfully"}
