from typing import List

from django.db import transaction

import init_django_orm  # noqa: F401

from db.models import Order, Ticket


def create_order(tickets: List[dict]) -> Order:
    with transaction.atomic():
        order = Order.objects.create()

        for ticket_data in tickets:
            Ticket.objects.create(order=order, **ticket_data)

        return order


if __name__ == "__main__":
    create_order(
        tickets=[
            {
                "seat": 10,
                "trip_id": 1,
            },
            {
                "seat": 12,
                "trip_id": 1,
            },
            {
                "seat": 12,
                "trip_id": 1,
            },
        ]
    )
