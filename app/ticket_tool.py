from langchain_core.tools import tool
from database import get_connection


@tool
def get_support_tickets(customer_id: str) -> str:
    """
    Get support tickets associated with a customer.
    Returns the ticket ID, issue type, description, status,
    and creation date.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            ticket_id,
            order_id,
            issue_type,
            description,
            status,
            created_at
        FROM support_tickets
        WHERE customer_id = %s
        ORDER BY created_at DESC
        """

        cursor.execute(query, (customer_id,))

        tickets = cursor.fetchall()

        if not tickets:
            return f"No support tickets were found for customer {customer_id}."

        result = []

        for ticket in tickets:
            result.append(
                f"Ticket ID: {ticket['ticket_id']}\n"
                f"Order ID: {ticket['order_id']}\n"
                f"Issue: {ticket['issue_type']}\n"
                f"Description: {ticket['description']}\n"
                f"Status: {ticket['status']}\n"
                f"Created: {ticket['created_at']}"
            )

        return "\n\n".join(result)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":

    result = get_support_tickets.invoke({
        "customer_id": "101"
    })

    print(result)