from database.DB_connect import DBConnect
from model.category import Category
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCategory():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.category_id as id, c.category_name as nome
                    from categories c """

        cursor.execute(query)

        for row in cursor:
            results.append(Category(row["id"], row["nome"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(idCategory):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from products p 
                    where p.category_id = %s """

        cursor.execute(query, (idCategory,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(dataI, dataF):

        conn = DBConnect.get_connection()

        listaIdP = []
        listaPV = []

        cursor = conn.cursor(dictionary=True)
        query = """select oi.product_id as id, count(*) as numeroOrdini
                    from order_items oi, orders o 
                    where oi.order_id = o.order_id 
                    and o.order_date between %s and %s
                    group by oi.product_id 
                    having count(*) >= 1"""

        cursor.execute(query, (dataI, dataF))

        for row in cursor:
            listaIdP.append(row["id"])
            listaPV.append((row["id"], row["numeroOrdini"]))

        cursor.close()
        conn.close()
        return listaIdP, listaPV

