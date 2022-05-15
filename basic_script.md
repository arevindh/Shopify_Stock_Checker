# Basic Script

## Dependencies

Python 3: [Download link](https://www.python.org/downloads/)

Python `requests` module: To install, enter the following command in cmd or a terminal:

```
pip install requests
```

## Usage

1. Create a file named `list.txt` in the same directory as `check_shopify_stock.py`. The file should contain a newline separated list of urls for items to check stock of. 

    For example: 
    ```
    https://examplestore.com/products/exampleproduct
    https://examplestore.com/products/exampleproduct2?variant=39615971195628
    https://examplestore.com/collections/examplecollection/products/exampleproduct3
    ```

    To check only specific variants of a product, be sure to use a url with the correct `?variant={variantid}` suffix. 
    
    To check all variants of a product, remove the `?variant={variantid}` suffix from the url if it appears.

2. Run `check_shopify_stock.py`

3. Optionally, edit the delays in `config.cfg` to change the delay in seconds between checking stock, checking cart, and request fail. (`config.cfg` is generated after starting the script once)

    `stock_delay` adds a delay after sending the stock check request.

    `batch_delay` is unused in the basic script. It is for the webhook only.

    `request_fail_delay` adds a delay after a request fails before resuming the sending of requests.
