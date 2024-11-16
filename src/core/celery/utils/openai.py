from openai import OpenAI
from typing import Dict
from core.config import settings


client = OpenAI(
    api_key=settings.openai.api)


def generate_financial_report(sales_data: Dict):
    sale_date = sales_data['sale']['date']
    products = sales_data['products']

    total_revenue = sum(p['quantity'] * p['price'] for p in products)
    top_products = sorted(products, key=lambda x: x['quantity'], reverse=True)[:3]
    categories = {}
    for p in products:
        categories[p['category']] = categories.get(p['category'], 0) + p['quantity']

    total_units_sold = sum(p['quantity'] for p in products)
    average_sale_price = total_revenue / total_units_sold if total_units_sold else 0

    top_products_str = ', '.join([p['name'] for p in top_products])
    categories_str = ', '.join([f"{k}: {v}" for k, v in categories.items()])

    prompt = f"""
        Проанализируй данные о продажах за {sale_date}:
        1. Общая выручка: {total_revenue}
        2. Топ-3 товара по продажам: {top_products_str}
        3. Распределение по категориям: {categories_str}
        4. Общее количество проданных единиц: {total_units_sold}
        5. Средняя цена за единицу: {average_sale_price:.2f}

        Составь подробный аналитический отчет с выводами и рекомендациями.
        """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты помощник для генерации финансовых отчетов."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.7,
    )
    report = response["choices"][0]["message"]["content"].strip()
    return report
