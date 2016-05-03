#
# Django Gems.
#
# Copyright (C) 2016 Pier Luigi Fiorini
#
# Author(s):
#   Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
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

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.core.serializers.json import DjangoJSONEncoder
from django.template import Library
from django.utils.safestring import mark_safe

try:
    from django.utils import simplejson
except ImportError:
    import json as simplejson

register = Library()

def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize("json", object))
    return mark_safe(simplejson.dumps(object, cls=DjangoJSONEncoder))

register.filter("jsonify", jsonify)
