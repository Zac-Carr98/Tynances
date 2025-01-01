import os

# Define categories and keywords from .env or hardcoded values
CATEGORY_ORDER = os.getenv('CATEGORY_ORDER', '').split(',')

class CategorySorter:
    def __init__(self):
        self.categories = {
            'EatingOut': ['HOUSE', 'ANGEL', 'Canadian Bakin', 'BELL', 'STARBUCKS', 'Rock N Roll', 'POPEYES',
                          'BOOT PIZZERIA HUNTSVILLE', 'CHICK-FIL-A', 'BLANCA', '*ROOSTER\'S CROW', '*TURBO COFFEE',
                          'TACO MAMA', 'Hatch Cafe', '#352103', 'DRIVE IN #5842', 'GUADALAJARA', 'BUS BREWING',
                          'MOON HUNTSVILLE', 'MERCADO LA COLONIHUNTSVILLE', '*GOLD SPRINT', 'House HUNTSVILLE',
                          'BRUEGGERS', 'WINDMILL BEVERAGES', 'CAVA WHITESBURG 256-696-5970', 'HATCH CAFE',
                          'MASON DIXON BAKERYHUNTSVILLE', 'LES JOURS', 'TST* HOUND & HARVEST', 'EL HERRADURA',
                          'TROPICAL SMOOTHIE CAFE', 'UAH HUNTSVILLE DUNKIN', 'WHATABURGER', 'GOOD COMPANY CAFE',
                          'Waffle House', '*DOMINO\'S'],
            'Groceries': ['Walmart', 'Wal-Mart', 'T-1367', 'WAL-MART', '70080', '9040', 'HTTPSINSTACARCAUS', '#1785 HUNTSVILLE',
                          '70080', '70083', 'WM SUPERCENTER', 'PUBLIX', 'JOE S #69'],
            'Home Reno': ['HOME DEPOT', 'HOMEDEPOT', 'FLOORING', '#41 10050', '866-483-7521', '10012 S MEMORIAL PKWY'],
            'Utilities': ['866-496-9669', 'UNITEDWHOLESALE', 'UTILITIES', '*Prime Pest LLC', 'HMFUSA.com', 'FARM RO',
                          'MORTGAGE MTG SERVICING'],
            'Payroll': ['TECHNOLO', 'CITY - PAYROLL'],
            'Gas': ['SERVICE STATION', 'OIL', 'MARATHON', 'CHEVRON', 'EXXON', 'SUNOCO'],
            'Venmo': ['Visa Direct', 'CASHOUT',],
            'Amazon': ['Mktp', 'AMAZON', 'Amazon', 'Amzn.com/billWAUS'],
            'Subscriptions': ['APPLE', 'Spotify', 'Reformed', 'NEXUSMODS', 'OF THE VALLEY', 'MICROSOFT', 'DISCORD',
                              'POSHERVA', 'Money - Premium', '*CLOUDFLARE', 'BUBBLES EXPRESS WASH'],
            'Fun Money': ['GAMES', 'Etsy.com', 'GOODWILL', 'BUY #514', 'NASA EXCHANGE', '*BESTBUY', '4112 VAL BEND 18',
                          'ONLINE 9640 888', 'NASA Bldg. 4203', '*G2A', 'MICHAELS', 'POSHMARK', 'HOBBYLOBBY',
                          'SAVING WAY - SOUTH', '*STEAM PURCHASE', '*PARTSEXPRES', 'HUNTSVILLE 26'],
            'Unplanned': ['FIRESTONE1', 'STAPLES', 'Supplies Plus', 'TOUCH GARDEN', 'ROCKET CAR WASH', 'PETSMART',
                          'AUTOZONE', 'ADVANCE AUTO PARTS', 'DIXIE WASH', 'MADISON COUNTY LICENSE'],
            'Medical': ['HUNTSVILLE HOSPITAL', 'WWW.HSCCOFAL.COM DECATUR', 'ALABAMA DERMATOLOGY', '*GREEN PRIMARY CARE',
                        'WHITESBURG ANIMAL HOSPIHUNTSVILLE', 'COUNSELING 101 LOWE', 'WWW.ROCKETCITYCOLLECTIVHUNTSVILLE',
                        'CRESTWOOD PHYS', 'WOMEN4WOMEN']
        }
        self.categories = {category: self.categories[category] for category in CATEGORY_ORDER}

    def categorize_data(self, df):
        category_data = {category: [] for category in self.categories}
        category_data['Other'] = []
        for _, row in df.iterrows():
            for category, keywords in self.categories.items():
                if any(str(keyword) in str(row[2]) for keyword in keywords):
                    category_data[category].append(row.to_dict())
                    break
            else:
                category_data['Other'].append(row.to_dict())
        return category_data