from langchain_core.tools import tool
from database import get_connection


@tool
def get_order_items(order_id: str) -> str:
    """
    Get the products, quantities, and prices included in a customer order.
    """


    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            p.product_name,
            oi.quantity,
            oi.unit_price
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        WHERE oi.order_id = %s
        """

        cursor.execute(query, (order_id,))

        items = cursor.fetchall()

        if not items:
            return f"No items were found for order {order_id}."

        result = []

        for item in items:
            result.append(
                f"{item['product_name']} "
                f"(Quantity: {item['quantity']}, "
                f"Unit price: ₹{item['unit_price']})"
            )

        return "\n".join(result)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":

    result = get_order_items.invoke({
        "order_id": "ORD1001"
    })

    print(result)