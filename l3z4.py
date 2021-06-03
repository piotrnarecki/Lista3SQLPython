from datetime import datetime
from datetime import datetime as datetime2
import mysql
from pip._vendor.distlib.compat import raw_input


def get_db(user, password):
    mydb = None
    try:
        try:
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user=user,
                password=password
            )
        except AttributeError:
            print('wrong user')
    except mysql.connector.errors.ProgrammingError:
        print('wrong password')

    return mydb


# sprawdza czy mozna dokonac zamowienia
def can_order(mydb, product_id, quantity):
    stock_quantity = 0
    order_quantity = 0

    # w magazynie
    mycursor = mydb.cursor()

    sql = "SELECT Nazwa,StanMagazywnowy FROM sprzedaz.produkty WHERE ProduktID = %s;"
    mycursor.execute(sql, (product_id,))

    myresult1 = mycursor.fetchone()
    if myresult1 is not None:
        product_name = myresult1[0]
        print('product: ' + product_name)
        stock_quantity = int(myresult1[1])
        print('quantity in stock: ' + str(stock_quantity))
    else:
        print('there is no product with id ' + str(product_id))

    mycursor.close()

    # w zamowieniach
    mycursor = mydb.cursor()

    sql = "SELECT SUM(Ilosc) FROM sprzedaz.zamowieniaprodukty WHERE NrProduktu = %s;"
    mycursor.execute(sql, (product_id,))

    myresult2 = mycursor.fetchone()

    if myresult2 is not None:

        try:
            order_quantity = int(myresult2[0])
            print('quantity in orders: ' + str(order_quantity))
        except TypeError:
            print('currently there is no product with id ' + str(product_id) + ' in orders')

    else:
        print('there is no product with id ' + str(product_id))

    mycursor.close()

    quantity_for_sale = stock_quantity - order_quantity
    print(str(quantity_for_sale) + ' ' + product_name + ' left')

    if quantity_for_sale >= quantity:
        print('you can order this')
        return True
    else:

        print('you cannot order. there is only ' + str(quantity_for_sale) + ' left')
        return False


def get_order_id(mydb, name):
    print(name)

    mycursor = mydb.cursor()

    sql = "SELECT ZamowienieID FROM sprzedaz.zamowienia WHERE Odbiorca=%s ; "

    mycursor.execute(sql, (name,))
    myresult = mycursor.fetchone()

    mycursor.close()
    order_id = int(myresult[0])
    return order_id


def confirm_order(mydb, order_number, product_id, quantity):
    # zamowieniaprodukty
    mycursor = mydb.cursor()

    sql = "INSERT INTO sprzedaz.zamowieniaprodukty (NrZamowienia,NrProduktu,Ilosc) VALUES (" \
          "%s,%s,%s) "
    val = (order_number, product_id, quantity)

    try:
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()
            print('order confirmed')

        except mysql.connector.errors.IntegrityError:  # sprawdza czy foreign key istnieje
            print("cannot add this thing to DB")
    except mysql.connector.errors.DatabaseError:  # sprawdza czy dodawane wartosci sa wlasciwego typu
        print("wrong values")

    mycursor.close


def prepare_order(mydb, product_name, quantity):
    # sprawdz czy produkt istnieje i czy jest na stanie
    mycursor = mydb.cursor()

    sql = "SELECT * FROM sprzedaz.produkty WHERE Nazwa = %s;"
    mycursor.execute(sql, (product_name,))

    myresult = mycursor.fetchone()
    mycursor.close()

    try:

        product_id = int(myresult[0])
        if can_order(mydb, product_id, quantity):

            name = str(raw_input('enter reciver name '))
            if name.isdigit():
                print('name cannot be a number')
            else:

                # zamownienia
                mycursor = mydb.cursor()

                sql = "INSERT INTO sprzedaz.zamowienia (Odbiorca) VALUES (" \
                      "%s) "
                val = (name,)

                try:
                    try:
                        mycursor.execute(sql, val)
                        mydb.commit()
                        mycursor.close()
                        print(mycursor.rowcount, "record inserted.")

                        order_id = get_order_id(mydb, name)

                        if order_id is not None:
                            confirm_order(mydb, order_id, product_id, quantity)
                        else:
                            print('cannot find order id')


                    except mysql.connector.errors.IntegrityError:  # sprawdza czy foreign key istnieje
                        print("cannot add this thing to DB")
                except mysql.connector.errors.DatabaseError:  # sprawdza czy dodawane wartosci sa wlasciwego typu
                    print("wrong values")

                mycursor.close



    except TypeError:
        print('there is no product with name ' + product_name)


def add_order(mydb):
    print('add new order')

    try:
        # order_number = int(raw_input('enter order number '))
        # w bazie danych numer zamowienia mam ustawiony na Auto Increment, nie ma poreby podawania go tutaj

        product_name = str(raw_input('enter product name '))
        if product_name.isdigit():
            print('product name is not a number')
        else:
            try:
                quantity = int(raw_input('enter quantity '))

                print(product_name)
                print(quantity)

                prepare_order(mydb, product_name, quantity)



            except ValueError:
                print('quantity should be a number')

    except ValueError:
        print('order number should be a number')


def print_db(mydb):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM sprzedaz.zamowienia;")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)


def main():
    import mysql.connector

    mydb = get_db("root", "password")

    # dodawanie zamówienia
    add_order(mydb)


if __name__ == '__main__':
    main()
