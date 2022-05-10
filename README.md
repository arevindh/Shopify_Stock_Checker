# Shopify Stock Checker

Script to check stock of Shopify store items.

## Dependencies

Python 3: [Download link](https://www.python.org/downloads/)

Python `requests` module: To install, enter the following commands in cmd or a terminal:

```
pip install requests
```

## Usage

1. Create a file named `list.txt` in the same directory as `shopify_stock_checker.py`. The file should contain a newline separated list of urls for items to check stock of. 

    For example: 
    ```
    https://examplestore.com/products/exampleproduct
    https://examplestore.com/products/exampleproduct2?variant=39615971195628
    https://examplestore.com/collections/examplecollection/products/exampleproduct3
    ```

    To check only specific variants of a product, be sure to use a url with the correct `?variant={variantid}` suffix. 
    
    To check all variants of a product, remove the `?variant={variantid}` suffix from the url if it appears.

2. Run `shopify_stock_checker.py`.

