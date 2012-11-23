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

from django.http import HttpResponseNotFound
from webgui.models import Parameter
import sqlite3
import sys
from django.shortcuts import render_to_response
from django.conf import settings

class Section:
	def __init__(self,fname,fparamlist):
		self.name = fname
		self.paramlist = fparamlist

def main(request):
	table=Parameter.objects.all() 
	datalist=[]
	for section in settings.SECTIONS:
		section_name=section[0]
		paramlist=section[1]
		tempparams=[]
		for param in paramlist:
			for row in table:
				if row.keystring == param: #find keystring in table
					tempparams.append(row) #append .parameter, .value, .comment to output list
					break
		datalist.append(Section(section_name,tempparams))
	return render_to_response('template.html', {
		'pagename': "Main",
		'sectionlist': datalist,
		})

def advanced(request):
	return render_to_response('template.html', {
		'pagename': "Advanced",
		'itemlist': "advanced",
		})
		
def status(request):
	return render_to_response('template.html', {
		'pagename': "Status",
		'itemlist': "status",
		})
def actions(request):
	return render_to_response('template.html', {
		'pagename': "Actions",
		'itemlist': "actions",
		})
def savedata(request):
	if request.method == 'POST':
		return render_to_response('template.html', {
			'pagename': "Savedata",
			'itemlist': "savedata",
			})
