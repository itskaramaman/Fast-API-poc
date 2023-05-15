from fastapi import FastAPI, Body, Depends
from schemas import TaskItem
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session 

Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.clone()


app = FastAPI()

fake_database = {
    1: {'task': 'Clean car'},
    2: {'task': 'Write Blog'},
    3: {'task': 'Start Stream'}
}


@app.get("/")
def get_tasks(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items


@app.get("/{id}")
def get_task(id: int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    if item:
        return item
    return {"message": "Task not in Database"}

@app.post("/")
def create_task(item: TaskItem, session: Session = Depends(get_session)):
    item = models.Item(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

# @app.post("/")
# def create_task(body = Body()):
#     new_id = len(fake_database.keys()) + 1
#     fake_database[new_id] = {'task': body['task']}
#     return {new_id: fake_database[new_id]}

@app.put("/{id}")
def update_task(id: int, item: TaskItem,  session: Session = Depends(get_session)):
    selectd_item = session.query(models.Item).get(id)
    if not selectd_item:
        return {"message": "Task not found"}
    selectd_item.task = item.task
    session.commit()

    return selectd_item

@app.delete("/{id}")
def delete_task(id: int, session: Session = Depends(get_session)):
    selected_item = session.query(models.Item).get(id)
    if not selected_item:
        return {"message": f"No task with id {id} found" }
    
    session.delete(selected_item)
    session.commit()
    session.close()
    return {"message": "Task successfully deleted"}

