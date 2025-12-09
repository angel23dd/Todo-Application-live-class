from app.database import SessionLocal
from app.models import TodoModel

db = SessionLocal()
todos = db.query(TodoModel).all()
print(f'Total todos in database: {len(todos)}')
for t in todos:
    print(f'  - ID: {t.id}, Title: {t.title}, Owner: {t.owner_id}')
db.close()
