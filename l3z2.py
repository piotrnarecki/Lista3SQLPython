from datetime import datetime
from datetime import datetime as datetime2
import mysql
from pip._vendor.distlib.compat import raw_input


def get_db(user, password):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user=user,
        password=password
    )
    return mydb


def print_db(mydb):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM dostawy.przesylki;")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)


def add_parcel(mydb):
    print('send the parcel')
    sender = str(raw_input('enter sender name '))
    date = str(datetime.today().strftime('%Y-%m-%d'))
    city = str(raw_input('enter city of delivery '))

    if sender.isdigit():
        print('name can not be a number')
    elif city.isdigit():
        print('city can not be a number')
    else:
        print(sender)
        print(date)
        print(city)

        mycursor = mydb.cursor()

        sql = "INSERT INTO dostawy.przesylki (Nadawca,DataNadania, MiastoDostarczenia, Kurier, DataDostarczenia) VALUES (" \
              "%s, %s, %s,%s, %s) "
        val = (sender, date, city, None, None)

        try:
            try:
                mycursor.execute(sql, val)
                mydb.commit()

                print(mycursor.rowcount, "record inserted.")
            except mysql.connector.errors.IntegrityError:  # sprawdza czy foreign key istnieje
                print("Cannot add this thing to DB")
        except mysql.connector.errors.DatabaseError:  # sprawdza czy dodawane wartosci sa wlasciwego typu
            print("Wrong values")

        mycursor.close


def find_couriers_from_city(mydb, city):
    mycursor = mydb.cursor()
    sql = "SELECT KurierID FROM dostawy.kurierzy WHERE CzyDostepny = 1 AND Miasto = %s;"
    mycursor.execute(sql, city)
    myresult = mycursor.fetchone()

    if myresult is None:
        print("there is no courier in this city")
    else:
        courierid = myresult[0]
        return courierid


def add_courier_to_parcels(mydb):
    mycursor = mydb.cursor()

    sql = "SELECT PrzesylkaId FROM dostawy.przesylki WHERE Kurier IS  NULL;"

    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    if myresult is None:
        print("all parcels have courier")
    else:
        for parcelID in myresult:

            sql = "SELECT MiastoDostarczenia FROM dostawy.przesylki WHERE PrzesylkaID = %s;"
            id = parcelID[0]
            mycursor.execute(sql, (id,))
            city = mycursor.fetchone()

            courierID = find_couriers_from_city(mydb, city)

            if courierID is None:
                print("there is no couriers in this city")
            else:

                sql = "UPDATE dostawy.przesylki SET Kurier = %s  WHERE PrzesylkaID = %s ;"
                values = (courierID, id)
                mycursor.execute(sql, values)

                print(courierID)

                sql = "UPDATE dostawy.kurierzy SET CzyDostepny = false  WHERE KurierID = %s ;"
                mycursor.execute(sql, (courierID,))

                mydb.commit()
                print("courier added to parcel")

    mycursor.close()


def confirm_pickup(mydb):
    import datetime

    print("confirm pickup ")
    parcel_id = str(raw_input('enter parcel id '))

    if parcel_id.isdigit():
        print(parcel_id)

        mycursor = mydb.cursor()

        sql = "SELECT * FROM dostawy.przesylki WHERE PrzesylkaID = %s AND Kurier IS NOT NULL ;"

        mycursor.execute(sql, (parcel_id,))

        myresult = mycursor.fetchone()

        mycursor.close

        if myresult is None:
            print('there is no parcel with id ' + parcel_id)
        else:
            shipment_date = myresult[2]
            print(shipment_date)

            pickup_date = myresult[5]
            if pickup_date is None:
                today = str(datetime2.today().strftime('%Y-%m-%d'))
                pickup_date = datetime2.strptime(today, '%Y-%m-%d').date()

                print(pickup_date)

                time_between = pickup_date - shipment_date
                print(time_between)
                if time_between > datetime.timedelta(days=1):  # sprawdza czy paczka zostala wyslana przed odbiorem
                    pickup_date = str(pickup_date)
                    mycursor = mydb.cursor()

                    sql = "UPDATE dostawy.przesylki SET DataDostarczenia = %s  WHERE PrzesylkaID = %s;"
                    mycursor.execute(sql, (pickup_date, parcel_id))

                    mydb.commit()

                    print('pickup confirmed')

                else:
                    print("pickup date should be after shipment date")


            else:
                print('the parcel has been delivered on ' + str(pickup_date))


    else:
        print('parcel id is a number')


def check_status(mydb):
    print("check parcel status")
    parcel_id = str(raw_input('enter parcel id '))

    if parcel_id.isdigit():

        mycursor = mydb.cursor()

        sql = "SELECT * FROM dostawy.przesylki WHERE PrzesylkaID = %s"

        mycursor.execute(sql, (parcel_id,))

        myresult = mycursor.fetchone()

        mycursor.close

        if myresult is None:
            print('there is no parcel with id ' + parcel_id)
        else:
            print(myresult)

            parcel_id = myresult[0]
            sender = myresult[1]
            shipment_date = myresult[2]
            city = myresult[3]
            courier_id = myresult[4]
            pickup_date = myresult[5]

            # istnieje
            if (parcel_id is not None) & (courier_id is None):
                print('parcel with id ' + str(parcel_id) + " exist")

            # nadana
            if (shipment_date is not None) & (courier_id is not None) & (pickup_date is None):
                print('parcel with id ' + str(parcel_id) + ' posted')

            # dostarczona
            if (shipment_date is not None) & (courier_id is not None) & (pickup_date is not None):
                print('parcel with id ' + str(parcel_id) + ' has been delivered')


    else:
        print('parcel id is a number')


def filter_by_sender(mydb):
    name = str(raw_input('enter sender name '))

    if name.isdigit():
        print('name cannot be a number')
    else:
        try:
            mycursor = mydb.cursor()

            sql = "SELECT * FROM dostawy.przesylki WHERE Nadawca = %s"

            mycursor.execute(sql, (name,))

            myresult = mycursor.fetchall()

            mycursor.close

            if len(myresult) > 0:
                print('there is ' + str(len(myresult)) + ' result(s):')

                for result in myresult:
                    print(result)

            else:
                print('there is no parcels with sender ' + name)


        except mysql.connector.errors.DatabaseError:
            print('DB problem')


def filter_by_city(mydb):
    city = str(raw_input('enter city '))

    if city.isdigit():
        print('city cannot be a number')
    else:
        try:
            mycursor = mydb.cursor()

            sql = "SELECT * FROM dostawy.przesylki WHERE MiastoDostarczenia = %s"

            mycursor.execute(sql, (city,))

            myresult = mycursor.fetchall()

            mycursor.close

            if len(myresult) > 0:
                print('there is ' + str(len(myresult)) + ' result(s):')

                for result in myresult:
                    print(result)

            else:
                print('there is no parcels for ' + city)


        except mysql.connector.errors.DatabaseError:
            print('DB problem')


def filter_by_shipment_date(mydb):
    date = str(raw_input('enter shipment date YYYY-MM-DD '))

    try:

        shipment_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")

        try:
            mycursor = mydb.cursor()

            sql = "SELECT * FROM dostawy.przesylki WHERE DataNadania >= %s"

            mycursor.execute(sql, (shipment_date,))

            myresult = mycursor.fetchall()

            mycursor.close

            if len(myresult) > 0:
                print('there is ' + str(len(myresult)) + ' result(s):')

                for result in myresult:
                    print(result)

            else:
                print('there is no parcels posted after ' + shipment_date)


        except mysql.connector.errors.DatabaseError:
            print('DB problem')

    except ValueError:
        print('wrong date')
        print('correct format  YYYY-MM-DD')


def filter_parcels(mydb):
    print('filter parcels by')
    print('1 - sender')
    print('2 - city')
    print('3 - shipment date')

    try:
        mode = int(raw_input('enter mode '))

        if mode == 1:
            filter_by_sender(mydb)
        elif mode == 2:
            filter_by_city(mydb)
        elif mode == 3:
            filter_by_shipment_date(mydb)
        else:
            print('mode is an integer between 1 and 3')

    except ValueError:
        print('mode should be a integer')


def main():
    import mysql.connector

    mydb = get_db("root", "password")

    # dodawanie przesylki
    # add_parcel(mydb)

    # przydzielanie kurierow do przesylek
    # add_courier_to_parcels(mydb)

    # potwierdzanie odbioru
    # confirm_pickup(mydb)

    # sprawdzanie statusu przesyłki
    # check_status(mydb)

    # filtrowanie
    filter_parcels(mydb)


if __name__ == '__main__':
    main()
