class ExchangeNotFoundException(Exception):
    def __init__(self, exchange_id: str):
        self.message = f'Exchange with id {exchange_id} not found'
