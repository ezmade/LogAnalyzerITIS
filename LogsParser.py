from pyparsing import Word, alphas, nums, Suppress
from geoip2 import database, errors
from re import search
from sqlite3 import connect

class Link(object):
    
    def __init__(self):
        self.product_category = None
        self.product_name = None
        self.goods_id = None
        self.amount = None
        self.cart_id = None
        self.user_id = None
        self.payment_id = None
        
    def SplitTheLink(self, link):
        request = search(r'bottom.com/(.*)', link).group(1)
        
        if request.startswith('pay?'):
            self.user_id, self.cart_id = search(r'user_id=(\w+)&cart_id=(\w+)', request).groups()

        elif request.startswith('cart?'):
            self.goods_id, self.amount, self.cart_id = search(r'goods_id=(\w+)&amount=(\w+)&cart_id=(\w+)', request).groups()
    
        if request.startswith('success_'):
            self.payment_id = search(r'pay_(\w+)/', request).group(1)

        elif request.count('/') is 0:
            self.product_category = None
            
        elif request.count('/') is 1:
            self.product_category = request[:-1]

        elif request.count('/') is 2:
            self.product_category, self.product_name = search(r'(\w+)/(\w+)', request).groups()
            
    
    def ShowTheLink(self, link):
        print(link)
        print(self.product_category, self.product_name, self.goods_id, self.amount, self.cart_id, self.user_id)
    
class Log(object):
    
    def __init__(self):
        self.api_name = Word(alphas + '_')
        self.date = Word(nums + '-')
        self.time = Word(nums + ':')
        self.key = Word(alphas + nums)
        self.ip = Word(nums + '.')
        self.link = Word(alphas + nums + ':' + '/' + '.' + '_' + '?' + '&' + '=')
    

    def GetCountryNameByIP(self, ip):
        try:
            country_name = reader.country(ip).country.name
        except errors.AddressNotFoundError:
            country_name = None
        return country_name
            

    def InsertDataToDatabase(self, LOG):
        self.LOG_full = Suppress(self.api_name + '|') + self.date + self.time + Suppress('[' + self.key + ']' + 'INFO:') + self.ip + self.link
        info = self.LOG_full.parseString(LOG)
        date , time, ip, link= info[0:4]
        l = Link()
        l.SplitTheLink(link)
        cursor.execute('''INSERT INTO requests (date, time, ip, country, category, product, good_id, cart_id, payment_id) VALUES('%s','%s','%s', '%s', '%s', '%s', '%s', '%s', '%s');''' % (date, time, ip, self.GetCountryNameByIP(ip), l.product_category, l.product_name, l.goods_id, l.cart_id, l.payment_id))
        print(date, time, ip, self.GetCountryNameByIP(ip), l.product_category, l.product_name, l.goods_id, l.cart_id, l.payment_id)
        

if __name__ == '__main__':
    reader = database.Reader('GeoLite2-Country.mmdb')
    connection = connect('data.db')
    cursor = connection.cursor()
    cursor.executescript('''CREATE TABLE "requests" (
				'id'         INTEGER PRIMARY KEY AUTOINCREMENT,
                'date'       TEXT,
                'time'       TEXT,
                'ip'         TEXT,
                'country'    TEXT,
                'category'   TEXT,
                'product'    TEXT,
                'good_id'    TEXT,
                'cart_id'    TEXT,
                'payment_id' TEXT);''')
    connection.commit()
    
    LOG = Log()
    logsFile = open('logs.txt', 'r')
    #s = logsFile.readline()
    #LOG.MakeFullData(s)
    for log in logsFile:
       LOG.InsertDataToDatabase(log)
    logsFile.close()
    print('All data are in database!')
    connection.commit()
    connection.close()


   




