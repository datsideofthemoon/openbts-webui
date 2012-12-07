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

from django.db import models

# CREATE TABLE CONFIG	
# KEYSTRING TEXT UNIQUE NOT NULL,
# VALUESTRING TEXT,
# STATIC INTEGER DEFAULT 0
# OPTIONAL INTEGER DEFAULT 0
# COMMENTS TEXT DEFAULT

class Parameter(models.Model):
	keystring = models.CharField(max_length=200, primary_key=True, null=False, db_column='KEYSTRING')
	valuestring = models.CharField(max_length=200, null=True, db_column='VALUESTRING')
	comments = models.TextField(null=True, db_column='COMMENTS')
	class Meta:
		db_table = 'CONFIG'

class Dialdata(models.Model):
	dialerid = models.CharField(max_length=40, primary_key=True, null=False, db_column='exten')
	imsi = models.CharField(max_length=128, null=False, db_column='dial')
	class Meta:
		db_table = 'dialdata_table'
