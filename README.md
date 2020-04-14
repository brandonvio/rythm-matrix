## rythm.cc

Forex, Crypto and Stock application. Running on a Kubernetes cluster in Azure. API integrations with Oanda and IEX Cloud.

[rythm.cc](http://app.rythm.cc)

## Architecture

### Static Website

[rythm-app](https://github.com/brandonvio/rythm-app "rythm-app - Github"). ReactJS running in Docker on Kubernetes.

### API

[rythm-api](https://github.com/brandonvio/rythm-app "rythm-api - Github"). NodeJS running in Docker on Kubernetes.

### Microservices

[rythm-matrix](https://github.com/brandonvio/rythm-matrix "rythm-api - Github"). Python microservice used to listen to HTTP stream of pricing data from Oanda.

### Data

MongoDB running in VM on Azure. Pricing data stream via RabbitMQ. Data caching with Redis.

![Architecture](https://raw.githubusercontent.com/brandonvio/rythm-matrix/master/arch2.png)
