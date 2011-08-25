#!/usr/bin/env python

from distutils.core import setup

setup(name="Django Gems",
	version="0.2.3",
	description="Django utilities library",
	author="Pier Luigi Fiorini",
	author_email="pierluigi.fiorini@gmail.com",
	packages=["django_gems", "django_gems.utils", "django_gems.templatetags"],
	package_dir={"django_gems": "django_gems"},
	license="BSD",
	platforms="Posix; MacOS X; Windows",
	classifiers=["Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: BSD",
		"Operating System :: OS Independent",
		"Topic :: Internet"],
	)
