from core.models import Product


def product_to_dict(product: Product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "quantity": product.quantity,
        "price": product.price,
        "category": product.category,
        "sale_id": product.sale_id
    }


def product_from_dict(data: dict) -> Product:
    return Product(
        id=data["id"],
        name=data["name"],
        quantity=data["quantity"],
        price=data["price"],
        category=data["category"],
        sale_id=data["sale_id"]
    )
