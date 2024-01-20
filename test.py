from elasticsearch import Elasticsearch
import requests

es = Elasticsearch(
    [{'host': 'localhost', 'port': 9200, 'scheme': 'https'}],
    basic_auth=('elastic', 'ZYG7ZJ9H_QlGlKiY=t1N'),
    verify_certs=False
)

# Check the connection
if es.ping():
    print("Connected to Elasticsearch")
    # Sample data to be indexed
    sample_data = {
        "title": "Sample Document",
        "content": "This is a sample document for Elasticsearch.",
    }
    
    # Index the document into Elasticsearch
    
    # Replace with your desired index name
    index_name = "test" 
    # Replace with a unique identifier for the document 
    document_id = "1" 

    es.index(index=index_name, id=document_id, body=sample_data)

    print(f"Document indexed with ID {document_id} in index {index_name}")
else:
    print("Unable to connect to Elasticsearch")

api_url ="https://api.patentsview.org/patents/query?q=%7b%22_gte%22:%7b%22patent_date%22:%222007-01-04%22%7d%7d&f=%5b%22patent_number%22,%22patent_date%22,%22patent_title%22%5d"
response = requests.get(api_url)

# Check if the request was successful 
if response.status_code == 200:
    patent_data = response.json()

    # Index patent data into Elasticsearch
    for patent in patent_data['patents']:
        es.index(index=index_name, body=patent)

    print("Patent data indexed successfully.")
else:
    print(f"Failed to fetch data from the API. Status code: {response.status_code}")
    print(response.text)