from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import os

from backend.database.session import get_db
from backend.database.models import User, Document
from backend.models.schemas import DocumentResponse
from backend.api.deps import get_current_user
from backend.storage.factory import get_storage_provider
from backend.services.doc_service import process_and_index_document, delete_document_from_system

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid filename")

    _, file_ext = os.path.splitext(filename)
    file_type = file_ext.lower().replace(".", "")
    allowed_types = ["pdf", "docx", "doc", "pptx", "ppt", "csv", "txt"]

    if file_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{file_type}'. Supported types: {allowed_types}"
        )

    # 1. Read file bytes
    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read file bytes: {e}"
        )

    # 2. Save physical file via StorageProvider
    try:
        storage = get_storage_provider()
        storage_path = storage.save_file(file_bytes, filename)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {e}"
        )

    # 3. Create Document DB record
    db_doc = Document(
        user_id=current_user.id,
        filename=filename,
        type=file_type,
        size=len(file_bytes),
        status="pending",
        storage_path=storage_path
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    # 4. Trigger processing in the background
    background_tasks.add_task(
        process_and_index_document,
        db=db,
        document_id=db_doc.id,
        user_id=current_user.id
    )

    return db_doc


@router.get("/", response_model=List[DocumentResponse])
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    docs = db.query(Document).filter(Document.user_id == current_user.id).all()
    return docs


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_document_from_system(db, document_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {document_id} not found or permission denied."
        )
    return {"message": "Document successfully deleted"}
