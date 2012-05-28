#
# Django Gems.
#
# Copyright (C) 2012 Pier Luigi Fiorini
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

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO
from django.http import HttpResponse

def xls_convert(array):
	"""
	This function creates a workbook from an array of arrays.
	Each item is a row represented as another array, for example:
	array = [
		["A1", "B1", "C1"],
		["A2", "B2", "C2"]
	]
	"""
	import xlwt

	wb = xlwt.Workbook()
	ws = wb.add_sheet("Foglio")

	row_count = 0
	for row in array:
		for col in range(len(row)):
			ws.write(row_count, col, row[col])
		row_count += 1

	buffer = StringIO()
	wb.save(buffer)
	data = buffer.getvalue()
	buffer.close()
	return data

def xls_view(func):
	"""
	Decorator that convers data into Excel.
	"""
	def _wrap(request, *args, **kwargs):
		try:
			(filename, array) = func(request, *args, **kwargs)
		except KeyboardInterrupt:
			# Allow keyboard interrupts through for debugging.
			raise
		response = HttpResponse(mimetype="application/vnd.ms-excel")
		response["Content-Disposition"] = "attachment; filename=" + filename
#		workbook = xls_convert(array)
#		workbook.save(response)
		data = xls_convert(array)
		response.write(data)
		return response
	return _wrap
