import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
sys.path.append('H:\\web-bao-cao')
from database import process_repeated_tickets_excel

process_repeated_tickets_excel("H:\\web-bao-cao\\downloads\\SM1_C12_20260812_094906.xlsx", "2026-08-12")
