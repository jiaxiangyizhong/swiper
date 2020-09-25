import pickle
from pickle import UnpicklingError

from redis import Redis as _Redis
from swiper.config import REDIS


# redis数据库缓存不识别中文或一些数据类型，设置缓存时需先序列化数据再进行缓存存储，获取缓存时获取到值后再进行反序列化

class Redis(_Redis):
    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        # 带序列化处理的set方法
        pickle_data = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        return super().set(name, pickle_data, ex, px, nx, xx)

    def get(self, name, default=None):
        # 贷序列化处理的get方法
        pickled_data = super().get(name)
        if pickled_data is None:
            return default
        try:
            value = pickle.loads(pickled_data)
        except (KeyError, EOFError, UnpicklingError):
            return pickled_data
        else:
            return value


rds = Redis(**REDIS)

