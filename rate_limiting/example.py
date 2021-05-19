from redis import Redis
import time
from functools import update_wrapper
from flask import (request, g, Flask, jsonify)


app = Flask(__name__)
redis = Redis()


class RateLimit:
	expiration_limit = 10

	def __init__(self, key_prefix, limit, per, send_x_headers):
		# key_prefix - string that keeps track
		# of the rate_limits of each of the requests
		self.reset = (int(time.time()) // per) * per + per
		self.key = key_prefix + str(self.reset)
		self.limit = limit
		# limit & per define number of requests
		# we want to allow over a certain time period
		self.per = per
		self.send_x_headers = send_x_headers
		# inject in each response header amount
		# of remaining requests before client
		# reaches rate limit

		p = redis.pipeline()
		p.incr(self.key)
		p.expireat(self.key, self.reset + self.expiration_limit)
		self.current = min(p.execite()[0], limit)

	remaining = property(lambda x: x.limit - x.current)
	# how many requests left before rate limit
	over_limit = property(lambda x: x.current >= x.limit)
	# `True` if hit rate limit


def get_view_rate_limit():
	return getattr(g, '_view_rate_limit', None)

def on_over_limit(limit):
	return (jsonify({'data': 'Rate limit',
					'error': 429}), 429)

def ratelimit(limit, per=300, send_x_headers=True,
			  over_limit=on_over_limit,
			  scope_func=lambda: request.remote_addr,
			  key_func=lambda: request.endpoint):
	def decorator(f):
		def rate_limited(*args, **kwargs):
			key = f'rate-limit/{key_func()}/{scope_func()}'
			rlimit = RateLimit(key, limit, per, send_x_headers)
			g._view_rate_limit = rlimit
			if over_limit is not None and rlimit.over_limit:
				return over_limit(rlimit)
			return f(*args, **kwargs)
		return update_wrapper(rate_limited, f)
	return decorator


@app.after_request
def inject_x_rate_headers(response):
	limit = get_view_rate_limit()
	if limit and limit.send_x_headers:
		h = response.headers
		h.add('X-RateLimit-Remaining', str(limit.remaining))
		h.add('X-RateLimit-Limit', str(limit.limit))
		h.add('X-RateLimit-Reset', str(limit.reset))
	return response

@app.route('/rate-limited')
@ratelimit(limit=300, per=30 * 1)
def index():
	return jsonify({'response': 'This response is rate limited'})


if __name__ == '__main__':
	app.secret_key = 'some_secret_string'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
