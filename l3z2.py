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
            city=mycursor.fetchone()


            #city=str(city)

            print(parcelID)
            print(city)

            print(type(city))




            courierID=find_couriers_from_city(mydb,city)
            print(courierID)

            city2=('Poznań',)
            print(type(city2))






            #
            # print(city)

            # courierID=find_couriers_from_city(mydb,city2)
            #
            #
            # print(courierID)

            #sql = "UPDATE dostawy.przesylki SET Kurier = %s  WHERE PrzesylkaID = %s ;"
            # mycursor.execute(sql,(),(id,))


    #
    # sql = "SELECT MiastoDostarczenia FROM dostawy.przesylki WHERE PrzesylkaID = %s;"
    # id = listOfParcels[0][1]
    # print(id)
    # mycursor.execute(sql, (id,))
    # myresult = mycursor.fetchone()
    # city = str(myresult[0])

    # sql = "UPDATE dostawy.przesylki SET Kurier = %s  WHERE PrzesylkaID = %s ;"
    #
    # city = (city,)
    #
    # mycursor.execute(sql, city)

    mycursor.close()



def find_couriers_from_city(mydb, city):
    print("typet")
    print(type(city))


    mycursor = mydb.cursor()

    sql = "SELECT KurierID FROM dostawy.kurierzy WHERE CzyDostepny = 1 AND Miasto = %s;"
    # city = (city,)

    mycursor.execute(sql, city)

    myresult = mycursor.fetchone()

    print(myresult[0])
    courierid = myresult[0]

    if myresult is None:
        print("there is no courier in this city")
    else:
        return courierid


def main():
    import mysql.connector

    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="password"
    )

    # printDB(mydb)
    #
    # addParcel(mydb)
    #
    # printDB(mydb)

    #city=("Opole",)
    #print(type(city))
    #find_couriers_from_city(mydb, city)

    add_courier_to_parcels(mydb)


if __name__ == '__main__':
    main()
