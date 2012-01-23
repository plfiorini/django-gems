#
# Django Gems.
#
# Copyright (C) 2011 Pier Luigi Fiorini
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

#
# The urlquote() function was taken from this page:
#    http://djangosnippets.org/snippets/1159/
#
def urlquote(link=None, get={}):
	"""
	This method does both: urlquote() and urlencode()

	urlqoute(): Quote special characters in 'link'

	urlencode(): Map dictionary to query string key=value&...

	HTML escaping is not done.

	Example:

	  urlquote('/wiki/Python_(programming_language)')     --> '/wiki/Python_%28programming_language%29'
	  urlquote('/mypath/', {'key': 'value'})              --> '/mypath/?key=value'
	  urlquote('/mypath/', {'key': ['value1', 'value2']}) --> '/mypath/?key=value1&key=value2'
	  urlquote({'key': ['value1', 'value2']})             --> 'key=value1&key=value2'
	"""
	from django.utils.http import urlquote  as django_urlquote
	from django.utils.http import urlencode as django_urlencode
	from django.utils.datastructures import MultiValueDict

	assert link or get
	if isinstance(link, dict):
		# urlqoute({'key': 'value', 'key2': 'value2'}) --> key=value&key2=value2
		assert not get, get
		get=link
		link=''
	assert isinstance(get, dict), 'wrong type "%s", dict required' % type(get)
	assert not (link.startswith('http://') or link.startswith('https://')), \
		'This method should only quote the url path. It should not start with http(s)://  (%s)' % (
		link)
	if get:
		# http://code.djangoproject.com/ticket/9089
		if isinstance(get, MultiValueDict):
			get=get.lists()
		if link:
			link='%s?' % django_urlquote(link)
		return u'%s%s' % (link, django_urlencode(get, doseq=True))
	else:
		return django_urlquote(link)
