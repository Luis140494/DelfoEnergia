from etl_script import fetch_data_from_api
from dagster import resource, op, job, schedule
from sqlalchemy.ext.asyncio import create_async_engine
from core.configs import settings
from datetime import date 

@resource
def postgres_fonte_resource():
    return create_async_engine(settings.DB_URL_FONTE)

@resource
def postgres_alvo_resource():
    return create_async_engine(settings.DB_URL_ALVO)

@op(required_resource_keys={"postgres_fonte", "postgres_alvo"})
def extract_transform_load(context, start_date: date, end_date: date):
    return

@job
def etl_job():
    start_date = date(2024, 11, 5)
    end_date = date(2024, 11, 7)
    extract_transform_load(start_date=start_date, end_date=end_date)

@schedule(cron_schedule="0 0 * * *", job=etl_job)
def daily_etl_schedule():
    return {}
