import redis

r = redis.Redis(host='127.0.0.1', port=6379)
try:
    r.ping()
    print("Conexión exitosa a Redis.")
except redis.ConnectionError:
    print("No se pudo conectar a Redis.")
