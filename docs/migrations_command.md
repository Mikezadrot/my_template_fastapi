# For Alembic migrations

On this project you can use few commands:

+ `alembic init migrations` - for initialize alembic(Not necessary on this project now)

+ `alembic upgrade head` - for migrate in db
+ `alembic revision --autogenerate -m "Name_Migration"` - for create file migration in directory migrations/versions
+ `alembic downgrade -1` - for downgrade to previous migration
+ `alembic downgrade <revision_id>` - for downgrade to <revision_id> migration
+ `alembic history` - history

