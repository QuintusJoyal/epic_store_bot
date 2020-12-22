import requests
import json
from .pgdb import Dtabase

db = Dtabase()

class Handle:
    def __init__(self):
        pass

    def check(self):

        t = []
        u = requests.get('https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US').json()
        lot_data = u['data']['Catalog']['searchStore']['elements']
        for i in range(len(lot_data)):
            try:
                start_date = lot_data[i]['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['startDate']
                end_date = lot_data[i]['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['endDate']
                state = "coming soon"
            except:
                try:
                    start_date = lot_data[i]['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['startDate']
                    end_date = lot_data[i]['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate']
                    state = "available"
                except:
                    start_date = 0
                    end_date = 0
                    state = "unknown"

            for j in lot_data[i]['keyImages']:
                try:
                    if str(j['type']) == "OfferImageWide":
                        thumb = str(j['url']) + "?h=427&resize=1&w=320"
                        break
                    else:
                        thumb = str(lot_data[i]['keyImages'][0]['url']) + "?h=427&resize=1&w=320"
                except:
                    thumb = None

            t.append({
                    "title": lot_data[i]['title'],
                    "thumbnail": thumb,
                    "url": "https://www.epicgames.com/store/en-US/product/" + [ o for o in lot_data[i]['customAttributes'] if o.get('key', '') == 'com.epicgames.app.productSlug'][0]['value'],
                    "start_date": start_date,
                    "end_date": end_date,
                    "state": state
                    })

        return t

    def save_cookies(self, cookie_d):
        db.ins_cookie(json.dumps(cookie_d))
        print('Cookie_Saved')

    def get_cookie(self):
        cookies_d = db.get_dta('browser_cookies')
        cookies_l = []
        for c in list(cookies_d.keys()):
            cookies_l.append(cookies_d[c])

        return cookies_l

    def owned(self, gname, gdata):
        if gname in list(db.get_dta('games_ordered').keys()):
            print('Already owned')
        else:
            db.insert_dta(gname, json.dumps(gdata))

            print('Added to purchased list')
