import os
import csv
import io
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Query
from fastapi.responses import StreamingResponse

from app.db import db
from app.schemas import CheckInRequest, CheckInResponse
from app.gmail import send_welcome_email

router = APIRouter()


def get_event_name() -> str:
    """Get current event name from environment variable."""
    return os.getenv("EVENT_NAME", "2026春季招生活動")


@router.post("/check-in", response_model=CheckInResponse)
async def check_in_user(
    request: CheckInRequest,
    background_tasks: BackgroundTasks
):
    """
    Check in a user for the event.

    - If user exists: Update tags and info
    - If user doesn't exist: Create new user
    - Create EventLog entry
    - Optionally send welcome email
    """
    # Check if user exists
    existing_user = await db.user.find_unique(where={"email": request.email})

    is_new_user = existing_user is None
    email_sent = False

    if existing_user:
        # Update existing user
        event_name = get_event_name()
        new_tags = existing_user.tags.copy() if existing_user.tags else []
        if event_name not in new_tags:
            new_tags.append(event_name)

        update_data = {"tags": new_tags}
        if request.name:
            update_data["name"] = request.name
        if request.phone:
            update_data["phone"] = request.phone

        user = await db.user.update(
            where={"id": existing_user.id},
            data=update_data
        )
        message = f"歡迎回來！已更新您的資料。"
    else:
        # Create new user
        event_name = get_event_name()
        user = await db.user.create(
            data={
                "email": request.email,
                "name": request.name,
                "phone": request.phone,
                "tags": [event_name]
            }
        )
        message = "打卡成功！歡迎加入！"

    # Create EventLog
    await db.eventlog.create(
        data={
            "eventName": get_event_name(),
            "userId": user.id
        }
    )

    # Send welcome email in background if requested
    if request.send_email:
        background_tasks.add_task(send_welcome_email, request.email, request.name)
        email_sent = True

    return CheckInResponse(
        success=True,
        message=message,
        is_new_user=is_new_user,
        email_sent=email_sent
    )


@router.get("/users")
async def get_users():
    """Get all users with their check-in logs."""
    users = await db.user.find_many(
        include={"logs": True},
        order={"createdAt": "desc"}
    )
    return users


@router.get("/event")
async def get_event():
    """Get current event info."""
    return {"event_name": get_event_name()}


@router.get("/stats")
async def get_stats():
    """Get check-in statistics."""
    total_users = await db.user.count()
    total_checkins = await db.eventlog.count()
    today_checkins = await db.eventlog.count(
        where={
            "eventName": get_event_name()
        }
    )

    return {
        "total_users": total_users,
        "total_checkins": total_checkins,
        "event_checkins": today_checkins
    }


@router.get("/export/csv")
async def export_users_csv(
    tag: str = Query(default=None, description="篩選特定標籤的用戶")
):
    """
    Export users to CSV file.
    Optionally filter by tag.
    """
    # Build query
    if tag:
        users = await db.user.find_many(
            where={"tags": {"has": tag}},
            order={"createdAt": "desc"}
        )
    else:
        users = await db.user.find_many(
            order={"createdAt": "desc"}
        )

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(["Email", "姓名", "電話", "標籤", "建立時間"])

    # Write data
    for user in users:
        writer.writerow([
            user.email,
            user.name or "",
            user.phone or "",
            ", ".join(user.tags) if user.tags else "",
            user.createdAt.strftime("%Y-%m-%d %H:%M:%S") if user.createdAt else ""
        ])

    # Prepare response
    output.seek(0)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"users_export_{timestamp}.csv"

    # Return as streaming response with BOM for Excel compatibility
    bom = '\ufeff'
    content = bom + output.getvalue()

    return StreamingResponse(
        iter([content]),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
