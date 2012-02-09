#
# Django Gems.
#
# Copyright (C) 2012 Pier Luigi Fiorini
# Copyright (C) 2008 rizumu
#
# Author(s):
#   Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
#   rizumu
#
# Taken from:
#	http://djangosnippets.org/snippets/1118/
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
from django.template import Context, loader
from django.conf import settings

register = template.Library()

@register.simple_tag
def analytics():
	"""
	This template tag allows easy inclusion of Google Analytics script.
	Define ANALYTICS_ID in your settings.py and put the script into templates/analytics/analytics.html,
	an example follows:

	<script type="text/javascript">
		var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
		document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
	</script>
	<script type="text/javascript">
		var pageTracker = _gat._getTracker("{{ analytics_code }}");
		pageTracker._trackPageview();
	</script>
	"""
	analytics_id = getattr(settings, "ANALYTICS_ID", None)
	if analytics_id and analytics_id.strip() != "":
		t = loader.get_template ("analytics/analytics.html")
		c = Context({
			"analytics_code": analytics_id
		})
		return t.render(c)
	return ""
