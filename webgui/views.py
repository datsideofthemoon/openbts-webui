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

import time, socket, os, re
from django.conf import settings
from webgui.models import Parameter, Dialdata
from django.db import connection, transaction
from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound

SOCKETNAME=''
SOCK = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

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
	global SOCKETNAME
	global SOCK
	if SOCKETNAME=='':
		SOCKETNAME="/tmp/OpenBTS.console.%d.%8lx" % (os.getpid(),time.time())
		try:
			SOCK.bind(SOCKETNAME)
		except Exception, e:
			return "Error: could not connect to OpenBTS." + ' bind: '+ str(e)
	socketaddres=Parameter.objects.get(keystring="CLI.SocketPath")	
	try:
		SOCK.sendto(command,socketaddres.valuestring)
	except Exception, e:
		return "Error: could not connect to OpenBTS." + ' sendto: '+ str(e)
	try:
		data = SOCK.recv(10000)
	except Exception, e:
		return "Error: could not connect to OpenBTS." + ' receive: '+ str(e)
	return data				#maybe close socket? delete tmp file?
	
def status(request):
	if request.method == 'POST':
		get_cli_command('tmsis clear')
	commands=['calls','cellid','chans','load','power','tmsis']
	alarms= None
	calls = None
	cellid= None
	chans = None
	load  = None
	power = None
	tmsis = None
	for command in commands:
		res=get_cli_command(command)
		if res.startswith('Error'):
			return render_to_response('status.html', {
			'mastername': "OpenBTS",
			'pagename': "Status",
			'errorstr':res,})
			
		if command=='alarms':
			alarms=res.split('\n')
		
		elif command=='calls':
			calls=[]
			res=res.split('\n')
			res.pop()
			res.pop()
			res.pop()
			if len(res)>0:
				for call in res:
					tempcall=call.split(' ')
					cID=tempcall[0]
					
					cIMSI=tempcall[3].split('=')
					cIMSI=cIMSI[1]
					
					cSIPID=tempcall[5].split('=')
					cSIPID=cSIPID[1]
					
					cCID=tempcall[8].split('=')
					cCID=cCID[1]
					
					cGSMState=tempcall[9].split('=')
					cGSMState=cGSMState[1]
					
					cSIPState=tempcall[10].split('=')
					cSIPState=cSIPState[1]
					
					cTime=tempcall[11]
					cTime=cTime[1:]
					
					tempcall=[cID,cIMSI,cSIPID,cCID,cGSMState,cSIPState,cTime]
					calls.append(tempcall)
			else:
				calls=' '		
		
		elif command=='cellid':
			cellid=[]
			for value in res.split(' '):
				value=value.split('=')
				cellid.append(value[1])

		elif command=='chans':
			chans=[]
			res=re.sub(' +',' ',res)
			res=res.split('\n')
			del res[0]
			del res[0]
			res.pop()
			res.pop()
			if len(res)>0:
				for idx,val in enumerate(res):
					val=val.lstrip()
					chans.append(val.split(' '))
			else:
				chans=" "
		
		elif command=='load':
			load=[]
			res=res.split('\n')
			res.pop()
			for param in res:
				value=param.split(': ')
				load.append(value[1])
			
		elif command=='power':
			power=[]
			res=res.split('\n')
			power.append(res[0])
			power.append(res[1])
			
		elif command=='tmsis':
			tmsis=[]
			res=res.split('\n')
			res.pop()
			del res[0]
			if len(res)>0:
				for idx,val in enumerate(res):
					val=re.sub(' +',' ',val) #replace multiple spaces with one
					val=val.lstrip() #remove leading space
					tmsis.append(val.split(' '))
			else:
				tmsis=" "	
	
	return render_to_response('status.html', {
		'mastername': "OpenBTS",
		'pagename': "Status",
		'alarms':alarms,
		'calls':calls,
		'chans':chans,
		'cellid':cellid,
		'load' :load,
		'power':power,
		'tmsis':tmsis,
		})
		
def actions(request):
	return render_to_response('actions.html', {
		'mastername': "OpenBTS",
		'pagename': "Actions",
		'itemlist': "actions",
		})
		
def dialdata(request):
	dialdata=Dialdata.objects.using('asterisk').all()
	return render_to_response('dialdata.html', {
		'mastername': "OpenBTS",
		'pagename': "Dial Data",
		'dialdata': dialdata,
		})
