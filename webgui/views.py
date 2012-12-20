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

import time, socket, os, re, subprocess
from django.conf import settings
from webgui.models import Parameter, Dialdata
from django.db import connection, transaction
from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound

SOCKETNAME=''
SOCK = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
class ActionsSection:
	def __init__(self,fname,fparam1,fparam1name,fparam2,fparam2name,fparam3,fparam3name,fcommand):
		self.name = fname
		self.param1 = fparam1
		self.param1name = fparam1name
		self.param2 = fparam2
		self.param2name = fparam2name
		self.param3 = fparam3
		self.param3name = fparam3name
		self.command = fcommand
		
class Section:
	def __init__(self,fname,fparamlist):
		self.name = fname
		self.paramlist = fparamlist

def main(request):
	if request.method == 'POST':
		for key, value in request.POST.iteritems():
			param=Parameter.objects.filter(keystring=key)
			param=param[0]
			if value=="[NULL]" :
				value=None
			NewParam=Parameter(keystring=param.keystring,valuestring=value,static=param.static,optional=param.optional,comments=param.comments)
			NewParam.save()
			
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
		for key, value in request.POST.iteritems():
			param=Parameter.objects.filter(keystring=key)
			param=param[0]
			if value=="[NULL]" :
				value=None
			NewParam=Parameter(keystring=param.keystring,valuestring=value,static=param.static,optional=param.optional,comments=param.comments)
			NewParam.save()
	
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
		return "Error: could not connect to OpenBTS." + ' OpenBTS is not running. '
	try:
		data = SOCK.recv(10000)
	except Exception, e:
		return "Error: could not connect to OpenBTS." + ' receive: '+ str(e)
	return data				#maybe close socket? delete tmp file?

def parseAlarms(string):
	return string.split('\n')

def parseCalls(string):
	calls=[]
	callsList=string.split('\n')
	callsList.pop()
	callsList.pop()
	callsList.pop()
	if len(callsList)>0:
		for call in callsList:
			tempcall=call.split(' ')
			cID=tempcall[0]
					
			cIMSI=tempcall[3].split('=')
			cIMSI=cIMSI[1]
					
			cSIPID=tempcall[5].split('=')
			cSIPID=cSIPID[1]
			
			if "SMS" in call:
				cCID=" "
					
				cGSMState=tempcall[8].split('=')
				cGSMState=cGSMState[1]
					
				cSIPState=tempcall[9].split('=')
				cSIPState=cSIPState[1]
					
				cTime=tempcall[10]
				cTime=cTime[1:]
			else:
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
	return calls

def parseCellID(string):
	cellid=[]
	for value in string.split(' '):
		value=value.split('=')
		cellid.append(value[1])
	return cellid

def parseChans(string):
	chans=[]
	string=re.sub(' +',' ',string)
	chansList=string.split('\n')
	del chansList[0]
	del chansList[0]
	chansList.pop()
	chansList.pop()
	if len(chansList)>0:
		for idx,val in enumerate(chansList):
			val=val.lstrip()
			chans.append(val.split(' '))
	else:
		chans=" "
	return chans

def parseLoad(string):
	load=[]
	loadList=string.split('\n')
	loadList.pop()
	for param in loadList:
		value=param.split(': ')
		load.append(value[1])
	return load
	
def parsePower(string):
	power=[]
	tmp=string.split('\n')
	power.append(tmp[0])
	power.append(tmp[1])
	return power

def parseTMSIs(string):
	tmsis=[]
	tmsisList=string.split('\n')
	tmsisList.pop()
	del tmsisList[0]
	if len(tmsisList)>0:
		for idx,val in enumerate(tmsisList):
			val=re.sub(' +',' ',val) #replace multiple spaces with one
			val=val.lstrip() #remove leading space
			tmsis.append(val.split(' '))
	else:
		tmsis=" "
	return tmsis

def parseUptime(string):
	uptime=[]
	tmp=string.split('\n')
	uptime.append(tmp[0])
	uptime.append(tmp[1])
	return uptime
	
def parseNoise(string):
	noise=[]
	tmp=string.split('\n')
	noise.append(tmp[0])
	noise.append(tmp[1])
	return noise

def parseRegperiod(string):
	regperiod=[]
	tmp=string.split('\n')
	regperiod.append(tmp[0])
	regperiod.append(tmp[1])
	return regperiod

def parseVersion(string):
	vers=[]
	tmp=string.split('\n')
	vers.append(tmp[0])
	return vers
	
def status(request):
	if request.method == 'POST':
		get_cli_command('tmsis clear')
		
	commands=['calls','cellid','chans','load','power','tmsis','uptime','regperiod','noise','version']
	alarms= None
	calls = None
	cellid= None
	chans = None
	load  = None
	power = None
	tmsis = None
	uptime= None
	regperiod=None
	noise=None
	vers=None
	
	for command in commands:
		res=get_cli_command(command)
		if res.startswith('Error'):
			return render_to_response('status.html', {
			'mastername': "OpenBTS",
			'pagename': "Status",
			'errorstr':res,})
			
		if command=='alarms':
			alarms=parseAlarms(res)
		elif command=='calls':
			calls=parseCalls(res)
		elif command=='cellid':
			cellid=parseCellID(res)
		elif command=='chans':
			chans=parseChans(res)
		elif command=='load':
			load=parseLoad(res)
		elif command=='power':
			power=parsePower(res)
		elif command=='tmsis':
			tmsis=parseTMSIs(res)
		elif command=='uptime':
			uptime=parseUptime(res)
		elif command=='regperiod':
			regperiod=parseRegperiod(res)
		elif command=='noise':
			noise=parseNoise(res)
		elif command=='version':
			vers=parseVersion(res)
		
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
		'uptime':uptime,
		'regperiod':regperiod,
		'noise':noise,
		'version':vers,
		})
		
def isProcessRunning(process_name):
	ps = subprocess.Popen("ps -A", shell=True, stdout=subprocess.PIPE)
	ps_pid = ps.pid
	output = ps.stdout.read()
	ps.stdout.close()
	ps.wait()
	for line in output.split("\n"):
		if line != "" and line != None:
			fields = line.split()
			pname = fields[3]
			if(pname == process_name):
				return True
	return False
	
def actions(request):
	if request.method == 'POST':
		res=''
		if request.POST['command']=='start':
			#start  openbts
			os.chdir(settings.OPENBTS_PATH)
			cmd= settings.OPENBTS_PATH + "/OpenBTS"
			p = subprocess.Popen(args=["gnome-terminal", "-e",'sudo '+cmd])
			time.sleep(2)
			
		elif request.POST['command']=='stop':
			#stop  openbts
			os.system("killall -9 OpenBTS")
			
		elif request.POST['command']=='endcall':
			transactionId=request.POST['transactionId']
			if transactionId=='':
				return render_to_response('actions.html', {
				'mastername': "OpenBTS",
				'pagename': "Actions",
				'error': "You need to specify Transaction ID.",})
			res=get_cli_command('endcall '+ transactionId)
			
		elif request.POST['command']=='page': #works
			imsi=request.POST['imsi']
			stime=request.POST['time']
			if imsi=='' or stime=='':
				return render_to_response('actions.html', {
				'mastername': "OpenBTS",
				'pagename': "Actions",
				'error': "You need to specify IMSI and time.",})
			res=get_cli_command('page '+ imsi+' '+stime)
			
		elif request.POST['command']=='power':  #works
			minAtten=request.POST['minAtten']
			maxAtten=request.POST['maxAtten']
			if minAtten=='' or maxAtten=='':
				return render_to_response('actions.html', {
				'mastername': "OpenBTS",
				'pagename': "Actions",
				'error': "You need to specify minAtten and maxAtten.",})
			res=get_cli_command('power '+ minAtten +' '+maxAtten)
			
		elif request.POST['command']=='sendsms':		#works
			imsi=request.POST['imsi']
			sourceAddress=request.POST['sourceAddress']
			text=request.POST['text']
			if imsi=='' or sourceAddress=='' or text=='':
				return render_to_response('actions.html', {
				'mastername': "OpenBTS",
				'pagename': "Actions",
				'error': "You need to specify IMSI, source address and text.",})
			res=get_cli_command('sendsms '+ imsi +' '+sourceAddress + ' '+text)
			
			
		elif request.POST['command']=='sendsimple':	#works
			imsi=request.POST['imsi']
			sourceAddress=request.POST['sourceAddress']
			text=request.POST['text']
			if imsi=='' or sourceAddress=='' or text=='':
				return render_to_response('actions.html', {
				'mastername': "OpenBTS",
				'pagename': "Actions",
				'error': "You need to specify IMSI, source address and text.",})
			res=get_cli_command('sendsimple '+ imsi +' '+sourceAddress + ' ' + text)
		
		elif request.POST['command']=='rxgain':
			gain=request.POST['gain']
			if gain=='':
				return render_to_response('actions.html', {
				'mastername': "OpenBTS",
				'pagename': "Actions",
				'error': "You need to specify gain.",})
			res=get_cli_command('rxgain '+gain)
			
		elif request.POST['command']=='regperiod':
			T3212=request.POST['T3212']
			SIP=request.POST['SIP']
			if T3212=='' or SIP=='':
				return render_to_response('actions.html', {
				'mastername': "OpenBTS",
				'pagename': "Actions",
				'error': "You need to specify T3212 and SIP registration periods.",})
				
		if res.startswith('Error'):
			return render_to_response('actions.html', {
				'mastername': "OpenBTS",
				'pagename': "Actions",
				'error': res,})
				
	section_commands=['startstop','endcall','page','power','sendsms','sendsimple','rxgain','regperiod']
	section_names=['Start/Stop OpenBTS','Endcall','Page','Set power','Send SMS','Send Simple','Set RX gain','Set registration period']
	
	Sections=[]
	
	#Start/stop OpenBTS
	if isProcessRunning('OpenBTS'):
		startstop=ActionsSection('Stop OpenBTS',None,None,None,None,None,None,'stop')
	else:
		startstop=ActionsSection('Start OpenBTS',None,None,None,None,None,None,'start')
	
	#encall TransactionID
	endcall=ActionsSection(section_names[1],'transactionId','Transaction ID',None,None,None,None,section_commands[1])
	#page IMSI
	page=ActionsSection(section_names[2],'imsi','IMSI','time','Time',None,None,section_commands[2])
	#power min,max
	power=ActionsSection(section_names[3],'minAtten','minAtten','maxAtten','maxAtten',None,None,section_commands[3])
	#sendsms IMSI, sourceAddress, text
	sendsms=ActionsSection(section_names[4],'imsi','IMSI','sourceAddress','Source address','text','Text',section_commands[4])
	#sendsimple CallerID, text
	sendsimple=ActionsSection(section_names[5],'imsi','IMSI','sourceAddress','Source address','text','Text',section_commands[5])
	#rxgain gain
	rxgain=ActionsSection(section_names[6],'gain','Gain',None,None,None,None,section_commands[6])
	#regperiod T3212, SIP
	regperiod=ActionsSection(section_names[7],'T3212','T3212 GSM','SIP','SIP',None,None,section_commands[7])
	
	Sections.append(startstop)
	Sections.append(endcall)
	Sections.append(page)
	Sections.append(sendsms)
	Sections.append(sendsimple)
	Sections.append(power)
	Sections.append(rxgain)
	Sections.append(regperiod)
	
	return render_to_response('actions.html', {
		'mastername': "OpenBTS",
		'pagename': "Actions",
		'sectionlist': Sections,
		})

def smqactions(request):
	if request.method == 'POST':
		if request.POST['command']=='start':
			#start  smqueue
			os.chdir(settings.SMQUEUE_PATH)
			cmd= settings.SMQUEUE_PATH + "/smqueue"
			p = subprocess.Popen(args=["gnome-terminal", "-e",'sudo '+cmd])
			time.sleep(2)
			
		elif request.POST['command']=='stop':
			#stop  smqueue
			os.system("killall -9 smqueue")

	Sections=[]
	
	#Start/stop smqueue
	if isProcessRunning('smqueue'):
		startstop=ActionsSection('Stop Smqueue',None,None,None,None,None,None,'stop')
	else:
		startstop=ActionsSection('Start Smqueue',None,None,None,None,None,None,'start')
		
	Sections.append(startstop)
	return render_to_response('smq_actions.html', {
		'mastername': "Smqueue",
		'pagename': "Actions",
		'sectionlist': Sections,
		})	
		
def smqmain(request):
	return render_to_response('smq_main.html', {
		'mastername': "Smqueue",
		'pagename': "Main",
		'sectionlist': None,
		})

def smqadvanced(request):
	if request.method == 'POST':
		for key, value in request.POST.iteritems():
			param=Parameter.objects.using('smqueue').filter(keystring=key)
			param=param[0]
			if value=="[NULL]" :
				value=None
			NewParam=Parameter(keystring=param.keystring,valuestring=value,static=param.static,optional=param.optional,comments=param.comments)
			NewParam.save(using='smqueue')
			
	table=Parameter.objects.using('smqueue').all() 
	datalist=[]
	for prefix in settings.SMQ_ADV_PREFIXES:
		tempparams=[]
		for row in table:
			if row.keystring.startswith(prefix): #find keystring in table by prefix
				tempparams.append(row) #append .parameter, .value, .comment to output list
		if len(tempparams)>0:
			datalist.append(Section(prefix,tempparams))
	return render_to_response('smq_advanced.html', {
		'mastername': "Smqueue",
		'pagename': "Advanced",
		'sectionlist': datalist,
		})

def sbrdialdata(request):
	dialdata=Dialdata.objects.using('asterisk').all()
	return render_to_response('sbr_dialdata.html', {
		'mastername': "SubscriberRegistry",
		'pagename': "Dial Data",
		'dialdata': dialdata,
		})

def sbractions(request):
	if request.method == 'POST':
		if request.POST['command']=='start':
			#start  subscriberRegistry
			os.chdir(settings.SUBSCRIBERREGISTRY_PATH)
			cmd = settings.SUBSCRIBERREGISTRY_PATH + "/sipauthserve"
			p = subprocess.Popen(args=["gnome-terminal", "-e",'sudo '+cmd])
			time.sleep(2)
			
		elif request.POST['command']=='stop':
			#stop  subscriberRegistry
			os.system("killall -9 sipauthserve")

	Sections=[]
	
	#Start/stop subscriberRegistry
	if isProcessRunning('sipauthserve'):
		startstop=ActionsSection('Stop SubscriberRegistry',None,None,None,None,None,None,'stop')
	else:
		startstop=ActionsSection('Start SubscriberRegistry',None,None,None,None,None,None,'start')
		
	Sections.append(startstop)
	return render_to_response('sbr_actions.html', {
		'mastername': "SubscriberRegistry",
		'pagename': "Actions",
		'sectionlist': Sections,
		})	
def sbradvanced(request):
	if request.method == 'POST':
		for key, value in request.POST.iteritems():
			param=Parameter.objects.using('subscriberregistry').filter(keystring=key)
			param=param[0]
			if value=="[NULL]" :
				value=None
			NewParam=Parameter(keystring=param.keystring,valuestring=value,static=param.static,optional=param.optional,comments=param.comments)
			NewParam.save(using='subscriberregistry')
			
	table=Parameter.objects.using('subscriberregistry').all() 
	datalist=[]
	for prefix in settings.SBR_ADV_PREFIXES:
		tempparams=[]
		for row in table:
			if row.keystring.startswith(prefix): #find keystring in table by prefix
				tempparams.append(row) #append .parameter, .value, .comment to output list
		if len(tempparams)>0:
			datalist.append(Section(prefix,tempparams))
	return render_to_response('sbr_advanced.html', {
		'mastername': "SubscriberRegistry",
		'pagename': "Advanced",
		'sectionlist': datalist,
		})
