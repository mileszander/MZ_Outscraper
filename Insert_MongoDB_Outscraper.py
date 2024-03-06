from pymongo import MongoClient
import requests
import json


# Replace 'your_connection_string' with your actual MongoDB connection string
connection_string = 'mongodb+srv://mzander:America%231@cluster0.3dqr20v.mongodb.net/'


# Connect to your MongoDB database
client = MongoClient(connection_string)

# Specify the database to use
db = client['OutScraper']  # Replace 'your_database_name' with your database name

# Specify the collection to use
collection = db['Test_data']  # Replace 'your_collection_name' with your collection name


query = "Central Machine Works, Austin, Texas"




def pull_data_and_insert(query):
  payload = {}
  headers = {
  'Cookie': 'session=.eJxNyj0OwjAMQOG7eK4QPzHQTtwEOYlbRdgxJHhC3J0ywfre94Lk_WnK7cpKRWACLcL9EsXSTbkuzfy-SaYw_GjjpVj9Wir1fzycnWGqLjKA97WUvLKZ9yOmORIjhu3hSDmHfIpph-eINAZ4fwBVqS9C.Zei-0A.6h-b2qbwws_cUv1-nfNHTZgJEVo'
  }
  base_url = "https://api.app.outscraper.com/maps/search-v3"
  api_key = "ZmUyOTVjZmJhZTU1NDAzNmFkZDRkN2JjMTU4YjVhOTR8YzlkMWMyMWY3OA"
  # Ensure the query is properly URL-encoded to handle spaces and special characters
  from urllib.parse import quote
  encoded_query = quote(query)

  # Construct the URL with the encoded query
  url = f"{base_url}?query={encoded_query}&limit=1&async=false&apiKey={api_key}"
  response = requests.request("GET", url, headers=headers, data=payload)

  # Convert the string response to a Python dictionary
  response = json.loads(response.text)


  # Extract the data array
  data_array = response['data'][0]  # Assuming you always want the first list inside the 'data' key

  # Iterate through items in the data array if there are multiple items you want to insert
  for item in data_array:
      # Set the '_id' to the 'name' value from the item
      item['_id'] = item['name']
      
      # Remove the 'name' field if you don't want it duplicated as '_id'
      # Comment out the following line if you want to keep the 'name' field as well
      del item['name']
      
      try:
          # Insert the item into MongoDB
          insert_result = collection.insert_one(item)
          print(f"Document inserted with _id: {insert_result.inserted_id}")
      except Exception as e:
          print(f"An error occurred: {e}")



pull_data_and_insert(query)
