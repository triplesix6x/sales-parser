from .celery_app import celery_app
from core.config import settings
from asgiref.sync import async_to_sync
from core.celery.utils.openai import generate_financial_report
from core.celery.utils.xml_parser import parse_sales_xml
from core.celery.utils.web import fetch_xml, post_request, patch_request
import logging


logger = logging.getLogger(__name__)

FASTAPI_URL = "http://api:" + str(settings.run.port)


@celery_app.task
def process_sales_data():
    async_to_sync(_process_sales_data)()


async def _process_sales_data():
    logger.info("Starting process_sales_data task")
    xml_url = settings.xml.url

    xml_data = await fetch_xml(xml_url)
    if not xml_data:
        logger.error("Failed to fetch XML data")
        return

    try:
        sales_data = parse_sales_xml(xml_data)
    except Exception as e:
        logger.error(f"Error parsing XML: {e}")
        return

    try:
        sale = await post_request(f"{FASTAPI_URL}/v1/sales/", json={
            "date": str(sales_data["sale"]["date"])
        })
        sale_id = sale["id"]
    except Exception as e:
        logger.error(f"Error creating Sale: {e}")
        return

    try:
        for product in sales_data["products"]:
            await post_request(f"{FASTAPI_URL}/v1/products/", json={
                "name": product["name"],
                "quantity": product["quantity"],
                "price": product["price"],
                "category": product["category"],
                "sale_id": sale_id
            })
    except Exception as e:
        logger.error(f"Error creating Products: {e}")
        return

    try:
        report = generate_financial_report(sales_data)
        await patch_request(f"{FASTAPI_URL}/v1/sales/{sale_id}/", json={
            "report": report
        })
    except Exception as e:
        logger.error(f"Error updating Sale with report: {e}")
        return

    logger.info("process_sales_data task completed successfully")
