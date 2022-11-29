# Discord Webhook Script Docker

## Dependencies

Docker: [Download link](https://www.docker.com/)

Docker Compose [Download link](https://docs.docker.com/compose/)

## Usage

1. Clone this repo 

   `git clone https://github.com/Kuuuube/Shopify_Stock_Checker`

2. Change to docker directory `Shopify_Stock_Checker/discord_webhook_script_docker`

   `cd Shopify_Stock_Checker/discord_webhook_script_docker`

3. Create a file named `list.txt`. The file should contain a newline separated list of urls for items to check stock of. 

    For example: 
    ```
    https://examplestore.com/products/exampleproduct
    https://examplestore.com/products/exampleproduct2?variant=39615971195628
    https://examplestore.com/collections/examplecollection/products/exampleproduct3
    ```

    To check only specific variants of a product, be sure to use a url with the correct `?variant={variantid}` suffix. 
    
    To check all variants of a product, remove the `?variant={variantid}` suffix from the url if it appears.

4. Edit `docker-compose.yaml` file and change `WEBHOOK_URL=` with your own.

5. Edit `WEBHOOK_CONTENT=` to configure the message content you want to send when a product goes from out of stock to in stock.

    `{Name}` sends the item's name.

    `{Title}` sends the item's title.

    `{SKU}` sends the item's sku.

    `{Public Title}` sends the item's public title.

    `{Option1}` sends the item's option1.

    `{Option2}` sends the item's option2.

    `{Option3}` sends the item's option3.

    `{Link}` sends a link to the item's store page.

6. Optionally, edit the delays to change the delay in seconds between checking stock, looping batch, and request fail.

    `STOCK_DELAY` adds a delay after sending the stock check request.

    `BATCH_DELAY` adds a delay between checking the full list of products. Only used between the last item in the list and the first item in the list when looping back to the first item.

    `REQUEST_FAIL_DELAY` adds a delay after a request fails before resuming the sending of requests.

7. Start the docker container

   `sudo docker-compose up -d`

## Troubleshooting

To reset stock states and tracking, delete `./discord_webhook_script_docker/stock_state.json`. This will remove the current stock data collected by the script. Upon running the script again it will rerecord the stock states. This will cause the script to resend webhook messages for items that had previously been recorded as in stock and have not had a change in state.
