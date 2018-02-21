from celery.decorators import task
from settings import MEDIA_ROOT, MEDIA_URL
import os
import xlwt
from .models import Client
from datetime import datetime

@task(name="exportExcel")
def exportExcel():
	fn = 0
	while (str(fn)+'.xls') in os.listdir(MEDIA_ROOT+'/download/'):
		fn = fn+1
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Список клиентов')
	ws.col(0).width = 6000
	ws.col(1).width = 5000
	ws.col(2).width = 4000

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Фамилия', 'Имя', 'Дата рождения']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
	ws.write(row_num, col_num+1, 'Возраст', font_style)
	
	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()
	date_style = xlwt.Style.easyxf(num_format_str='DD.MM.YYYY')
	now = datetime.date(datetime.today())
	
	
	rows = Client.objects.all().values_list('surname', 'name', 'birthday')
	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			if (col_num==2):
				ws.write(row_num, col_num, row[col_num], date_style)
			else:
				ws.write(row_num, col_num, row[col_num], font_style)
		#возраст	
		cBD = row[col_num]
		cAGE = now.year - cBD.year
		if (now.month<cBD.month) or ((now.month==cBD.month) and (now.day<cBD.day)):
			cAGE = cAGE - 1
		ws.write(row_num, col_num+1, cAGE, font_style)
	
	wb.save(MEDIA_ROOT+'/download/'+str(fn)+'.xls')
	return str(fn)+'.xls'