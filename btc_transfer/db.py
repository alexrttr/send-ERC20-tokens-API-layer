import redis


class Redis(object):
    def __init__(self):
        self._db = None

    @property
    def _redis_db(self):
        if self._db is None:
            self._db = redis.StrictRedis(host="database", port=6379, db=0)
        return self._db

    def save_job_results(self, job_id, results):
        self._redis_db.set(job_id, results)

    def get_job_result(self, job_id):
        return self._redis_db.get(job_id)
