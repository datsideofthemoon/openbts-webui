# Copyright (C) 2012 Daniil Egorov <datsideofthemoon@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from webgui.models import Parameter
from django.db import connection, transaction
from django.shortcuts import render_to_response
import socket
from django.http import HttpResponseNotFound

class StatusSection:
	def __init__(self,fcname,fres):
		self.name=fcname
		self.text=fres
class Section:
	def __init__(self,fname,fparamlist):
		self.name = fname
		self.paramlist = fparamlist

def main(request):
	if request.method == 'POST':
		cursor = connection.cursor()
		for key, value in request.POST.iteritems():
			if value=="[NULL]" :
				cursor.execute("UPDATE CONFIG SET VALUESTRING = null WHERE KEYSTRING = %s", [key])
			else:
				cursor.execute("UPDATE CONFIG SET VALUESTRING = %s WHERE KEYSTRING = %s", [value,key])
			transaction.commit_unless_managed()
	table=Parameter.objects.all() 
	datalist=[]
	for section in settings.MAIN_SECTIONS:
		section_name=section[0] #section name
		paramlist=section[1]	#parameters
		nameslist=section[2]	#parameters names
		tempparams=[]
		for idx, param in enumerate(paramlist):
			for row in table:
				if row.keystring == param:
					tempparams.append([row.keystring,nameslist[idx],row.valuestring,row.comments])
					break
		datalist.append(Section(section_name,tempparams))
	return render_to_response('main.html', {
		'mastername': "OpenBTS",
		'pagename': "Main",
		'sectionlist': datalist,
		})

def advanced(request):
	if request.method == 'POST':
		cursor = connection.cursor()
		for key, value in request.POST.iteritems():
			if value=="[NULL]" :
				cursor.execute("UPDATE CONFIG SET VALUESTRING = null WHERE KEYSTRING = %s", [key])
			else:
				cursor.execute("UPDATE CONFIG SET VALUESTRING = %s WHERE KEYSTRING = %s", [value,key])
			transaction.commit_unless_managed()
	table=Parameter.objects.all() 
	datalist=[]
	for prefix in settings.ADV_PREFIXES:
		tempparams=[]
		for row in table:
			if row.keystring.startswith(prefix): #find keystring in table by prefix
				tempparams.append(row) #append .parameter, .value, .comment to output list
		datalist.append(Section(prefix,tempparams))
	return render_to_response('advanced.html', {
	'mastername': "OpenBTS",
	'pagename': "Advanced",	
	'sectionlist': datalist,})

def get_cli_command(command):
	socketaddres=Parameter.objects.get(keystring="CLI.SocketPath")
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	try:
		s.connect(socketaddres.valuestring)
		s.send(command)
		data = s.recv(1024)
		s.close()
	except IOError as e:
		return e.strerror
	return data	
	
def status(request):
	resdata=[]
	commands=['alarms','calls','cellid','chans','load','power','tmsis']
	blocknames=['Alarms','Calls','Cell ID','Channels','Load','Power','TMSIs']
	for idx,val in enumerate(commands):
		res=get_cli_command(val)
		resdata.append(StatusSection(blocknames[idx],res))
	return render_to_response('status.html', {
		'mastername': "OpenBTS",
		'pagename': "Status",
		'datalist': resdata,
		})
		
def actions(request):
	return render_to_response('actions.html', {
		'mastername': "Actions",
		'pagename': "Actions",
		'itemlist': "actions",
		})
