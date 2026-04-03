from bs4 import BeautifulSoup
import requests
from plyer import notification

URL: str = "https://www.amazon.com/Razer-Viper-Wireless-Esports-Gaming/dp/B0CW25XR5R?crid=2RR4OCP9DP3KN&dib=eyJ2IjoiMSJ9.BGHfQhfkTBo0y9hDkJpjFBeNjZ-BWz3KpPOWaoKxrYUIK42tLmg5NMVYqrhJMU5JJ6NAutn3tCjns10z7mpgLuemm22h4i16uRpVxRSyfAE8zxXW24k3QB75l2sr4zH6tuDqyoWsjrETc3ZQpsQyYPdRTtGhQ_DQHV_lgHEZpkca_U0JJJOsCgqagU9p6GEnhhLimnLJhjX6nUEuMjAKzAs4QYbUpy1KV2gddb7xass.rfzHVDqfI7wscamrM60b8ScJFfV_TRZ1ki-CLBZv9B0&dib_tag=se&keywords=viper+v3+pro&qid=1775105636&sprefix=viper+v3+pro%2Caps%2C173&sr=8-2&ufe=app_do%3Aamzn1.fos.2e3b5aa5-f8d0-4dc3-9548-d7ef437ce444"
ITEMS_TO_CHECK = {}
ITEMS_PRICE_RESULT = {}


def get_items() -> None:
    item = input("Enter item link, price. Enter 'done' when done \n")
    
    while item != "done":
        item_ , price = item.split(",")
        ITEMS_TO_CHECK[item_] = int(price)
        item = input("Enter item link, price. Enter 'done' when done \n")
    
    
    
def check_price() -> None:
    #make request to URL
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    for key in ITEMS_TO_CHECK.keys():
        page = requests.get(key, headers=headers)
        
        #check if request successful
        if page.status_code == 200:
        
            #get the parsed HTML
            parsed_html = BeautifulSoup(page.text, "html.parser")
            
            #extract price
            price = parsed_html.find("span", class_="a-price-whole")
            if price:
                ITEMS_PRICE_RESULT[key] = int(price.get_text().strip("."))
            else:
                print("Price element not found")
                continue
        else:
            print("Error fetching page data")
            continue
        

def notify_price() -> None:
    for key in ITEMS_PRICE_RESULT.keys():
        if ITEMS_PRICE_RESULT[key] != None and ITEMS_PRICE_RESULT[key] <= ITEMS_TO_CHECK[key]:
            try:
                if notification.notify is not None:
                    notification.notify(
                        title='Price Alert',
                        message=f'Price is ${ITEMS_PRICE_RESULT[key]}!',
                        app_name='Price Tracker',
                        timeout=10
                    )
            except Exception as e:
                print(f"Notification failed: {e}")
                
def run_app() -> None:
    get_items()
    check_price()
    notify_price()


if __name__ == "__main__":
    run_app()
