A project for streaming stock tickers from finnhub.
A producer grabs the data from the API, sends via a topic tickers data to a consumer.
The consumer pushes the processed tickers data to Google BigQuery and in turn creating a report using Google data studio.
