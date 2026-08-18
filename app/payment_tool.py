from langchain_core.tools import tool
from database import get_connection


@tool
def get_payment_details(order_id: str) -> str:
    """
    Get the payment method, payment status, payment date,
    and payment amount for a customer order.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            payment_method,
            payment_status,
            payment_date,
            amount
        FROM payments
        WHERE order_id = %s
        """

        cursor.execute(query, (order_id,))

        payment = cursor.fetchone()

        if not payment:
            return f"No payment information was found for order {order_id}."

        return (
            f"Payment method: {payment['payment_method']}\n"
            f"Payment status: {payment['payment_status']}\n"
            f"Payment date: {payment['payment_date']}\n"
            f"Amount: ₹{payment['amount']}"
        )

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":

    result = get_payment_details.invoke({
        "order_id": "ORD1001"
    })

    print(result)