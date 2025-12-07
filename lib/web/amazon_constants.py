class AmazonSelectors:
    BASE_URL = "https://www.amazon.com/"
    
    # Selectors - Search
    SEARCH_INPUT = "#twotabsearchtextbox"
    SEARCH_SUBMIT_BUTTON = "#nav-search-submit-button"
    SEARCH_RESULT_SLOT = ".s-main-slot"
    SEARCH_RESULT_ITEM = ".s-result-item[data-component-type='s-search-result']"
    SEARCH_RESULT_TITLE = ".s-result-item[data-component-type='s-search-result'] h2"
    SEARCH_RESULT_LINK = "div[data-component-type='s-search-result'] h2 a"
    SEARCH_RESULT_PRICE_WHOLE = ".s-result-item[data-component-type='s-search-result'] .a-price-whole"
    SEARCH_RESULT_PRICE_FRACTION = ".s-result-item[data-component-type='s-search-result'] .a-price-fraction"
    NO_RESULTS_TEXT = "text=No results for"

    # Selectors - Cart
    ADD_TO_CART_BUTTON = "#add-to-cart-button"
    ADDED_TO_CART_CONFIRM_SELECTORS = "#NATC_SMART_WAGON_CONF_MSG_SUCCESS_text, #huc-v2-order-row-confirm-text, text=Added to Cart"
    ADDED_TO_CART_TEXT = "text=Added to Cart"
    ADDED_TO_CART_SUCCESS_ID = "#NATC_SMART_WAGON_CONF_MSG_SUCCESS_text"
    CART_COUNT_BADGE = "#nav-cart-count"
    NAV_CART = "#nav-cart"
    CART_DELETE_BUTTON = "input[value='Delete']"
    CART_EMPTY_MSG = "text=Your Amazon Cart is empty"
    CHECKOUT_BUTTON = "input[name='proceedToRetailCheckout']"

    # Selectors - Product Detail
    PRODUCT_TITLE = "#productTitle"
    DETAIL_PRICE_WHOLE = ".a-price-whole"
    DETAIL_PRICE_FRACTION = ".a-price-fraction"
    
    # Selectors - Misc
    PAGE_BODY = "body"
    NAV_BAR_LINK_TEMPLATE = "#nav-xshop a:has-text(\"{}\")"
    BRAND_FILTER_TEMPLATE = "#brandsRefinements a:has-text('{}')"
