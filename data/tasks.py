import csv

from celery_progress.backend import ProgressRecorder
import random


from django.core.files.storage import default_storage

from data.fake_data import generate_csv
from data.models import Data, DataFile, DataStatusChoises
from core.celery import app

@app.task(bind=True)
def create_csv(self, task_id, rows):
    """Create csv file with generated data and save it to db"""
    schema = Data.objects.get(id=task_id)
    number = random.randint(1, 999999)
    progress_recorder = ProgressRecorder(self)
    schema_file = DataFile.objects.create(
        status=DataStatusChoises.PROCESSING, schema=schema)

    try:
        columns = [
            column for column in schema.column_in_data.all().order_by("order")
        ]
        filename = f"/data-{schema.id}--{number}.csv"

        with default_storage.open(filename, "w") as csv_file:
            csv_file.truncate()
            writer = csv.writer(csv_file,
                                delimiter=schema.separator)
            writer.writerow([column.name for column in columns])

            for i in range(rows):
                row_to_write = []
                for column in columns:
                    row_to_write.append(
                        " ".join(generate_csv(column.id).split()))
                writer.writerow(row_to_write)

                progress_recorder.set_progress(i, rows,
                                               description="Generating")

                self.update_state(state='PROGRESS',
                                  meta={'current': i, 'total': rows})

        # updating model instance
        schema_file.file = filename
        schema_file.status = DataStatusChoises.READY
        schema_file.save()
        return 'Done'

    except Exception as ex:
        print(ex)
        schema.schema_files.create(file='', status=DataStatusChoises.FAILED)
        return 'Failed'
    finally:
        schema.save()


