import os
import random

DATA_RECORD_FILE = 'bank_accounts.txt'

class CoreAccount:
    def __init__(self, account_id, account_key, account_category, current_funds=0):
        self.account_id = account_id
        self.account_key = account_key
        self.account_category = account_category
        self.current_funds = current_funds

    def add_funds(self, amount):
        self.current_funds += amount
        print(f"Deposited {amount}. Current balance is {self.current_funds}.")

    def deduct_funds(self, amount):
        if amount > self.current_funds:
            print("Inadequate balance.")
        else:
            self.current_funds -= amount
            print(f"Withdrew {amount}. Current balance is {self.current_funds}.")

    def show_balance(self):
        print(f"Current balance: {self.current_funds}")

class PersonalAccount(CoreAccount):
    def __init__(self, account_id, account_key, current_funds=0):
        super().__init__(account_id, account_key, 'Personal', current_funds)

class CompanyAccount(CoreAccount):
    def __init__(self, account_id, account_key, current_funds=0):
        super().__init__(account_id, account_key, 'Business', current_funds)

class BankingHub:
    def __init__(self):
        self.user_accounts = self.load_accounts()

    def load_accounts(self):
        user_accounts = {}
        if os.path.exists(DATA_RECORD_FILE):
            with open(DATA_RECORD_FILE, 'r') as file:
                for line in file:
                    account_id, account_key, account_category, current_funds = line.strip().split(',')
                    current_funds = float(current_funds)
                    if account_category == 'Personal':
                        user_accounts[account_id] = PersonalAccount(account_id, account_key, current_funds)
                    elif account_category == 'Business':
                        user_accounts[account_id] = CompanyAccount(account_id, account_key, current_funds)
        return user_accounts

    def store_accounts(self):
        with open(DATA_RECORD_FILE, 'w') as file:
            for user_account in self.user_accounts.values():
                file.write(f"{user_account.account_id},{user_account.account_key},{user_account.account_category},{user_account.current_funds}\n")

    def register_account(self, account_category):
        account_id = str(random.randint(100000, 999999))
        account_key = str(random.randint(1000, 9999))
        if account_category == 'individual':
            user_account = PersonalAccount(account_id, account_key)
        elif account_category == 'business':
            user_account = CompanyAccount(account_id, account_key)
        else:
            print("Invalid account category.")
            return
        self.user_accounts[account_id] = user_account
        self.store_accounts()
        print(f"Account created. Your Account Number: {account_id}, Password: {account_key}")

    def verify_credentials(self, account_id, account_key):
        user_account = self.user_accounts.get(account_id)
        if user_account and user_account.account_key == account_key:
            return user_account
        else:
            print("Invalid credentials.")
            return None

    def transfer_funds(self, sender_id, receiver_id, transfer_amount):
        sender_account = self.user_accounts.get(sender_id)
        receiver_account = self.user_accounts.get(receiver_id)
        if not receiver_account:
            print("No such account.")
        elif sender_account.current_funds < transfer_amount:
            print("Insufficient funds.")
        else:
            sender_account.deduct_funds(transfer_amount)
            receiver_account.add_funds(transfer_amount)
            self.store_accounts()
            print(f"Successfully transferred {transfer_amount} to account {receiver_id}.")

    def delete_account(self, account_id, account_key):
        user_account = self.user_accounts.get(account_id)
        if user_account and user_account.account_key == account_key:
            del self.user_accounts[account_id]
            self.store_accounts()
            print("Account removed successfully.")
        else:
            print("Invalid credentials.")

def run_banking_system():
    banking_hub = BankingHub()
    while True:
        print("\n1. Open Account\n2. Login\n3. Exit")
        user_choice = input("Enter choice: ")
        if user_choice == '1':
            account_category = input("Enter account type (individual/business): ").lower()
            if account_category in ['individual', 'business']:
                banking_hub.register_account(account_category)
            else:
                print("Invalid account type.")
        elif user_choice == '2':
            account_id = input("Enter account number: ")
            account_key = input("Enter password: ")
            user_account = banking_hub.verify_credentials(account_id, account_key)
            if user_account:
                while True:
                    print("\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Transfer Funds\n5. Close Account\n6. Logout")
                    action_choice = input("Enter action: ")
                    if action_choice == '1':
                        user_account.show_balance()
                    elif action_choice == '2':
                        deposit_amount = float(input("Enter amount to deposit: "))
                        user_account.add_funds(deposit_amount)
                    elif action_choice == '3':
                        withdraw_amount = float(input("Enter amount to withdraw: "))
                        user_account.deduct_funds(withdraw_amount)
                    elif action_choice == '4':
                        receiver_id = input("Enter receiver account number: ")
                        transfer_amount = float(input("Enter amount to transfer: "))
                        banking_hub.transfer_funds(account_id, receiver_id, transfer_amount)
                    elif action_choice == '5':
                        banking_hub.delete_account(account_id, account_key)
                        break
                    elif action_choice == '6':
                        break
                    else:
                        print("Invalid action.")
        elif user_choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    run_banking_system()
