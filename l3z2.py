import mysql
from _mysql_connector import MySQLInterfaceError


def print_db(mydb):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM dostawy.przesylki;")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)


def add_parcel(mydb):
    mycursor = mydb.cursor()

    sql = "INSERT INTO dostawy.przesylki (Nadawca,DataNadania, MiastoDostarczenia, Kurier, DataDostarczenia) VALUES (" \
          "%s, %s, %s,%s, %s) "
    val = ("Andrzej Testowy", "2021-04-20", "Wroclaw", "55", "2021-04-27")

    try:
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except mysql.connector.errors.IntegrityError:  # sprawdza czy foreign key istnieje
            print("Cannot add this thing to DB")
    except mysql.connector.errors.DatabaseError:  # sprawdza czy dodawane wartosci sa wlasciwego typu
        print("Wrong values")


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
        print("All parcels have courier")
    else:
        for parcelID in myresult:

            sql = "SELECT MiastoDostarczenia FROM dostawy.przesylki WHERE PrzesylkaID = %s;"
            id = parcelID[0]
            mycursor.execute(sql, (id,))
            city = mycursor.fetchone()

            courierID = find_couriers_from_city(mydb, city)

            if courierID is None:
                print("cannot add courier to this parcel")
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
    print("pickup confrimed")

def main():
    import mysql.connector

    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="password"
    )

    # addParcel(mydb)

    # printDB(mydb)

    # find_couriers_from_city(mydb, city)

    #add_courier_to_parcels(mydb)

    confirm_pickup(mydb)

if __name__ == '__main__':
    main()
