from tastypie.serializers import Serializer

import urlparse





class urlencodeSerializer(Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'plist', 'urlencode']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        
        'plist': 'application/x-plist',
        'urlencode': 'application/x-www-form-urlencoded',
        }
  
    def from_urlencode(self, data,options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v)>1 else v[0] )
            for k, v in urlparse.parse_qs(data).iteritems())
        
        return qs

    def to_urlencode(self,content): 
       
        pass
    