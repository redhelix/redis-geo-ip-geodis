#Copyright 2011 Do@. All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, are
#permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice, this list of
#      conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright notice, this list
#      of conditions and the following disclaimer in the documentation and/or other materials
#      provided with the distribution.
#
#THIS SOFTWARE IS PROVIDED BY Do@ ``AS IS'' AND ANY EXPRESS OR IMPLIED
#WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR
#CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those of the
#authors and should not be interpreted as representing official policies, either expressed
#or implied, of Do@.

from countries import countries
from location import Location
import json

class Country(Location):
    """
    Wrapper for a country location object
    """

    #what we want to save for a country
    __spec__ = Location.__spec__ + ['population', 'countrycode', 'altname']

    #key is identical to what we want to save
    __keyspec__ = None
    
    def __init__(self, **kwargs):

        super(Country, self).__init__(**kwargs)
        self.altname = kwargs.get('altname', None)
        self.countrycode = kwargs.get('countrycode', None)
        # self.name = countries.get( kwargs.get('country', None), kwargs.get('country', '')).strip()
        self.population = kwargs.get('population', '').strip()


    def save(self, redisConn):
        #save all properties
        redisConn.hmset(self.getId(), dict(((k, getattr(self, k)) for k in \
                                        self.__spec__)))
        redisConn.sadd("country_codes", self.countrycode)
        redisConn.sadd("allcountries", self.name)
        redisConn.set("country:%s" % (self.name), json.dumps({'country' : self.name, 'country_code' : self.countrycode, 'lat' : self.lat, 'lon' : self.lon }))