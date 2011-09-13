#
# Django Gems.
#
# Copyright (C) 2011 Pier Luigi Fiorini
# Copyright (C) 2009 Gerry Eisenhaur
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
# Here's a brief list of changes made by Pier Luigi Fiorini.
#
# Options added:
#   - distinct
#   - start_empty
#
# Methods added:
#
# Other changes:
#   - field_to_colmodel(): editable set to False
#   - get_queryset(): queryset filtered by all fields in get_field_names()
#   - filter_items(): use self.get_model() so that self.model is set according
#                     to the queryset when not explicitely assigned by user
#   - filter_items(): use lookup_foreign_key_field() to allow searches on
#                     foreign keys.
#

import operator
from django.db import models
from django.core.exceptions import FieldError, ImproperlyConfigured
from django.core.paginator import Paginator, InvalidPage
from django.utils import simplejson as json
from django.utils.encoding import smart_str
from django.http import Http404
from json import json_encode

import logging
logger = logging.getLogger(__name__)

class JqGrid(object):
	queryset = None
	model = None
	fields = []
	allow_empty = True
	distinct = True
	start_empty = False

	pager_id = "#pager"
	url = None
	caption = None
	colmodel_overrides = {}

	def get_queryset(self, request):
		if hasattr(self, "queryset") and self.queryset is not None:
			queryset = self.queryset.values(*self.get_field_names())._clone()
		elif hasattr(self, "model") and self.model is not None:
			queryset = self.model.objects.values(*self.get_field_names())
		else:
			raise ImproperlyConfigured("No queryset or model defined.")
		if self.distinct:
			self.queryset = queryset.distinct()
		else:
			self.queryset = queryset
		return self.queryset

	def get_model(self):
		if hasattr(self, "model") and self.model is not None:
			model = self.model
		elif hasattr(self, "queryset") and self.queryset is not None:
			model = self.queryset.model
			self.model = model
		else:
			raise ImproperlyConfigured("No queryset or model defined.")
		return model

	def get_items(self, request):
		items = self.get_queryset(request)
		items = self.filter_items(request, items)
		items = self.sort_items(request, items)
		paginator, page, items = self.paginate_items(request, items)
		return (paginator, page, items)

	def get_filters(self, request):
		_search = request.GET.get("_search")
		filters = None

		if _search == "true":
			_filters = request.GET.get("filters")
			try:
				filters = _filters and json.loads(_filters)
			except ValueError:
				return None

			if filters is None:
				field = request.GET.get("searchField")
				op = request.GET.get("searchOper")
				data = request.GET.get("searchString")

				if all([field, op, data]):
					filters = {
						"groupOp": "AND",
						"rules": [{ "op": op, "field": field, "data": data }]
					}
		return filters

	def filter_items(self, request, items):
		# TODO: Add option to use case insensitive filters
		# TODO: Add more support for RelatedFields (searching and displaying)
		# FIXME: Validate data types are correct for field being searched.
		filter_map = {
			# jqgrid op: (django_lookup, use_exclude)
			"ne": ("%(field)s__exact", True),
			"bn": ("%(field)s__startswith", True),
			"en": ("%(field)s__endswith",  True),
			"nc": ("%(field)s__contains", True),
			"ni": ("%(field)s__in", True),
			"in": ("%(field)s__in", False),
			"eq": ("%(field)s__exact", False),
			"ieq": ("%(field)s__iexact", False),
			"bw": ("%(field)s__startswith", False),
			"gt": ("%(field)s__gt", False),
			"ge": ("%(field)s__gte", False),
			"lt": ("%(field)s__lt", False),
			"le": ("%(field)s__lte", False),
			"ew": ("%(field)s__endswith", False),
			"cn": ("%(field)s__contains", False),
			"icn": ("%(field)s__icontains", False)
		}
		_filters = self.get_filters(request)
		if _filters is None:
			return items

		q_filters = []
		for rule in _filters["rules"]:
			op, field, data = rule["op"], rule["field"], rule["data"]
			opts = self.get_model()._meta
			field_class = self.lookup_foreign_key_field(opts, field)[0]
			filter_fmt, exclude = filter_map[op]
			filter_str = smart_str(filter_fmt % {"field": field})
			if filter_fmt.endswith("__in"):
				d_split = data.split(",")
				filter_kwargs = {filter_str: data.split(",")}
			else:
				if field_class.get_internal_type() == "BooleanField":
					# Boolean fields have a special treatment
					filter_value = False
					if smart_str(data) == "true": filter_value = True
					filter_kwargs = {filter_str: filter_value}
				else:
					filter_kwargs = {filter_str: smart_str(data)}
			# Append the filters to the list
			if exclude:
				q_filters.append(~models.Q(**filter_kwargs))
			else:
				q_filters.append(models.Q(**filter_kwargs))
		# Filter the data
		if _filters["groupOp"].upper() == "OR":
			filters = reduce(operator.ior, q_filters)
		else:
			filters = reduce(operator.iand, q_filters)
		return items.filter(filters)

	def sort_items(self, request, items):
		sidx = request.GET.get("sidx")
		if sidx is not None:
			sord = request.GET.get("sord")
			order_by = "%s%s" % (sord == "desc" and "-" or "", sidx)
			try:
				items = items.order_by(order_by)
			except FieldError:
				pass
		return items

	def get_paginate_by(self, request):
		rows = request.GET.get("rows", 10)
		try:
			paginate_by = int(rows)
		except ValueError:
			paginate_by = 10
		return paginate_by

	def paginate_items(self, request, items):
		paginate_by = self.get_paginate_by(request)
		if not paginate_by:
			return (None, None, items)

		paginator = Paginator(items, paginate_by,
			allow_empty_first_page=self.allow_empty)
		page = request.GET.get("page", 1)

		try:
			page_number = int(page)
			page = paginator.page(page_number)
		except (ValueError, InvalidPage):
			page = paginator.page(1)
		return (paginator, page, page.object_list)

	def get_data(self, request, as_json=True):
		# Honor the start_empty setting
		if self.start_empty and request.GET.get("_search", "false") == "false":
			result = {
				"page": 1,
				"total": 1,
				"rows": [],
				"records": 0
			}
		else:
			# Otherwise return the items
			paginator, page, items = self.get_items(request)
			result = {
				"page": page.number,
				"total": paginator.num_pages,
				"rows": items,
				"records": paginator.count
			}
		if as_json:
			return json_encode(result)
		return result

	def get_json(self, request):
		# Honor the start_empty setting
		if self.start_empty and request.GET.get("_search", "false") == "false":
			return json_encode({
				"page": 1,
				"total": 1,
				"rows": [],
				"records": 0
			})
		# Otherwise return the items
		paginator, page, items = self.get_items(request)
		return json_encode({
			"page": page.number,
			"total": paginator.num_pages,
			"rows": items,
			"records": paginator.count
		})

	def get_default_config(self):
		config = {
			"datatype": "json",
			"autowidth": True,
			"forcefit": True,
			"shrinkToFit": True,
			"jsonReader": {"repeatitems": False},
			"rowNum": 10,
			"rowList": [10, 25, 50, 100],
			"sortname": "id",
			"viewrecords": True,
			"sortorder": "asc",
			"pager": self.pager_id,
			"altRows": True,
			"gridview": True,
			"height": "auto",
			"viewsortcols": True,
			#"multikey": "ctrlKey",
			#"multiboxonly": True,
			#"multiselect": False,
			#"toolbar": [False, "bottom"],
			#"userData": None,
			#"rownumbers": False,
		}
		return config

	def get_url(self):
		return self.url

	def get_caption(self):
		if self.caption is None:
			opts = self.get_model()._meta
			self.caption = opts.verbose_name_plural.capitalize()
		return self.caption

	def get_config(self, as_json=True):
		config = self.get_default_config()
		config.update({
			"url": self.get_url(),
			"caption": self.get_caption(),
			"colModel": self.get_colmodels(),
		})
		if as_json:
			config = json_encode(config)
		return config
	
	def lookup_foreign_key_field(self, options, field_name):
		"""Make a field lookup converting __ into real models fields"""
		if "__" in field_name:
			fk_name, field_name = field_name.split("__", 1)
			fields = [f for f in options.fields if f.name == fk_name]
			if len(fields) > 0:
				field_class = fields[0]
			else:
				raise FieldError("No field %s in %s" % (fk_name, options))
			foreign_model_options = field_class.rel.to._meta
			return self.lookup_foreign_key_field(foreign_model_options, field_name)
		else:
			return options.get_field_by_name(field_name)

	def get_colmodels(self):
		colmodels = []
		opts = self.get_model()._meta
		for field_name in self.get_field_names():
			(field, model, direct, m2m) = self.lookup_foreign_key_field(opts, field_name)
			colmodel = self.field_to_colmodel(field, field_name)
			override = self.colmodel_overrides.get(field_name)

			if override:
				colmodel.update(override)
			colmodels.append(colmodel)
		return colmodels

	def get_field_names(self):
		fields = self.fields
		if not fields:
			fields = [f.name for f in self.get_model()._meta.local_fields]
		return fields

	def field_to_colmodel(self, field, field_name):
		colmodel = {
			"name": field_name,
			"index": field.name,
			"label": field.verbose_name,
			"editable": False
		}
		return colmodel
