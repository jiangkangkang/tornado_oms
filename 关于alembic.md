# 初始化
alembic init alembic
# 自动创建版本
alembic revision --autogenerate -m "initdb"
# 更新数据库
alembic upgrade 版本号

# 更新到最新版
alembic upgrade head

#降级数据库
alembic downgrade 版本号
#更新到最初版
alembic downgrade head
#离线更新（生成sql）
alembic upgrade 版本号 --sql > migration.sql
#从特定起始版本生成sql
alembic upgrade 版本一:版本二 --sql > migration.sql
#查询当前数据库版本号
#查看alembic_version表。
#清除所有版本
将versions删掉，并删除alembic_version表