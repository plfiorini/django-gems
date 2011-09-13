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
# Taken from
#		http://djangosnippets.org/snippets/1825/
#

import locale

from django.template import Library

register = Library()

@register.filter
def currency(value, arg="", symbol=True):
	"""
	Currency formatting template filter.

	Takes a number -- integer, float, decimal -- and formats it according to
	the locale specified as the template tag argument (arg). Examples:

	  * {{ value|currency }}
	  * {{ value|currency:"en_US" }}
	  * {{ value|currency:"pt_BR" }}
	  * {{ value|currency:"pt_BR.UTF8" }}

	If the argument is omitted, the default system locale will be used.

	The third parameter, symbol, controls whether the currency symbol will be
	printed or not. Defaults to true.

	As advised by the Django documentation, this template won't raise
	exceptions caused by wrong types or invalid locale arguments. It will
	return an empty string instead.

	Be aware that currency formatting is not possible using the 'C' locale.
	This function will fall back to 'en_US.UTF8' in this case.
	"""
	saved = '.'.join([x for x in locale.getlocale() if x]) or (None, None)
	given = arg and ('.' in arg and str(arg) or str(arg) + ".UTF-8")

	# Workaround for Python bug 1699853 and other possibly related bugs.
	if '.' in saved and saved.split('.')[1].lower() in ("utf", "utf8"):
		saved = saved.split('.')[0] + ".UTF-8"

	if saved == (None, None) and given == '':
		given = "en_US.UTF-8"

	try:
		locale.setlocale(locale.LC_ALL, given)
		return locale.currency(value or 0, symbol, True)
	except (TypeError, locale.Error):
		return ""
	finally:
		locale.setlocale(locale.LC_ALL, saved)
