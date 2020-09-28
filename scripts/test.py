import os
import sys
import django

# print(__file__)
# print(os.path.abspath(__file__))
#
# print(os.path.dirname(os.path.abspath(__file__)))
# 第一步：将项目的绝对路径加载到sys.path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# 第二部：设置环境变量 DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper.settings')
# 第三部：django 环境初始化
django.setup()

from User.models import User

