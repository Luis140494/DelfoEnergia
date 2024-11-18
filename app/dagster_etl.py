from dagster import job, op, ScheduleDefinition
import datetime
from etl_script import fetch_data_from_api, process_and_insert_data

# Operações do pipeline
@op
async def extract_data():
    # Definir a data de extração, exemplo: ontem
    start_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return await fetch_data_from_api(start_date, end_date, ['wind_speed', 'power'])

@op
async def transform_and_load(data):
    await process_and_insert_data(data)

@job
def etl_job():
    data = extract_data()
    transform_and_load(data)

# Agendar o job para rodar diariamente
schedule = ScheduleDefinition(
    job=etl_job,
    cron_schedule="* * * * *", 
)