from collections import defaultdict as DD
import csv
import datetime as dt
from pathlib import Path
from .settings import RESULT_DIR


BASE_DIR = Path(__file__).parent.parent

FIELDS_NAME = ('Статус', 'Количество')
DT_FORMAT = '%Y-%m-%dT%H-%M-%S'
FILE_NAME = 'status_summary_{time}.csv'


class PepParsePipeline:
    def open_spider(self, spider):
        self.results = DD(int)
        self.result_dir = BASE_DIR / RESULT_DIR
        self.result_dir.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        pep_status = item['status']
        if self.results.get(pep_status):
            self.results[pep_status] += 1
        else:
            self.results[pep_status] = 1
        return item

    def close_spider(self, spider):
        file_dir = self.result_dir / FILE_NAME.format(
            time=dt.datetime.now().strftime(DT_FORMAT))
        with open(file_dir, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerow(FIELDS_NAME)
            for key, val in self.results.items():
                writer.writerow([key, val])
            writer.writerow(['Total', sum(self.results.values())])
