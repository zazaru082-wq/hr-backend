import os

with open('models.py', 'r', encoding='utf-8') as f:
    models_content = f.read()

if "class LeaveRequest" not in models_content:
    models_content += """

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    person_id = Column(String, index=True) # ForeignKey could be used, but keeping simple
    leave_type = Column(String) # ลาป่วย, ลากิจ, ลาปฏิบัติธรรม
    start_date = Column(Date)
    end_date = Column(Date)
    reason = Column(Text, nullable=True)
    status = Column(String, default="รออนุมัติ") # รออนุมัติ, อนุมัติแล้ว, ไม่อนุมัติ
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
"""
    with open('models.py', 'w', encoding='utf-8') as f:
        f.write(models_content)

with open('schemas.py', 'r', encoding='utf-8') as f:
    schemas_content = f.read()

if "class LeaveRequest" not in schemas_content:
    schemas_content += """
from datetime import datetime

class LeaveRequestBase(BaseModel):
    person_id: str
    leave_type: str
    start_date: date
    end_date: date
    reason: Optional[str] = None
    status: Optional[str] = "รออนุมัติ"

class LeaveRequestCreate(LeaveRequestBase):
    pass

class LeaveRequest(LeaveRequestBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
"""
    with open('schemas.py', 'w', encoding='utf-8') as f:
        f.write(schemas_content)

with open('main.py', 'r', encoding='utf-8') as f:
    main_content = f.read()

if "/api/leaves" not in main_content:
    main_content += """

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
"""
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(main_content)

print("Updated backend for Phase 2")
