from collections import defaultdict
from django.db.models import Sum, Case, When, DecimalField
from django.db.models.functions import TruncMonth

from transactions.models import Transaction


def get_monthly_balance(user):
    """
    Devuelve el balance mensual del usuario.
    No conoce DRF, serializers ni Response.
    """

    monthly_qs = (
        Transaction.objects
        .filter(user=user)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(
            income=Sum(
                Case(
                    When(category__category_type="INCOME", then="amount"),
                    default=0,
                    output_field=DecimalField(),
                )
            ),
            expense=Sum(
                Case(
                    When(category__category_type="EXPENSE", then="amount"),
                    default=0,
                    output_field=DecimalField(),
                )
            ),
        )
        .order_by("-month")
    )

    expenses_by_category = (
        Transaction.objects
        .filter(
            user=user,
            category__category_type="EXPENSE"
        )
        .annotate(month=TruncMonth("created_at"))
        .values("month", "category__name")
        .annotate(total=Sum("amount"))
    )

    incomes_by_category = (
        Transaction.objects
        .filter(
            user=user,
            category__category_type="INCOME"
        )
        .annotate(month=TruncMonth("created_at"))
        .values("month", "category__name")
        .annotate(total=Sum("amount"))
    )

    categories_map = defaultdict(lambda: {
        "expenses": [],
        "incomes": []
    })

    for row in expenses_by_category:
        categories_map[row["month"]]["expenses"].append({
            "category": row["category__name"],
            "amount": row["total"]
        })

    for row in incomes_by_category:
        categories_map[row["month"]]["incomes"].append({
            "category": row["category__name"],
            "amount": row["total"]
        })

    for month_data in categories_map.values():
        month_data["expenses"].sort(key=lambda x: x["amount"], reverse=True)
        month_data["incomes"].sort(key=lambda x: x["amount"], reverse=True)

    result = []

    for row in monthly_qs:
        result.append({
            "month": row["month"],
            "income": row["income"],
            "expense": row["expense"],
            "expenses_by_category": categories_map[row["month"]]["expenses"],
            "incomes_by_category": categories_map[row["month"]]["incomes"],
        })

    return result
