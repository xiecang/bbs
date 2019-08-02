# v2ex
一个仿 v2ex 论坛

## 环境
python：3.x


## 运行
```
# 复制配置文件并自行修改
cp settings.py.example setting.py
pip3 install -r requirements.txt

# 使用 python shell 初始化数据库
python3 app.py shell
>>> from models import db
>>> db.create_all()
>>> from models.role import Role
>>> Role.insert_roles()

python3 app.py run
```
