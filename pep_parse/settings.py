from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
ALLOWED_DOMAINS = "peps.python.org"
PEP_NAME_PATTERN = r"PEP (?P<pep_number>\d+) – (?P<pep_name>.*)"
TIME_FORMAT = "%Y-%m-%dT%H-%M-%S"
RESULT_DIR = "results"
FILE_FORMAT = "csv"


BOT_NAME = "pep_parse"
NEWSPIDER_MODULE = "pep_parse.spiders"
SPIDER_MODULES = ["pep_parse.spiders"]
ROBOTSTXT_OBEY = False
FEEDS = {
    f"results/pep_%(time)s.{FILE_FORMAT}": {
        "format": FILE_FORMAT,
        "fields": ["number", "name", "status"],
        "overwrite": True,
    }
}
ITEM_PIPELINES = {
    "pep_parse.pipelines.PepParsePipeline": 300,
}
