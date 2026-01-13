from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.db import db
from app.scheduler import schedule_email_task, cancel_email_task
from app.gmail import get_admission_notice_template

router = APIRouter(prefix="/scheduler", tags=["scheduler"])


class CreateScheduledEmailRequest(BaseModel):
    name: str
    subject: str
    html_content: str
    target_tags: list[str]
    scheduled_at: datetime


class UpdateScheduledEmailRequest(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    html_content: Optional[str] = None
    target_tags: Optional[list[str]] = None
    scheduled_at: Optional[datetime] = None


class ScheduledEmailResponse(BaseModel):
    id: str
    name: str
    subject: str
    target_tags: list[str]
    scheduled_at: datetime
    status: str
    sent_count: int
    failed_count: int


@router.get("/emails")
async def list_scheduled_emails():
    """List all scheduled emails."""
    emails = await db.scheduledemail.find_many(
        order={"scheduledAt": "desc"}
    )
    return emails


@router.get("/emails/{email_id}")
async def get_scheduled_email(email_id: str):
    """Get a specific scheduled email."""
    email = await db.scheduledemail.find_unique(
        where={"id": email_id}
    )
    if not email:
        raise HTTPException(status_code=404, detail="Scheduled email not found")
    return email


@router.post("/emails")
async def create_scheduled_email(request: CreateScheduledEmailRequest):
    """Create a new scheduled email."""
    # Validate scheduled time is in the future
    if request.scheduled_at <= datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Scheduled time must be in the future"
        )

    # Create in database
    email = await db.scheduledemail.create(
        data={
            "name": request.name,
            "subject": request.subject,
            "htmlContent": request.html_content,
            "targetTags": request.target_tags,
            "scheduledAt": request.scheduled_at,
            "status": "pending"
        }
    )

    # Schedule the task
    schedule_email_task(email.id, request.scheduled_at)

    return email


@router.put("/emails/{email_id}")
async def update_scheduled_email(email_id: str, request: UpdateScheduledEmailRequest):
    """Update a scheduled email."""
    existing = await db.scheduledemail.find_unique(where={"id": email_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Scheduled email not found")

    if existing.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Cannot update an email that has already been sent or cancelled"
        )

    update_data = {}
    if request.name is not None:
        update_data["name"] = request.name
    if request.subject is not None:
        update_data["subject"] = request.subject
    if request.html_content is not None:
        update_data["htmlContent"] = request.html_content
    if request.target_tags is not None:
        update_data["targetTags"] = request.target_tags
    if request.scheduled_at is not None:
        if request.scheduled_at <= datetime.now():
            raise HTTPException(
                status_code=400,
                detail="Scheduled time must be in the future"
            )
        update_data["scheduledAt"] = request.scheduled_at

    email = await db.scheduledemail.update(
        where={"id": email_id},
        data=update_data
    )

    # Reschedule if time was updated
    if request.scheduled_at is not None:
        schedule_email_task(email.id, request.scheduled_at)

    return email


@router.delete("/emails/{email_id}")
async def cancel_scheduled_email(email_id: str):
    """Cancel a scheduled email."""
    existing = await db.scheduledemail.find_unique(where={"id": email_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Scheduled email not found")

    if existing.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Cannot cancel an email that has already been sent"
        )

    # Cancel the scheduled task
    cancel_email_task(email_id)

    # Update status
    email = await db.scheduledemail.update(
        where={"id": email_id},
        data={"status": "cancelled"}
    )

    return {"message": "Scheduled email cancelled", "email": email}


@router.get("/templates/admission")
async def get_admission_template():
    """Get the admission notice email template."""
    return {
        "subject": "【招生通知】華語文教學系國際與文化組招生申請開放",
        "html_content": get_admission_notice_template("{{name}}", "請參閱招生簡章")
    }


@router.get("/preview-recipients")
async def preview_recipients(tags: str = ""):
    """Preview users that would receive an email based on tags."""
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]

    if tag_list:
        users = await db.user.find_many(
            where={"tags": {"has_every": tag_list}},
            select={"id": True, "email": True, "name": True, "tags": True}
        )
    else:
        users = await db.user.find_many(
            select={"id": True, "email": True, "name": True, "tags": True}
        )

    return {
        "count": len(users),
        "users": users
    }


@router.get("/logs")
async def get_email_logs(limit: int = 100):
    """Get recent email logs."""
    logs = await db.emaillog.find_many(
        take=limit,
        order={"sentAt": "desc"},
        include={"user": True}
    )
    return logs
