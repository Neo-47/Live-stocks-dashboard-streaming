
from settings import *

# Producing as JSON
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
value_serializer=lambda m: json.dumps(m).encode('ascii'))



def on_message(ws, message):
    
    
    payload = json.loads(message)
    df = pd.DataFrame(payload['data'])
    print(df)
    producer.send('test-topic', payload['data'])
    print("payload sent to consumer")

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"AAL"}')
    ws.send('{"type":"subscribe","symbol":"ACHL"}')
    ws.send('{"type":"subscribe","symbol":"ATO"}')
    ws.send('{"type":"subscribe","symbol":"ATOS"}')
    ws.send('{"type":"subscribe","symbol":"ATOM"}')


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=cmtbkl9r01qqtangmqrgcmtbkl9r01qqtangmqs0",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()