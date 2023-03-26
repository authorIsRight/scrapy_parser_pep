import csv
from pathlib import Path
from datetime import datetime

from itemadapter import ItemAdapter

BASE_DIR = Path(__file__).parent.parent

NOW_TIME = datetime.strftime(datetime.now(), '%Y-%m-%dT%H-%M-%S')


class PepParsePipeline:
    def open_spider(self, spider):
        self.statuses = {}

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('status'):
            pep_status = adapter['status']
            self.statuses[pep_status] = (
                self.statuses.get(pep_status, 0) + 1
            )
            return item

    def close_spider(self, spider):
        RESULT_DIR = BASE_DIR / 'results'
        filename = "status_summary_" + NOW_TIME + ".csv"
        with open(RESULT_DIR / filename, newline='',
                  mode='w', encoding='utf-8') as f:
            csv.writer(f,).writerows(
                (("Статус", "Колличество"),
                    *self.statuses.items(),
                    ("Total", sum(self.statuses.values())))
            )
