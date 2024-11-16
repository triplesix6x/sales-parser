from datetime import datetime
from lxml import etree


def parse_sales_xml(xml_content):
    try:
        root = etree.fromstring(xml_content)
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML: {e}")
        print(f"XML content: {xml_content}")
        raise

    date_str = root.attrib.get('date')
    sale_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    products = []
    for product_elem in root.find('products').findall('product'):
        product = {
            "name": product_elem.find('name').text,
            "quantity": int(product_elem.find('quantity').text),
            "price": float(product_elem.find('price').text),
            "category": product_elem.find('category').text
        }
        products.append(product)

    sale_data = {
        "date": sale_date,
    }

    return {"sale": sale_data, "products": products}
