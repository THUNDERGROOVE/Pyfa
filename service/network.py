#===============================================================================
# Copyright (C) 2014 Ryan Holmes
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

from service.settings import NetworkSettings
import urllib2
import urllib
import config
import socket

# network timeout, otherwise pyfa hangs for a long while if no internet connection
timeout = 3
socket.setdefaulttimeout(timeout)

class Error(StandardError):
    def __init__(self, msg=None):
        self.message = msg

class RequestError(StandardError):
    pass

class AuthenticationError(StandardError):
    pass

class ServerError(StandardError):
    pass

class TimeoutError(StandardError):
    pass

class Network():
    # Request constants - every request must supply this, as it is checked if
    # enabled or not via settings
    ENABLED = 1
    EVE = 2  # Mostly API, but also covers CREST requests
    PRICES = 4
    UPDATE = 8

    _instance = None
    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = Network()

        return cls._instance

    def request(self, url, type, data=None):
        # URL is required to be https as of right now
        #print "Starting request: %s\n\tType: %s\n\tPost Data: %s"%(url,type,data)

        # Make sure request is enabled
        access = NetworkSettings.getInstance().getAccess()

        if not self.ENABLED & access or not type & access:
            raise Error("Access not enabled - please enable in Preferences > Network")

        # Set up some things for the request
        versionString = "{0} {1} - {2} {3}".format(config.version, config.tag, config.expansionName, config.expansionVersion)
        headers={"User-Agent" : "pyfa {0} (Python-urllib2)".format(versionString)}

        proxy = NetworkSettings.getInstance().getProxySettings()
        if proxy is not None:
            proxy = urllib2.ProxyHandler({'https': "{0}:{1}".format(*proxy)})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)

        request = urllib2.Request(url, headers=headers, data=urllib.urlencode(data) if data else None)
        try:
            return urllib2.urlopen(request)
        except urllib2.HTTPError, error:
            if error.code == 404:
                raise RequestError()
            elif error.code == 403:
                raise AuthenticationError()
            elif error.code >= 500:
                raise ServerError()
        except urllib2.URLError, error:
            if "timed out" in error.reason:
                raise TimeoutError()
            else:
                raise Error(error)
