from langchain_core.tools import tool
from database import get_connection


@tool
def check_order_status(order_id: str) -> str:
    """
    Check the current status of a customer order using its order ID.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT order_id, status, estimated_delivery
        FROM orders
        WHERE order_id = %s
        """

        cursor.execute(query, (order_id,))

        order = cursor.fetchone()

        if not order:
            return f"No order was found with order ID {order_id}."

        return (
            f"Order {order['order_id']} is currently "
            f"{order['status']}. "
            f"Estimated delivery: {order['estimated_delivery']}."
        )

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":

    result = check_order_status.invoke({
        "order_id": "ORD1001"
    })

    print(result)

