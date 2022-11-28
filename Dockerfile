FROM python:3.9-alpine

ENV STOCK_DELAY=30
ENV BATCH_DELAY=10800
ENV REQUEST_FAIL_DELAY=120
ENV WEBHOOK_URL=test
ENV WEBHOOK_CONTENT="In Stock!\nName: {Name}, Title: {Title}, SKU: {SKU}\nLink: {Link}"

WORKDIR /usr/app

RUN pip install requests

COPY . .

CMD [ "python", "check_shopify_stock_webhook.py" ]