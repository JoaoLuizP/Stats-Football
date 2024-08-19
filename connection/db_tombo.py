import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles.fills import PatternFill
from openpyxl.styles import Font
import time
import math
import PySimpleGUI as sg
from numpy import random
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

data_do_dia = datetime.today().strftime('%d-%m-%Y')
local_db = psycopg2.connect(
    user="postgres",
    password="Santos010802.2311",
    host="woefully-hot-vulture.data-1.use1.tembo.io",
    port="5432",
    database="postgres")
engine_local = create_engine('postgresql://postgres:Santos010802.2311@woefully-hot-vulture.data-1.use1.tembo.io:5432')


teste = pd.read_sql_table("tbl_teste", con=engine_local, schema="tembo")

df = pd.DataFrame(teste)

print(f'\n\n{df}')

