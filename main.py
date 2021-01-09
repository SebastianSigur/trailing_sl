import get_data
import time
from datetime import datetime

URL = 'https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch'
XPATH = '//span[@data-reactid="32"]/text()'

class stock:
    def __init__(self, stock_url, stock_XPath, file_name):
        self._url = stock_url
        self._XPath = stock_XPath
        self.price = 0
        self.file_name = file_name
        self.stop_loss = 0

    def update_stop_loss(self, procent, current_price):
        if float(current_price) > float(self.price):
            self.stop_loss = float(self.price) - (float(self.price)*(float(procent)/100))

    def write_to_text_file(self, file, string):
        with open(file, 'a') as f:
            f.write(string)

    def check_line_in_text_file(self, file, line):
        with open(file) as f:
            list_of_lines = f.readlines()
            line = list_of_lines[line]
            print(line)

    def call(self, time_delay, stop_loss_prosentage):
        while True:
            current_price = get_data.get_data_from_website(URL, self._XPath)[0]
            current_price = current_price.replace(',', '')
            self.update_stop_loss(stop_loss_prosentage, current_price)
            if self.price != current_price:
                now = datetime.now()
                self.price = current_price
                self.write_to_text_file(self.file_name, f"Price is {self.price} at ->{now.strftime('%H:%M:%S')}. Stop loss at ->{self.stop_loss}\n")
            time.sleep(time_delay)

bitcoin = stock(URL, XPATH, "output.txt")
bitcoin.call(5, 1)
