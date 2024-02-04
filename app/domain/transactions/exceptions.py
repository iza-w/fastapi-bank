from app.domain.exceptions import ObjectDoesNotExist


class TransactionDoesNotExist(ObjectDoesNotExist):
    def __init__(self, transaction_id: int) -> None:
        self.transaction_id = transaction_id
        super().__init__(f"Transaction {transaction_id} does not exist.")
