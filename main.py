import get_data
import time
from datetime import datetime

URL = 'https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch'
XPATH = '//span[@data-reactid="32"]/text()'

# URL = 'https://www.timeanddate.com/worldclock/usa/new-york'
# XPATH = '//span[@class="h1"]/text()'

class stock:
    def __init__(self, stock_url, stock_XPath, file_name):
        self._url = stock_url
        self._XPath = stock_XPath
        self.best_price = 0.0
        self.price = 0.0
        self.file_name = file_name
        self.stop_loss = 0.0
        self.first_setup = True
        self.is_buying = False
        self.buy_short_price = 0.1
        self.money = 100
        self.p_l_from_buy = 0.0
        self.lowest_price = 'NAN'
        self.procent_move_from_sell = 0.0
        self.now_money = 100
        self.sell_price = 0.0
        self.status = ''

    def update_stop_loss(self, procent, current_price):
        if self.price == 0:
            self.stop_loss = float(current_price) - (float(current_price) * (float(procent) / 100))
        if float(current_price) >= float(self.best_price):
            self.stop_loss = float(self.best_price) - (float(self.best_price) * (float(procent) / 100))

    def update_best_price(self, current_price):
        if float(current_price) > float(self.best_price):
            self.best_price = current_price

    def update_lowest_price(self):
        if float(self.price) < float(self.lowest_price):
            self.lowest_price = self.price

    def write_to_text_file(self, file, string):
        with open(file, 'a') as f:
            f.write(string)

    def check_line_in_text_file(self, file, line):
        with open(file) as f:
            list_of_lines = f.readlines()
            line = list_of_lines[line]
            print(line)

    def buy_short(self, stop_loss_prosentage):
        # kaupa eða shorta
        self.buy_short_price = self.price
        self.is_buying = True
        self.best_price = self.price
        self.update_stop_loss(stop_loss_prosentage, self.best_price)
        self.procent_move_from_sell = 'NAN'
        self.status = 'buying'
       #print('buy')

    def check_loss(self):
        if float(self.price) <= float(self.stop_loss):
            return True
        else:
            return False

    def sell(self):
        # selja
        self.is_buying = False
        self.sell_price = self.price
        self.status = 'Selling'

    def update_money(self):
        if self.is_buying:
            try:
                self.now_money = self.money * (float(self.price) / float(self.buy_short_price))
                self.p_l_from_buy = (float(self.price) / float(self.buy_short_price) - 1) * 100
                # print(float(self.price)/float(self.buy_short_price)*100)
            except ZeroDivisionError:
                pass
        #print(str(self.now_money) + "kr")

    def should_i_buy(self, buy_procent, stop_loss_prosentage):
        if self.procent_move_from_sell >= buy_procent:
            self.buy_short(stop_loss_prosentage)

    def call(self, time_delay, stop_loss_prosentage, buy_procent):
        current_price = 'Fullscreen'
        while current_price == 'Fullscreen':
            current_price = get_data.get_data_from_website(URL, self._XPath)
            if current_price[0] == 'Fullscreen':
                print('Waring')
            current_price = current_price[0]

        current_price = current_price.replace(',', '')
        self.update_best_price(current_price)
        self.update_stop_loss(stop_loss_prosentage, current_price)
        if self.price != current_price:
            now = datetime.now()
            self.price = current_price
            self.update_money()
            if self.status != 'buying' and self.status != 'selling':
                self.status = 'holding'

            if self.first_setup:
                self.best_price = self.price
                self.buy_short(stop_loss_prosentage)
                self.first_setup = False

            if self.is_buying:
                s_l_hit = self.check_loss()
                if s_l_hit:
                    self.sell()
                    #print('sold')
                    self.lowest_price = self.price
            else:
                self.update_lowest_price()
                self.procent_move_from_sell = (float(self.price)/float(self.lowest_price)-1)*100
                self.should_i_buy(buy_procent, stop_loss_prosentage)
            self.write_to_text_file(self.file_name, f"Price: {self.price} at {now.strftime('%H:%M:%S')}. \n"
                                                    f"Stop loss: {self.stop_loss}.\n"
                                                    f"Best price: {self.best_price}\n"
                                                    f"P/L %: {self.p_l_from_buy}\n"
                                                    f"% move from lowest price {self.procent_move_from_sell}\n"
                                                    f"Lowest Price: {self.lowest_price}\n"
                                                    f"Money P/L: {self.now_money}\n" 
                                                    f"Status: {self.status}"
                                                    f"\n\n")
            time.sleep(time_delay)


def main():
    bitcoin1 = stock(URL, XPATH, "output0.1-0.1.txt")
    bitcoin3 = stock(URL, XPATH, "output0.3-0.3.txt")
    bitcoin5 = stock(URL, XPATH, "output0.5-0.5.txt")
    bitcoin10 = stock(URL, XPATH, "output1-1.txt")
    while True:
        bitcoin1.call(1, 0.1, 0.1)
        bitcoin3.call(1, 0.3, 0.3)
        bitcoin5.call(1, 0.5, 0.5)
        bitcoin10.call(1, 1, 1)

main()
