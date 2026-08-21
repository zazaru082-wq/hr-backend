import os

# 1. Update models.py
with open('models.py', 'r', encoding='utf-8') as f:
    models_content = f.read()

if "class Document" not in models_content:
    models_content += """

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doc_id = Column(String, index=True) # D001
    category = Column(String)
    name = Column(String)
    link_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Rule(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    keyword = Column(String, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Merit(Base):
    __tablename__ = "merits"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    merit_type = Column(String) # งานบุญส่วนกลาง / บุคคล
    date = Column(Date)
    location = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
"""
    with open('models.py', 'w', encoding='utf-8') as f:
        f.write(models_content)

# 2. Update schemas.py
with open('schemas.py', 'r', encoding='utf-8') as f:
    schemas_content = f.read()

if "class DocumentBase" not in schemas_content:
    schemas_content += """

# Document (06)
class DocumentBase(BaseModel):
    doc_id: str
    category: str
    name: str
    link_url: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    class Config:
        orm_mode = True

# Rule (07)
class RuleBase(BaseModel):
    keyword: str
    description: str

class RuleCreate(RuleBase):
    pass

class Rule(RuleBase):
    id: int
    class Config:
        orm_mode = True

# Merit (08)
class MeritBase(BaseModel):
    title: str
    merit_type: str
    date: date
    location: Optional[str] = None
    image_url: Optional[str] = None

class MeritCreate(MeritBase):
    pass

class Merit(MeritBase):
    id: int
    class Config:
        orm_mode = True
"""
    with open('schemas.py', 'w', encoding='utf-8') as f:
        f.write(schemas_content)

# 3. Update main.py
with open('main.py', 'r', encoding='utf-8') as f:
    main_content = f.read()

if "/api/documents" not in main_content:
    main_content += """

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
"""
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(main_content)

print("Updated backend for Phase 4")
