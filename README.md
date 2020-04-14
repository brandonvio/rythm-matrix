## rythm.cc

Forex, Crypto and Stock application. Running on a Kubernetes cluster in Azure. API integrations with Oanda and IEX Cloud.

[rythm.cc](https://app.rythm.cc)

## Architecture

### Static Website

ReactJS running in Docker on Kubernetes

### API

NodeJS running in Docker on Kubernetes

### Data

MongoDB running in VM on Azure. Pricing data stream via RabbitMQ. Data caching with Redis.

![Architecture](https://raw.githubusercontent.com/brandonvio/rythm-matrix/master/arch2.png)
