#
# Django Gems.
#
# Copyright (C) 2011 Pier Luigi Fiorini
# Copyright (C) 2008-2010 Tobias Llipstein
#
# Author: Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#	1. Redistributions of source code must retain the above copyright notice,
#	   this list of conditions and the following disclaimer.
#
#	2. Redistributions in binary form must reproduce the above copyright
#	   notice, this list of conditions and the following disclaimer in the
#	   documentation and/or other materials provided with the distribution.
#
#	3. Neither the name of the project nor the names of its contributors may
#	   be used to endorse or promote products derived from this software
#	   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Adapted from
#		http://code.google.com/p/dojango/source/browse/trunk/dojango/util/__init__.py
#

import os, datetime
from decimal import Decimal

from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.db.models import Model
from django.db.models import ImageField, FileField
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.utils import simplejson as json
from django.utils.functional import Promise
from django.utils.encoding import force_unicode

def json_encode(data):
	"""
	The main issues with Django's default JSON serializer is that properties that
	had been added to an object dynamically are being ignored (and it also has 
	problems with some models).
	"""
	def _any(data):
		ret = None
		# Ops, we used to check if it is of type list, but that fails 
		# i.e. in the case of django.newforms.utils.ErrorList, which extends
		# the type "list". Oh man, that was a dumb mistake!
		if isinstance(data, list):
			ret = _list(data)
		# Same as for lists above.
		elif isinstance(data, dict):
			ret = _dict(data)
		elif isinstance(data, Decimal):
			# json.dumps() cant handle Decimal
			ret = str(data)
		elif isinstance(data, QuerySet):
			# Actually its the same as a list ...
			ret = _list(data)
		elif isinstance(data, Model):
			ret = _model(data)
		# here we need to encode the string as unicode (otherwise we get utf-16 in the json-response)
		elif isinstance(data, basestring):
			ret = unicode(data)
		# see http://code.djangoproject.com/ticket/5868
		elif isinstance(data, Promise):
			ret = force_unicode(data)
		elif isinstance(data, datetime.datetime):
			# For dojo.date.stamp we convert the dates to use 'T' as separator instead of space
			# i.e. 2008-01-01T10:10:10 instead of 2008-01-01 10:10:10
			ret = str(data).replace(' ', 'T')
		elif isinstance(data, datetime.date):
			ret = str(data)
		elif isinstance(data, datetime.time):
			ret = 'T' + str(data)
		else:
			# Always fallback to a string!
			ret = data
		return ret
	
	def _model(data):
		ret = {}
		# If we only have a model, we only want to encode the fields.
		for f in data._meta.fields:
			# special FileField handling (they can't be json serialized)
			if isinstance(f, ImageField) or isinstance(f, FileField):
				ret[f.attname] = unicode(getattr(data, f.attname))
			else:
				ret[f.attname] = _any(getattr(data, f.attname))
		# And additionally encode arbitrary properties that had been added.
		fields = dir(data.__class__) + ret.keys()
		# ignoring _state and delete properties
		add_ons = [k for k in dir(data) if k not in fields and k not in ('delete', '_state',)]
		for k in add_ons:
			ret[k] = _any(getattr(data, k))
		return ret

	def _list(data):
		ret = []
		for v in data:
			ret.append(_any(v))
		return ret
	
	def _dict(data):
		ret = {}
		for k,v in data.items():
			ret[k] = _any(v)
		return ret
	
	ret = _any(data)
	return json.dumps(ret, cls=DateTimeAwareJSONEncoder)

def json_decode(json_string):
	"""
	This function is just for convenience/completeness (because we have json_encode).
	Sometimes you want to convert a json-string to a python object.
	It throws a ValueError, if the JSON String is invalid.
	"""
	return json.loads(json_string)

def json_view(func):
	"""
	Decorator that serializes data into a JSON string.
	"""
	def _wrap(request, *args, **kwargs):
		response = None
		try:
			data = func(request, *args, **kwargs)
		except KeyboardInterrupt:
			# Allow keyboard interrupts through for debugging.
			raise
		import datetime
		encoded = json_encode(data)
		response = HttpResponse(encoded, mimetype="application/json")
		response["Pragma"] = "no-cache"
		response["Cache-Control"] = "must-revalidate"
		response["If-Modified-Since"] = str(datetime.datetime.now())
		return response
	return _wrap

class JSONResponseMixin(object):
	def render_to_response(self, context):
		"Returns a JSON response containing 'context' as payload."
		return self.get_json_response(self.convert_context_to_json(context))
	
	def get_json_response(self, content, **httpresponse_kwargs):
		"Construct a `HttpResponse` object."
		import datetime
		response = HttpResponse(content,
				mimetype="application/json",
				**httpresponse_kwargs)
		response["Pragma"] = "no-cache"
		response["Cache-Control"] = "must-revalidate"
		response["If-Modified-Since"] = str(datetime.datetime.now())
		return response
	
	def convert_context_to_json(self, context):
		"Convert the context dictionary into a JSON object."
		return json_encode(context)
