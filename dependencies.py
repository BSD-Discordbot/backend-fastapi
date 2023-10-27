from fastapi import HTTPException, Request
from db.database import SessionLocal
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_admin(request: Request):
    if(request.session.get("is_admin", None) == None):
        raise HTTPException(status_code=401, detail="User not authentified")
    if(request.session.get("is_admin", None) == False):
        raise HTTPException(status_code=403, detail="Unauthorized")