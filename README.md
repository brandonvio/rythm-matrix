## [rythm.cc](http://app.rythm.cc)

Forex, Crypto and Stock application. Running on a Kubernetes cluster in Azure. API integrations with [Oanda](https://www.oanda.com/us-en/), [IEX Cloud](https://iexcloud.io/) and [TradingView](https://www.tradingview.com/).

## Architecture

### Static Website

[rythm-app](https://github.com/brandonvio/rythm-app "rythm-app - Github"). ReactJS running in Docker on Kubernetes. Socket.io used for realtime stream price data. [TradingView](https://www.tradingview.com/HTML5-stock-forex-bitcoin-charting-library/?library=cloud-widget) charts.

### API

[rythm-api](https://github.com/brandonvio/rythm-app "rythm-api - Github"). NodeJS running in Docker on Kubernetes. Socket.io used for realtime stream price data. [Oanda API](https://developer.oanda.com/rest-live-v20/introduction/) integration. [IEX Cloud API](https://iexcloud.io/) integration.

### Microservices

[rythm-matrix](https://github.com/brandonvio/rythm-matrix "rythm-api - Github"). Python microservice used to listen to HTTP stream of pricing data from Oanda.

### Data

MongoDB running in VM on Azure. Pricing data stream via RabbitMQ. Data caching with Redis.

![Architecture](https://raw.githubusercontent.com/brandonvio/rythm-matrix/master/arch2.png)
