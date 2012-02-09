#
# Django Gems.
#
# Copyright (C) 2012 Pier Luigi Fiorini
# Copyright (C) 2010 javinievas
#
# Author(s):
#   Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
#   javinievas
#
# Taken from:
#	http://djangosnippets.org/snippets/2130/
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

from django import template

register = template.Library()

@register.filter
def qr(value, size="150x150"):
	"""
	Can convert any string to a QR code as easy as using a simple filter.

	For example:

		<img src="{{ object.code|qr:"120x130"}} " />

	will render a 120x130 QR code.
	"""
	return "http://chart.apis.google.com/chart?chs=%s&cht=qr&chl=%s&choe=UTF-8&chld=H|0" % (size, value)
