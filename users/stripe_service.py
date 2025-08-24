import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name, description=None):
    if not description:
        description = "РћРїРёСЃР°РЅРёРµ РЅРµРґРѕСЃС‚СѓРїРЅРѕ"
    return stripe.Product.create(name=name, description=description)


def create_stripe_price(product_id: str, amount: int, currency: str = "usd") -> str:
    price = stripe.Price.create(
        unit_amount=amount, currency=currency, product=product_id
    )
    return price.id


def create_checkout_session(price_id: str, success_url: str, cancel_url: str) -> str:
    session = stripe.checkout.Session.create(
        success_url=success_url,
        cancel_url=cancel_url,
        mode="payment",
        line_items=[{"price": price_id, "quantity": 1}],
    )
    return session.url
