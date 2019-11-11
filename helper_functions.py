from question_summary import *
from user import *


def find_and_populate(parser, html_tag, label, class_name):
    collection = []
    klass = globals()[class_name]
    matches = parser.get_matches(html_tag, label)
    for match in matches:
        item = klass(parser)
        item.scrape_info(match)
        collection.append(item)
    return collection
