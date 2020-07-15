import random
import sqlite3


def create_connection(db):
    conn = sqlite3.connect(db)
    return conn


def create_table(sql, db='card.s3db'):
    conn = create_connection(db)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def execute_sql(id, number, pin_code, balance=0, db='card.s3db'):
    conn = create_connection(db)
    cur = conn.cursor()
    cur.execute(insert_into_table, (id, number, pin_code, balance))
    conn.commit()
    return cur.lastrowid


def select_all(num, pin_cod, db='card.s3db'):
    conn = create_connection(db)
    cur = conn.cursor()
    cur.execute("SELECT * FROM card")
    rows = cur.fetchall()
    for row in rows:
        print(row)
        if str(num) == row[1] and str(pin_cod) == row[2]:
            return True
    return False


sql_create_card_table = """ CREATE TABLE IF NOT EXISTS card (
                                        id integer PRIMARY KEY ,
                                        number text ,
                                         pin text ,
                                        balance INTEGER DEFAULT 0
                                    ); """

insert_into_table = '''INSERT INTO card (id, number, pin, balance) 
                    VALUES(?, ?, ?, ?)'''
create_table(sql_create_card_table)
exit = {'exit': True, 'quit': True}
nine_digit_card_number_list = list()



def show_menue():
    bank_instruction = ['Create an account', 'Log into account', 'Exit']
    for i in range(len(bank_instruction)):
        if i == 2:
            print(f'0. {bank_instruction[i]}')
        else:
            print(f'{i + 1}. {bank_instruction[i]}')


def state_of_bank_system():
    show_menue()
    what_to_do = int(input())
    if what_to_do == 1:
        create_sixteen_digit_account()
    elif what_to_do == 2:
        log_in()
    elif what_to_do == 0:
        exit['exit'] = False


def generate_nine_digit_card_number():
    card_number = int(''.join([str(random.randint(1, 9)) for _ in range(9)]))
    if card_number not in nine_digit_card_number_list:
        nine_digit_card_number_list.append(card_number)
        return card_number


def add_checksum_digit():
    card_number = str(generate_nine_digit_card_number())
    card_number_list = list()
    numbers_sum = 0
    for i in range(len(card_number)):
        if i % 2 == 0:
            card_number_list.append(int(card_number[i]) * 2)
        else:
            card_number_list.append(int(card_number[i]))
    for j in range(len(card_number_list)):
        if card_number_list[j] > 9:
            card_number_list[j] -= 9
    for k in card_number_list:
        numbers_sum += int(k)
    numbers_sum += 8
    checksum = 10 - numbers_sum % 10
    if checksum == 10:
        return str(card_number) + '0'
    else:
        return str(card_number) + str(checksum)


def luhn_algorithm_check(number):
    card_number = number[6:15]
    card_number_list = list()
    numbers_sum = 0
    for i in range(len(card_number)):
        if i % 2 == 0:
            card_number_list.append(int(card_number[i]) * 2)
        else:
            card_number_list.append(int(card_number[i]))
    for j in range(len(card_number_list)):
        if card_number_list[j] > 9:
            card_number_list[j] -= 9
    for k in card_number_list:
        numbers_sum += int(k)
    numbers_sum += (int(number[0]) * 2)
    checksum = 10 - numbers_sum % 10
    if checksum == 10 and number[-1] == '0':
        return False
    elif int(number[-1]) == checksum:
        return False
    return True


def create_sixteen_digit_account():
    card_number = '400000' + add_checksum_digit()
    # sixteen_digit_number_list.append(int(card_number))
    print('Your card has been created')
    print('Your card number:')
    print(card_number)
    generate_pin_code(card_number)


def generate_pin_code(number):
    random.seed(number)
    pin_code = int(''.join([str(random.randint(1, 9)) for _ in range(4)]))
    print('Your card PIN:')
    print(pin_code)
    # pin_code_list.append(pin_code)
    execute_sql(id=pin_code, number=number, pin_code=pin_code)


def log_in():
    card_number = int(input('Enter your card number:'))
    pin_code = int(input('Enter your PIN:'))
    # if card_number in sixteen_digit_number_list and pin_code in pin_code_list:
    if select_all(num=card_number, pin_cod=pin_code):
        print()
        print('You have successfully logged in!')
        while exit['quit']:
            log_in_menue()
            after_log_in(str(card_number))
    else:
        print('Wrong card number or PIN!')


def log_in_menue():
    log_in_instruction = ['Balance', 'Add income', 'Do transfer', 'Close account', 'Log out', 'Exit']
    for i in range(len(log_in_instruction)):
        if i == 5:
            print(f'0. {log_in_instruction[i]}')
        else:
            print(f'{i + 1}. {log_in_instruction[i]}')


def after_log_in(number):
    what_to_do = int(input())
    if what_to_do == 1:
        get_balance_from_database(number)
    elif what_to_do == 2:
        add_income(number)
    elif what_to_do == 3:
        transfer(number)
    elif what_to_do == 4:
        close_account(number)
    elif what_to_do == 5:
        exit['quit'] = False
    elif what_to_do == 0:
        exit['quit'] = False
        exit['exit'] = False


def close_account(number, db='card.s3db'):
    conn = create_connection(db)
    cur = conn.cursor()
    cur.execute("DELETE FROM card WHERE number=?", (number,))
    conn.commit()
    print('The account has been closed!')
    print()
    exit['quit'] = False


def transfer(number, db='card.s3db'):
    print('Transfer')
    transfer_card_number = input('Enter card number:')
    if number == transfer_card_number:
        print("You can't transfer money to the same account!")
    elif len(transfer_card_number) != 16:
        print('Such a card does not exist')
    elif luhn_algorithm_check(transfer_card_number):
        print("Probably you made mistake in the card number. Please try again!")
    elif if_number_exist(transfer_card_number):
        print('Such a card does not exist')

    else:
        transfer_money = int(input('Enter how much money you want to transfer:'))
        conn = create_connection(db)
        cur = conn.cursor()
        from_balance = int(get_balance_from_database(number))
        to_balance = int(get_balance_from_database(transfer_card_number))
        if from_balance < transfer_money:
            print('Not enough money!')
        else:
            from_balance -= transfer_money
            to_balance += transfer_money
            transaction(number, from_balance)
            transaction(transfer_card_number, to_balance)
            print('Success!')


def transaction(number, money, db='card.s3db'):
    conn = create_connection(db)
    cur = conn.cursor()
    cur.execute("UPDATE card SET balance = ?  WHERE number=?", (money, number))
    conn.commit()


def get_balance_from_database(number, db='card.s3db'):
    conn = create_connection(db)
    cur = conn.cursor()
    cur.execute("SELECT balance FROM card WHERE number=?", (number,))
    balance_set = cur.fetchone()
    balance = balance_set[0]
    print(f'Balance: {balance}')
    print()
    return balance


def if_number_exist(number, db='card.s3db'):
    conn = create_connection(db)
    cur = conn.cursor()
    cur.execute("SELECT balance FROM card WHERE number=?", (number,))
    balance_set = cur.fetchone()
    if balance_set:
        return False
    return True


def add_income(number, db='card.s3db'):
    income = input('Enter income:')
    conn = create_connection(db)
    cur = conn.cursor()
    cur.execute("UPDATE card SET balance = balance + ?  WHERE number=?", (income, number))
    conn.commit()
    print('Income was added!')


while exit['exit']:
    state_of_bank_system()
