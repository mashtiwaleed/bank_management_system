import json
import os
import random
from datetime import datetime

DATA_FILE = "bank_data.json"


class BankAccount:
    def __init__(self, name, account_number, password, balance=0, history=None):
        self.name = name
        self.account_number = account_number
        self.password = password
        self.balance = balance
        self.history = history if history is not None else []

    def add_history(self, text):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"{time} - {text}")

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid amount.")
        else:
            self.balance += amount
            self.add_history(f"Deposited {amount} CZK")
            print(f"Deposit successful. Balance: {self.balance} CZK")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid amount.")
        elif amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            self.add_history(f"Withdrawn {amount} CZK")
            print(f"Withdrawal successful. Balance: {self.balance} CZK")

    def show_info(self):
        print("\n----- Account Information -----")
        print(f"Name: {self.name}")
        print(f"Account Number: {self.account_number}")
        print(f"Balance: {self.balance} CZK")

    def show_history(self):
        print("\n----- Transaction History -----")
        if not self.history:
            print("No transactions yet.")
        else:
            for item in self.history:
                print(item)


def load_accounts():
    accounts = {}

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

            for acc_num, acc_data in data.items():
                accounts[acc_num] = BankAccount(
                    acc_data["name"],
                    acc_data["account_number"],
                    acc_data["password"],
                    acc_data["balance"],
                    acc_data["history"]
                )

    return accounts


def save_accounts(accounts):
    data = {}

    for acc_num, account in accounts.items():
        data[acc_num] = {
            "name": account.name,
            "account_number": account.account_number,
            "password": account.password,
            "balance": account.balance,
            "history": account.history
        }

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def generate_account_number(accounts):
    while True:
        number = str(random.randint(10000, 99999))
        if number not in accounts:
            return number


def create_account(accounts):
    name = input("Enter full name: ")
    password = input("Create password: ")

    account_number = generate_account_number(accounts)

    accounts[account_number] = BankAccount(name, account_number, password)
    save_accounts(accounts)

    print("\nAccount created successfully.")
    print(f"Your account number is: {account_number}")


def login(accounts):
    account_number = input("Enter account number: ")
    password = input("Enter password: ")

    if account_number not in accounts:
        print("Account not found.")
        return None

    account = accounts[account_number]

    if account.password != password:
        print("Wrong password.")
        return None

    print(f"\nWelcome, {account.name}!")
    return account


def transfer_money(accounts, sender):
    receiver_number = input("Enter receiver account number: ")

    if receiver_number not in accounts:
        print("Receiver account not found.")
        return

    if receiver_number == sender.account_number:
        print("You cannot transfer money to yourself.")
        return

    amount = float(input("Enter amount to transfer: "))

    if amount <= 0:
        print("Invalid amount.")
    elif amount > sender.balance:
        print("Insufficient funds.")
    else:
        receiver = accounts[receiver_number]

        sender.balance -= amount
        receiver.balance += amount

        sender.add_history(f"Transferred {amount} CZK to {receiver.name} ({receiver.account_number})")
        receiver.add_history(f"Received {amount} CZK from {sender.name} ({sender.account_number})")

        save_accounts(accounts)
        print("Transfer successful.")


def account_menu(accounts, account):
    while True:
        print(f"\n----- Account Menu: {account.name} -----")
        print("1. Deposit money")
        print("2. Withdraw money")
        print("3. Check balance")
        print("4. Show account information")
        print("5. Show transaction history")
        print("6. Transfer money")
        print("7. Change account name")
        print("8. Back to main menu")

        choice = input("Choose an option: ")

        if choice == "1":
            amount = float(input("Enter amount to deposit: "))
            account.deposit(amount)
            save_accounts(accounts)

        elif choice == "2":
            amount = float(input("Enter amount to withdraw: "))
            account.withdraw(amount)
            save_accounts(accounts)

        elif choice == "3":
            print(f"Current balance: {account.balance} CZK")

        elif choice == "4":
            account.show_info()

        elif choice == "5":
            account.show_history()

        elif choice == "6":
            transfer_money(accounts, account)

        elif choice == "7":
            new_name = input("Enter new name: ")
            account.name = new_name
            account.add_history(f"Account name changed to {new_name}")
            save_accounts(accounts)
            print("Name updated successfully.")

        elif choice == "8":
            break

        else:
            print("Invalid choice.")


def admin_panel(accounts):
    admin_password = input("Enter admin password: ")

    if admin_password != "admin123":
        print("Wrong admin password.")
        return

    while True:
        print("\n----- Admin Panel -----")
        print("1. Show all accounts")
        print("2. Search account")
        print("3. Delete account")
        print("4. Show total bank balance")
        print("5. Back to main menu")

        choice = input("Choose an option: ")

        if choice == "1":
            if not accounts:
                print("No accounts found.")
            else:
                for acc_num, account in accounts.items():
                    print(f"{acc_num} - {account.name} - {account.balance} CZK")

        elif choice == "2":
            acc_num = input("Enter account number: ")

            if acc_num in accounts:
                accounts[acc_num].show_info()
            else:
                print("Account not found.")

        elif choice == "3":
            acc_num = input("Enter account number to delete: ")

            if acc_num in accounts:
                del accounts[acc_num]
                save_accounts(accounts)
                print("Account deleted successfully.")
            else:
                print("Account not found.")

        elif choice == "4":
            total = 0
            for account in accounts.values():
                total += account.balance

            print(f"Total money in bank: {total} CZK")

        elif choice == "5":
            break

        else:
            print("Invalid choice.")


def main():
    accounts = load_accounts()

    print("======================================")
    print(" Welcome to Waleed National Bank")
    print(" Your trusted Python banking system")
    print("======================================")

    while True:
        print("\n----- Main Menu -----")
        print("1. Create new account")
        print("2. Login to account")
        print("3. Admin panel")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_account(accounts)

        elif choice == "2":
            account = login(accounts)
            if account:
                account_menu(accounts, account)

        elif choice == "3":
            admin_panel(accounts)

        elif choice == "4":
            save_accounts(accounts)
            print("Thank you for using Waleed National Bank.")
            break

        else:
            print("Invalid choice.")


main()