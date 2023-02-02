from bs4 import BeautifulSoup
from parser.get_bestchange import get_page
from parser.parser_exceptions import ExchangeNotFoundException

# TODO подумать про Exception и логеры


class ExchangeAnalyst:
    """
    Класс, анализирующий курс в обменнике по id обменника
    """
    def __init__(self, exchange_id: str):
        self.exchange_id = exchange_id
        self.page_path = 'bitcoin-to-tether-trc20.html'

    @property
    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(get_page(self.page_path), 'html5lib')

    async def get_best_exchange(self) -> BeautifulSoup:
        """
        Получает строку (элемент) лучшего обменника

        :return: Строка лучшего (первого в списке) обменника
        :rtype: BeautifulSoup
        """
        content_table = self.soup.body.find(id='content_table')
        best_exchange = content_table.tbody.find()
        return best_exchange

    async def get_cur_exchange(self) -> BeautifulSoup:
        """
        Получает строку (элемент) текущего обменника

        :return: строка текущего обменника
        :rtype: BeautifulSoup
        """
        content_table = self.soup.body.find(id='content_table')
        links = content_table.tbody.find_all('a')
        curr_exchange = None
        for link in links:
            href = link.get('href')
            if f'?id={self.exchange_id}' in href:
                curr_exchange = link.parent.parent.parent
                break
        if not curr_exchange:
            raise ExchangeNotFoundException(self.exchange_id)
        return curr_exchange

    @staticmethod
    async def get_exchange_price(exchange: BeautifulSoup) -> float:
        """
        Вычисляет курс обменника по элементу обменника.

        :param exchange: строка (элемент) обменника
        :type exchange: BeautifulSoup
        :return: обменный курс в выбранном обменнике
        :rtype: float
        """

        exchange_rate_str = exchange.find_all('td', 'bi')[1].get_text("|", strip=True)
        exchange_rate = float(exchange_rate_str.split('|')[0].replace(' ', ''))
        return exchange_rate

    async def get_diff_with_best(self) -> float:
        """
        Метод считает разницу между лучшим обменным курсом и курсом текущего обменника

        :return: разница в курсе между текущим и выбранным обменником
        :rtype: float
        """
        best_exchange_price = await self.get_exchange_price(await self.get_best_exchange())
        curr_exchange_price = await self.get_exchange_price(await self.get_cur_exchange())
        return round(best_exchange_price - curr_exchange_price, 4)
