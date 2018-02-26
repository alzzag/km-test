import xlwt
from django.shortcuts import render
from .models import Client
from datetime import datetime
from django.http import HttpResponse
from cBase.tasks import exportExcel
import json

def poll_for_download(request):
	task_id = request.GET.get('task_id', '')
	result = exportExcel.AsyncResult(task_id)
	# Вопрос 2: Зачем в реализации остались закомментированные строки кода?
	#response = HttpResponse(content_type='application/json')
	if result.ready():
		#response.write(json.dumps({'filename': result.get()}))
		response = HttpResponse(json.dumps({"filename": result.get()}))
	else:
		#response.write(json.dumps({'filename': 'qwe'}))
		response = HttpResponse(json.dumps({"filename": None}))
	return response
    
def downloadExcel(request):
	task = exportExcel.delay()
	return render(request, 'cBase/downloading.html', {'task_id' : task.task_id})

def photos(request):
	
	if request.GET.get('cID', '') != '':
		c = Client.objects.get(pk=int(request.GET.get('cID', '')))
		if c.rating<10:
			# Вопрос 1: Что будет, если на сайте 2 кликнуть на + при уже
			# установленном значении счетчика 9?
			from random import randint
			from time import sleep
			sleep(randint(4, 10))
			Client.objects.filter(id=int(request.GET.get('cID', ''))).update(rating=c.rating+1)
	
	clients = Client.objects.all()
	return 	render(request, 'cBase/photos.html', {'clients' : clients})

def client_list(request):
	clients = Client.objects.filter(name__contains=request.GET.get('filter_name', ''), surname__contains=request.GET.get('filter_sname', ''))
	filter_params = '&filter_name='+request.GET.get('filter_name', '')+'&filter_sname='+request.GET.get('filter_sname', '')
	
	name_href = '?orderby=name&order=asc'+filter_params
	sname_href = '?orderby=sname&order=asc'+filter_params
	bday_href = '?orderby=bday&order=asc'+filter_params
	
	if request.GET.get('orderby', '') == 'name':
		if request.GET.get('order', '') == 'asc':
			name_href = '?orderby=name&order=desc'+filter_params
			clients = clients.order_by('name')
		else:
			name_href = '?orderby=name&order=asc'+filter_params
			clients = clients.order_by('-name')
	elif request.GET.get('orderby', '') == 'sname':
		if request.GET.get('order', '') == 'asc':
			sname_href = '?orderby=sname&order=desc'+filter_params
			clients = clients.order_by('surname')
		else:
			sname_href = '?orderby=sname&order=asc'+filter_params
			clients = clients.order_by('-surname')			
	elif request.GET.get('orderby', '') == 'bday':
		if request.GET.get('order', '') == 'asc':
			bday_href = '?orderby=bday&order=desc'+filter_params
			clients = clients.order_by('-birthday')			
		else:
			bday_href = '?orderby=bday&order=asc'+filter_params
			clients = clients.order_by('birthday')			
		
		
		
	

	
	now = datetime.date(datetime.today())
	for client in clients:
		client.age = now.year - client.birthday.year
		if (now.month<client.birthday.month) or ((now.month==client.birthday.month) and (now.day<client.birthday.day)):
			client.age = client.age - 1
	return 	render(request, 'cBase/client_list.html', {'clients' : clients,
							'name_href' : name_href,
							'sname_href' : sname_href,
							'bday_href' : bday_href})

def export_excel(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="ClientList.xls"'

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
	
	wb.save(response)
	return response