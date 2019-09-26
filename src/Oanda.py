import sys
import json
import v20


class Oanda:
    def __init__(self, api, accountID, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accountID = accountID
        self.api = api

    def get_account_summary(self):
        response = self.api.account.summary(self.accountID).get("account", 200)
        return response

    def get_account_instruments(self):
        response = self.api.account.instruments(self.accountID).get("instruments", 200)
        return response

    def get_transaction_list(self):
        response = self.api.transaction.list(self.accountID)
        transaction_list = {}
        transaction_list["from"] = response.get("from")
        transaction_list["to"] = response.get("to")
        transaction_list["pageSize"] = response.get("pageSize")
        transaction_list["count"] = response.get("count")
        transaction_list["pages"] = response.get("pages")
        transaction_list["lastTransactionID"] = response.get("lastTransactionID")
        return transaction_list

    def get_transaction_range(self, from_id, to_id, filter):
        response = self.api.transaction.range(
            self.accountID,
            fromID=from_id,
            toID=to_id,
            type=filter)
        transactions = response.get("transactions", 200)
        return transactions
