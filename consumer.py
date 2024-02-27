
from settings import *


# Getting the data as JSON
consumer = KafkaConsumer('stocks-stream',
bootstrap_servers=['localhost:9092'],
value_deserializer=lambda m: json.loads(m.decode('ascii')))

def write_local(df: pd.DataFrame, dataset_name: str, dataset_file: str) -> Path:
    
    """Write DataFrame out locally as parquet file"""
    
    path = Path(f"data/{dataset_name}/{dataset_file}.csv")
    df.to_csv(path, compression="gzip")
    
    return path


def write_gcs(path: Path) -> None:
    """Upload local parquet file to gcs"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=path,to_path=path)
    return

def write_bq(df: pd.DataFrame) -> None:
    """Write data to BigQuery"""

    gcp_credentials_block = GcpCredentials.load("zoom-gcs-creds")
   
    df.to_gbq(destination_table="stocks_project.tickers",
              project_id="stately-planet-407118",
              chunksize=500_000,
              credentials=gcp_credentials_block.get_credentials_from_service_account(),
              if_exists='append')
    
    



stocks = pd.DataFrame()
dataset_name = DATASET_NAME
dataset_file = DATASET_FILE

i = 1

for message in consumer:
    print(message)
    df = pd.DataFrame(message.value)
    stocks = pd.concat([stocks, df])
    
    if(i % 20 == 0):
        
        print("Writing to the cloud")
        stocks['t'] = pd.to_datetime(stocks['t'], unit='ms')
        stocks = stocks.explode("c")

        path = write_local(stocks, dataset_name, dataset_file)
        write_gcs(path)
        write_bq(stocks)
        
        stocks = pd.DataFrame()
        
    i += 1
    print(df)
    







