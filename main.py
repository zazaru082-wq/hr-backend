
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import models
import schemas
import datetime
from database import engine, get_db

models.Base.metadata.drop_all(bind=engine) # Drop old tables to rebuild with new schema
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Niramitsilp Fund API", version="2.0")

# Enable CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Niramitsilp Fund API"}

# ----- 01 บุคลากร (Employees) -----
@app.post("/api/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_emp = db.query(models.Employee).filter(models.Employee.person_id == employee.person_id).first()
    if db_emp:
        raise HTTPException(status_code=400, detail="Person ID already registered")
    
    new_emp = models.Employee(**employee.dict(), last_updated=datetime.date.today())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp

@app.get("/api/employees/", response_model=List[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Employee).offset(skip).limit(limit).all()

@app.get("/api/employees/{person_id}", response_model=schemas.Employee)
def read_employee(person_id: str, db: Session = Depends(get_db)):
    db_emp = db.query(models.Employee).filter(models.Employee.person_id == person_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_emp

@app.put("/api/employees/{person_id}", response_model=schemas.Employee)
def update_employee(person_id: str, employee_update: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    db_emp = db.query(models.Employee).filter(models.Employee.person_id == person_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_data = employee_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_emp, key, value)
        
    db_emp.last_updated = datetime.date.today()
    db.commit()
    db.refresh(db_emp)
    return db_emp

@app.delete("/api/employees/{person_id}")
def delete_employee(person_id: str, db: Session = Depends(get_db)):
    db_emp = db.query(models.Employee).filter(models.Employee.person_id == person_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_emp)
    db.commit()
    return {"message": "Deleted successfully"}


# ----- 02 วันลา (Leave Management) -----
@app.post("/api/leaves/", response_model=schemas.LeaveRequest)
def create_leave(leave: schemas.LeaveRequestCreate, db: Session = Depends(get_db)):
    db_leave = models.LeaveRequest(**leave.dict())
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

@app.get("/api/leaves/", response_model=List[schemas.LeaveRequest])
def read_leaves(db: Session = Depends(get_db)):
    return db.query(models.LeaveRequest).order_by(models.LeaveRequest.created_at.desc()).all()

@app.put("/api/leaves/{leave_id}/status")
def update_leave_status(leave_id: int, status: str, db: Session = Depends(get_db)):
    db_leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()
    if not db_leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    db_leave.status = status
    db.commit()
    db.refresh(db_leave)
    return db_leave


# ----- 03 คิวหัวหน้า (Schedules) -----
@app.post("/api/schedules/", response_model=schemas.Schedule)
def create_schedule(sched: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_sched = models.Schedule(**sched.dict())
    db.add(db_sched)
    db.commit()
    db.refresh(db_sched)
    return db_sched

@app.get("/api/schedules/", response_model=List[schemas.Schedule])
def read_schedules(db: Session = Depends(get_db)):
    return db.query(models.Schedule).order_by(models.Schedule.date.desc()).all()

@app.put("/api/schedules/{schedule_id}", response_model=schemas.Schedule)
def update_schedule(schedule_id: int, sched: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_sched = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not db_sched:
        raise HTTPException(status_code=404, detail="Schedule not found")
    for key, value in sched.dict().items():
        setattr(db_sched, key, value)
    db.commit()
    db.refresh(db_sched)
    return db_sched

@app.delete("/api/schedules/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_sched = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not db_sched:
        raise HTTPException(status_code=404, detail="Schedule not found")
    db.delete(db_sched)
    db.commit()
    return {"detail": "Schedule deleted successfully"}

# ----- 04 ผลงาน (Performances) -----
@app.post("/api/performances/", response_model=schemas.Performance)
def create_performance(perf: schemas.PerformanceCreate, db: Session = Depends(get_db)):
    db_perf = models.Performance(**perf.dict())
    db.add(db_perf)
    db.commit()
    db.refresh(db_perf)
    return db_perf

@app.get("/api/performances/", response_model=List[schemas.Performance])
def read_performances(db: Session = Depends(get_db)):
    return db.query(models.Performance).order_by(models.Performance.date.desc()).all()

# ----- 05 โครงการ (Projects) -----
@app.post("/api/projects/", response_model=schemas.Project)
def create_project(proj: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_proj = models.Project(**proj.dict())
    db.add(db_proj)
    db.commit()
    db.refresh(db_proj)
    return db_proj

@app.get("/api/projects/", response_model=List[schemas.Project])
def read_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()


# ----- 06 เอกสารสำคัญ (Documents) -----
@app.post("/api/documents/", response_model=schemas.Document)
def create_document(doc: schemas.DocumentCreate, db: Session = Depends(get_db)):
    db_doc = models.Document(**doc.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@app.get("/api/documents/", response_model=List[schemas.Document])
def read_documents(db: Session = Depends(get_db)):
    return db.query(models.Document).all()

# ----- 07 กติกา (Rules) -----
@app.post("/api/rules/", response_model=schemas.Rule)
def create_rule(rule: schemas.RuleCreate, db: Session = Depends(get_db)):
    db_rule = models.Rule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

@app.get("/api/rules/", response_model=List[schemas.Rule])
def read_rules(search: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Rule)
    if search:
        query = query.filter(models.Rule.keyword.ilike(f"%{search}%") | models.Rule.description.ilike(f"%{search}%"))
    return query.all()

# ----- 08 ทบทวนบุญ (Merits) -----
@app.post("/api/merits/", response_model=schemas.Merit)
def create_merit(merit: schemas.MeritCreate, db: Session = Depends(get_db)):
    db_merit = models.Merit(**merit.dict())
    db.add(db_merit)
    db.commit()
    db.refresh(db_merit)
    return db_merit

@app.get("/api/merits/", response_model=List[schemas.Merit])
def read_merits(db: Session = Depends(get_db)):
    return db.query(models.Merit).order_by(models.Merit.date.desc()).all()

# --- Extra PUT / DELETE endpoints ---

@app.put("/api/performances/{item_id}", response_model=schemas.Performance)
def update_performance(item_id: int, item: schemas.PerformanceCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Performance).filter(models.Performance.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Performance not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/api/performances/{item_id}")
def delete_performance(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Performance).filter(models.Performance.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Performance not found")
    db.delete(db_item)
    db.commit()
    return {"status": "deleted"}

@app.put("/api/projects/{item_id}", response_model=schemas.Project)
def update_project(item_id: str, item: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Project).filter(models.Project.project_id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/api/projects/{item_id}")
def delete_project(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(models.Project).filter(models.Project.project_id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_item)
    db.commit()
    return {"status": "deleted"}

@app.put("/api/documents/{item_id}", response_model=schemas.Document)
def update_document(item_id: int, item: schemas.DocumentCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Document).filter(models.Document.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Document not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/api/documents/{item_id}")
def delete_document(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Document).filter(models.Document.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(db_item)
    db.commit()
    return {"status": "deleted"}

@app.put("/api/rules/{item_id}", response_model=schemas.Rule)
def update_rule(item_id: int, item: schemas.RuleCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Rule).filter(models.Rule.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Rule not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/api/rules/{item_id}")
def delete_rule(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Rule).filter(models.Rule.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(db_item)
    db.commit()
    return {"status": "deleted"}

@app.put("/api/merits/{item_id}", response_model=schemas.Merit)
def update_merit(item_id: int, item: schemas.MeritCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Merit).filter(models.Merit.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Merit not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/api/merits/{item_id}")
def delete_merit(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Merit).filter(models.Merit.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Merit not found")
    db.delete(db_item)
    db.commit()
    return {"status": "deleted"}

# Attempt to alter tables for missing columns (safe to fail if they exist)
from sqlalchemy import text
try:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS description TEXT;"))
        conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS owner VARCHAR;"))
        conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS progress INTEGER;"))
        conn.commit()
except Exception as e:
    print("Alter table failed (might already exist):", e)
