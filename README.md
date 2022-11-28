# Shopify Stock Checker

Scripts to check stock of shopify items.

## [Basic Script](basic_script.md)

Single run stock checking in command line. 

## [Discord Webhook Script](discord_webhook_script.md)

Automated stock checking and notifying through discord webhook.

## Docker 

Create `docker-compose.yaml`

```yaml
version: '3.3'
services:
  shopify_stock:
    container_name: shopify_stock
    volumes:
      - './list.txt:/usr/app/list.txt'
    environment:
      - 'WEBHOOK_URL=url-'
    image: arevindh/shopify_stock
```

Create a file named `list.txt` .  The file should contain a newline separated list of urls for items to check stock of. 

For example: 
```
https://examplestore.com/products/exampleproduct
https://examplestore.com/products/exampleproduct2?variant=39615971195628
https://examplestore.com/collections/examplecollection/products/exampleproduct3
```

To check only specific variants of a product, be sure to use a url with the correct `?variant={variantid}` suffix. 

To check all variants of a product, remove the `?variant={variantid}` suffix from the url if it appears.