import os
import sys
## default config
PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PARENT not in sys.path:
    sys.path.insert(0,PARENT)

import default_cfg

from .mongoquery import query_yahoo, query_wantTimes, query_news_by_oid
from .mongoquery import query_items


