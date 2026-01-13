import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from app.db import db
from app.gmail import send_email

scheduler = AsyncIOScheduler(timezone="Asia/Taipei")


async def execute_scheduled_email(scheduled_email_id: str):
    """
    Execute a scheduled email task.
    Send emails to all users matching the target tags.
    """
    print(f"[Scheduler] Executing scheduled email: {scheduled_email_id}")

    try:
        # Get the scheduled email task
        task = await db.scheduledemail.find_unique(
            where={"id": scheduled_email_id}
        )

        if not task:
            print(f"[Scheduler] Task not found: {scheduled_email_id}")
            return

        if task.status != "pending":
            print(f"[Scheduler] Task already processed: {task.status}")
            return

        # Find users with matching tags
        users = await db.user.find_many(
            where={
                "tags": {"has_every": task.targetTags}
            } if task.targetTags else {}
        )

        print(f"[Scheduler] Found {len(users)} users to send email")

        sent_count = 0
        failed_count = 0

        for user in users:
            # Personalize content
            personalized_content = task.htmlContent.replace(
                "{{name}}", user.name or "朋友"
            ).replace(
                "{{email}}", user.email
            )

            success = await send_email(
                to_email=user.email,
                subject=task.subject,
                html_content=personalized_content,
                name=user.name
            )

            # Log the email
            await db.emaillog.create(
                data={
                    "userId": user.id,
                    "emailType": "scheduled_notification",
                    "subject": task.subject,
                    "status": "sent" if success else "failed",
                    "error": None if success else "Failed to send"
                }
            )

            if success:
                sent_count += 1
            else:
                failed_count += 1

        # Update task status
        await db.scheduledemail.update(
            where={"id": scheduled_email_id},
            data={
                "status": "sent",
                "sentAt": datetime.now(),
                "sentCount": sent_count,
                "failedCount": failed_count
            }
        )

        print(f"[Scheduler] Email task completed: {sent_count} sent, {failed_count} failed")

    except Exception as e:
        print(f"[Scheduler] Error executing task: {e}")
        await db.scheduledemail.update(
            where={"id": scheduled_email_id},
            data={
                "status": "failed",
                "failedCount": -1  # Indicates system error
            }
        )


def schedule_email_task(task_id: str, scheduled_time: datetime):
    """
    Add a new email task to the scheduler.
    """
    job_id = f"email_{task_id}"

    # Remove existing job if any
    existing_job = scheduler.get_job(job_id)
    if existing_job:
        scheduler.remove_job(job_id)

    # Schedule the new job
    scheduler.add_job(
        lambda: asyncio.create_task(execute_scheduled_email(task_id)),
        trigger=DateTrigger(run_date=scheduled_time),
        id=job_id,
        name=f"Scheduled Email: {task_id}",
        replace_existing=True
    )

    print(f"[Scheduler] Scheduled email task: {task_id} at {scheduled_time}")


def cancel_email_task(task_id: str):
    """
    Cancel a scheduled email task.
    """
    job_id = f"email_{task_id}"
    try:
        scheduler.remove_job(job_id)
        print(f"[Scheduler] Cancelled email task: {task_id}")
        return True
    except Exception as e:
        print(f"[Scheduler] Failed to cancel task: {e}")
        return False


async def restore_pending_tasks():
    """
    Restore pending scheduled tasks from database on startup.
    """
    pending_tasks = await db.scheduledemail.find_many(
        where={
            "status": "pending",
            "scheduledAt": {"gt": datetime.now()}
        }
    )

    for task in pending_tasks:
        schedule_email_task(task.id, task.scheduledAt)

    print(f"[Scheduler] Restored {len(pending_tasks)} pending tasks")


def start_scheduler():
    """Start the scheduler."""
    if not scheduler.running:
        scheduler.start()
        print("[Scheduler] Started")


def shutdown_scheduler():
    """Shutdown the scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        print("[Scheduler] Shutdown")
