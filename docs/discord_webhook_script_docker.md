# Discord Webhook Script Docker

## Dependencies

Python 3: [Download link](https://www.python.org/downloads/)

Python `requests` module: To install, enter the following command in cmd or a terminal:

```
pip install requests
```

## Usage

1. Create a file named `list.txt` in the same directory as `check_shopify_stock_webhook.py`. The file should contain a newline separated list of urls for items to check stock of. 

    For example: 
    ```
    https://examplestore.com/products/exampleproduct
    https://examplestore.com/products/exampleproduct2?variant=39615971195628
    https://examplestore.com/collections/examplecollection/products/exampleproduct3
    ```

    To check only specific variants of a product, be sure to use a url with the correct `?variant={variantid}` suffix. 
    
    To check all variants of a product, remove the `?variant={variantid}` suffix from the url if it appears.

2. Open `Dockerfile` and add your discord webhook url for `WEBHOOK_URL=`.

3. Edit `WEBHOOK_CONTENT=` to configure the message content you want to send when a product goes from out of stock to in stock.

    `{Name}` sends the item's name.

    `{Title}` sends the item's title.

    `{SKU}` sends the item's sku.

    `{Public Title}` sends the item's public title.

    `{Option1}` sends the item's option1.

    `{Option2}` sends the item's option2.

    `{Option3}` sends the item's option3.

    `{Link}` sends a link to the item's store page.

4. Optionally, edit the delays in `Dockerfile` to change the delay in seconds between checking stock, looping batch, and request fail.

    `STOCK_DELAY` adds a delay after sending the stock check request.

    `BATCH_DELAY` adds a delay between checking the full list of products. Only used between the last item in the list and the first item in the list when looping back to the first item.

    `REQUEST_FAIL_DELAY` adds a delay after a request fails before resuming the sending of requests.

5. Run `sudo docker-compose up -d`

## Troubleshooting

To reset stock states and tracking, delete `stock_state.json`. This will remove the current stock data collected by the script. Upon running the script again it will rerecord the stock states. This will cause the script to resend webhook messages for items that had previously been recorded as in stock and have not had a change in state.