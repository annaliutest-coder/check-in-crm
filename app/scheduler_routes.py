import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.db import db
from app.scheduler import schedule_email_task, cancel_email_task
from app.email_templates import get_template, get_all_templates, TEMPLATES

router = APIRouter(prefix="/scheduler", tags=["scheduler"])


def parse_tags(tags_str: str) -> list[str]:
    """Parse JSON tags string to list."""
    try:
        return json.loads(tags_str) if tags_str else []
    except:
        return []


def serialize_tags(tags: list[str]) -> str:
    """Serialize tags list to JSON string."""
    return json.dumps(tags, ensure_ascii=False)


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


@router.get("/emails")
async def list_scheduled_emails():
    """List all scheduled emails."""
    emails = await db.scheduledemail.find_many(order={"scheduledAt": "desc"})

    # Parse tags for response
    result = []
    for email in emails:
        result.append({
            "id": email.id,
            "name": email.name,
            "subject": email.subject,
            "targetTags": parse_tags(email.targetTags),
            "scheduledAt": email.scheduledAt,
            "sentAt": email.sentAt,
            "status": email.status,
            "sentCount": email.sentCount,
            "failedCount": email.failedCount,
            "createdAt": email.createdAt
        })

    return result


@router.get("/emails/{email_id}")
async def get_scheduled_email(email_id: str):
    """Get a specific scheduled email."""
    email = await db.scheduledemail.find_unique(where={"id": email_id})
    if not email:
        raise HTTPException(status_code=404, detail="Scheduled email not found")

    return {
        "id": email.id,
        "name": email.name,
        "subject": email.subject,
        "htmlContent": email.htmlContent,
        "targetTags": parse_tags(email.targetTags),
        "scheduledAt": email.scheduledAt,
        "status": email.status
    }


@router.post("/emails")
async def create_scheduled_email(request: CreateScheduledEmailRequest):
    """Create a new scheduled email."""
    if request.scheduled_at <= datetime.now():
        raise HTTPException(status_code=400, detail="Scheduled time must be in the future")

    email = await db.scheduledemail.create(
        data={
            "name": request.name,
            "subject": request.subject,
            "htmlContent": request.html_content,
            "targetTags": serialize_tags(request.target_tags),
            "scheduledAt": request.scheduled_at,
            "status": "pending"
        }
    )

    schedule_email_task(email.id, request.scheduled_at)

    return {
        "id": email.id,
        "name": email.name,
        "subject": email.subject,
        "targetTags": request.target_tags,
        "scheduledAt": email.scheduledAt,
        "status": email.status
    }


@router.put("/emails/{email_id}")
async def update_scheduled_email(email_id: str, request: UpdateScheduledEmailRequest):
    """Update a scheduled email."""
    existing = await db.scheduledemail.find_unique(where={"id": email_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Scheduled email not found")

    if existing.status != "pending":
        raise HTTPException(status_code=400, detail="Cannot update a processed email")

    update_data = {}
    if request.name is not None:
        update_data["name"] = request.name
    if request.subject is not None:
        update_data["subject"] = request.subject
    if request.html_content is not None:
        update_data["htmlContent"] = request.html_content
    if request.target_tags is not None:
        update_data["targetTags"] = serialize_tags(request.target_tags)
    if request.scheduled_at is not None:
        if request.scheduled_at <= datetime.now():
            raise HTTPException(status_code=400, detail="Scheduled time must be in the future")
        update_data["scheduledAt"] = request.scheduled_at

    email = await db.scheduledemail.update(where={"id": email_id}, data=update_data)

    if request.scheduled_at is not None:
        schedule_email_task(email.id, request.scheduled_at)

    return {"message": "Updated", "id": email.id}


@router.delete("/emails/{email_id}")
async def cancel_scheduled_email(email_id: str):
    """Cancel a scheduled email."""
    existing = await db.scheduledemail.find_unique(where={"id": email_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Scheduled email not found")

    if existing.status != "pending":
        raise HTTPException(status_code=400, detail="Cannot cancel a processed email")

    cancel_email_task(email_id)

    await db.scheduledemail.update(
        where={"id": email_id},
        data={"status": "cancelled"}
    )

    return {"message": "Cancelled"}


# ===== Templates API =====

@router.get("/templates")
async def list_templates():
    """List all available email templates."""
    return get_all_templates()


@router.get("/templates/{template_id}")
async def get_template_by_id(template_id: str):
    """Get a specific email template."""
    template = get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    return {
        "id": template_id,
        "name": template["name"],
        "subject": template["subject"],
        "html_content": template["html"]
    }


# ===== Recipients Preview =====

@router.get("/preview-recipients")
async def preview_recipients(tags: str = ""):
    """Preview users that would receive an email based on tags."""
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]

    users = await db.user.find_many()

    if tag_list:
        filtered = []
        for user in users:
            user_tags = parse_tags(user.tags)
            if all(t in user_tags for t in tag_list):
                filtered.append({
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "tags": user_tags
                })
        return {"count": len(filtered), "users": filtered}
    else:
        result = [{
            "id": u.id,
            "email": u.email,
            "name": u.name,
            "tags": parse_tags(u.tags)
        } for u in users]
        return {"count": len(result), "users": result}


@router.get("/logs")
async def get_email_logs(limit: int = 100):
    """Get recent email logs."""
    logs = await db.emaillog.find_many(
        take=limit,
        order={"sentAt": "desc"},
        include={"user": True}
    )
    return logs
