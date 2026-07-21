import time
from functools import wraps
 
_store= {}
def cached(ttl_seconds=60):
	def decorator(fn):
		@wraps(fn)
		def wrapper(*args,**kwargs):
			key= (fn.__module__,fn.__name__,args,tuple(sorted(kwargs.items())))
			now= time.time()
			hit= _store.get(key)
			if hit and now < hit[1]:
				return hit[0]
			result= fn(*args,**kwargs)
			_store[key]= (result,now+ttl_seconds)
			return result
		return wrapper
	return decorator

def clear_cache():
	_store.clear()