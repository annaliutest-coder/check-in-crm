import os
import csv
import io
import json
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


def parse_tags(tags_str: str) -> list[str]:
    """Parse JSON tags string to list."""
    try:
        return json.loads(tags_str) if tags_str else []
    except:
        return []


def serialize_tags(tags: list[str]) -> str:
    """Serialize tags list to JSON string."""
    return json.dumps(tags, ensure_ascii=False)


@router.post("/check-in", response_model=CheckInResponse)
async def check_in_user(
    request: CheckInRequest,
    background_tasks: BackgroundTasks
):
    """
    Check in a user for the event.
    """
    existing_user = await db.user.find_unique(where={"email": request.email})

    is_new_user = existing_user is None
    email_sent = False
    event_name = get_event_name()

    if existing_user:
        # Update existing user
        current_tags = parse_tags(existing_user.tags)
        if event_name not in current_tags:
            current_tags.append(event_name)

        update_data = {"tags": serialize_tags(current_tags)}
        if request.name:
            update_data["name"] = request.name
        if request.phone:
            update_data["phone"] = request.phone

        user = await db.user.update(
            where={"id": existing_user.id},
            data=update_data
        )
        message = "歡迎回來！已更新您的資料。"
    else:
        # Create new user
        user = await db.user.create(
            data={
                "email": request.email,
                "name": request.name,
                "phone": request.phone,
                "tags": serialize_tags([event_name])
            }
        )
        message = "打卡成功！歡迎加入！"

    # Create EventLog
    await db.eventlog.create(
        data={
            "eventName": event_name,
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

    # Parse tags for each user
    result = []
    for user in users:
        user_dict = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "phone": user.phone,
            "tags": parse_tags(user.tags),
            "createdAt": user.createdAt,
            "logs": user.logs
        }
        result.append(user_dict)

    return result


@router.get("/event")
async def get_event():
    """Get current event info."""
    return {"event_name": get_event_name()}


@router.get("/stats")
async def get_stats():
    """Get check-in statistics."""
    total_users = await db.user.count()
    total_checkins = await db.eventlog.count()
    event_checkins = await db.eventlog.count(
        where={"eventName": get_event_name()}
    )

    return {
        "total_users": total_users,
        "total_checkins": total_checkins,
        "event_checkins": event_checkins
    }


@router.get("/tags")
async def get_all_tags():
    """Get all unique tags from users."""
    users = await db.user.find_many()
    all_tags = set()
    for user in users:
        tags = parse_tags(user.tags)
        all_tags.update(tags)
    return sorted(list(all_tags))


@router.get("/export/csv")
async def export_users_csv(
    tag: str = Query(default=None, description="篩選特定標籤的用戶")
):
    """Export users to CSV file."""
    users = await db.user.find_many(order={"createdAt": "desc"})

    # Filter by tag if specified
    if tag:
        users = [u for u in users if tag in parse_tags(u.tags)]

    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Email", "姓名", "電話", "標籤", "建立時間"])

    for user in users:
        tags = parse_tags(user.tags)
        writer.writerow([
            user.email,
            user.name or "",
            user.phone or "",
            ", ".join(tags),
            user.createdAt.strftime("%Y-%m-%d %H:%M:%S") if user.createdAt else ""
        ])

    output.seek(0)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"users_export_{timestamp}.csv"

    bom = '\ufeff'
    content = bom + output.getvalue()

    return StreamingResponse(
        iter([content]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
