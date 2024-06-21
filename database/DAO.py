from database.DB_connect import DBConnect
from model.connessione import Connessione


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getProvider():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct ny.Provider as p
                        from nyc_wifi_hotspot_locations ny
                        order by ny.Provider """
            cursor.execute(query, )
            for row in cursor:
                result.append(row["p"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getLocations(provider):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct ny.Location as l
                        from nyc_wifi_hotspot_locations ny
                        where ny.Provider = %s
                        order by ny.Provider """
            cursor.execute(query, (provider,))
            for row in cursor:
                result.append(row["l"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getPosition(provider):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT  Location , AVG(Latitude) as Latitude, AVG(Longitude) as Longitude
                        FROM nyc_wifi_hotspot_locations nwhl 
                        WHERE Provider = %s
                        GROUP BY Location """
            cursor.execute(query, (provider,))
            for row in cursor:
                result.append(Connessione(**row))
            cursor.close()
            cnx.close()
        return result
