#!/usr/bin/env python

from distutils.core import setup

setup(name="django-gems",
	version="0.2.4",
	description="Django utilities library",
	long_description="""Contents of this library:
		* jqgrid integration with Django
		* JSONResponseMixIn
		* JSON encoding and decoding functions
		* JSON view decorator
		* Raw template tag that doesn't parse its content, useful for jQuery Template code which uses the same notation of Django templates
		* Currency formatter for templates""",
	author="Pier Luigi Fiorini",
	author_email="pierluigi.fiorini@gmail.com",
	maintainer="Pier Luigi Fiorini",
	maintainer_email="pierluigi.fiorini@gmail.com",
	url="http://plfiorini.github.com/django-gems",
	download_url="http://github.com/plfiorini/django-gems/tarball/master",
	packages=["django_gems", "django_gems.utils", "django_gems.templatetags"],
	package_dir={"django_gems": "django_gems"},
	license="BSD",
	classifiers=["Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Framework :: Django",
		"Classifier: Environment :: Web Environment",
		"License :: OSI Approved :: BSD License",
		"Operating System :: OS Independent",
		"Topic :: Internet"],
	)
