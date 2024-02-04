from app.domain.exceptions import ObjectDoesNotExist


class AccountDoesNotExist(ObjectDoesNotExist):
    def __init__(self, account_id: int) -> None:
        self.account_id = account_id
        super().__init__(f"Account {account_id} does not exist.")


class InsufficientFoundsError(Exception):
    def __init__(self, account_id: int) -> None:
        self.account_id = account_id
        super().__init__(
            f"Account {account_id} has insufficient funds to perform this operation."
        )
