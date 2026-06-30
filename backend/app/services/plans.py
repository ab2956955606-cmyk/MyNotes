from datetime import date as date_type
from datetime import datetime
from uuid import uuid4

from ..db import get_conn
from ..errors import bad_request, not_found
from ..schemas import PlanCreate, PlanOut, PlanUpdate


def _normalize_date(value: str) -> str:
    try:
        return date_type.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise bad_request("date must use YYYY-MM-DD format") from exc


def _normalize_time(value: str) -> str:
    try:
        return datetime.strptime(value, "%H:%M").strftime("%H:%M")
    except ValueError as exc:
        raise bad_request("time must use HH:MM format") from exc


def _normalize_content(content: str | None, title: str | None) -> str:
    value = (content or title or "").strip()
    if not value:
        raise bad_request("plan content cannot be empty")
    return value


def _normalize_result(result: str | None, completion: str | None) -> str:
    return result if result is not None else completion or ""


def _to_plan(row) -> PlanOut:
    return PlanOut(
        id=row["id"],
        date=row["date"],
        time=row["time"],
        content=row["content"],
        done=bool(row["done"]),
        result=row["result"],
        priority=row["priority"],
        estimatedMinutes=row["estimated_minutes"],
        source=row["source"],
        createdAt=row["created_at"],
        updatedAt=row["updated_at"],
    )


def list_plans(plan_date: str) -> list[PlanOut]:
    normalized_date = _normalize_date(plan_date)
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM plans
            WHERE date = ?
            ORDER BY time ASC, created_at ASC
            """,
            (normalized_date,),
        ).fetchall()
    return [_to_plan(row) for row in rows]


def create_plan(payload: PlanCreate) -> PlanOut:
    normalized_date = _normalize_date(payload.date)
    normalized_time = _normalize_time(payload.time)
    content = _normalize_content(payload.content, payload.title)
    result = _normalize_result(payload.result, payload.completion)
    plan_id = str(uuid4())
    with get_conn() as conn:
        row = conn.execute(
            """
            INSERT INTO plans(
              id, date, time, content, done, result, priority, estimated_minutes, source
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING *
            """,
            (
                plan_id,
                normalized_date,
                normalized_time,
                content,
                int(payload.done),
                result,
                payload.priority,
                payload.estimated_minutes,
                payload.source,
            ),
        ).fetchone()
    return _to_plan(row)


def update_plan(plan_id: str, payload: PlanUpdate) -> PlanOut:
    updates: dict[str, object] = {}
    if payload.date is not None:
        updates["date"] = _normalize_date(payload.date)
    if payload.time is not None:
        updates["time"] = _normalize_time(payload.time)
    if payload.content is not None or payload.title is not None:
        updates["content"] = _normalize_content(payload.content, payload.title)
    if payload.done is not None:
        updates["done"] = int(payload.done)
    if payload.result is not None or payload.completion is not None:
        updates["result"] = _normalize_result(payload.result, payload.completion)
    if payload.priority is not None:
        updates["priority"] = payload.priority
    if payload.estimated_minutes is not None:
        updates["estimated_minutes"] = payload.estimated_minutes
    if payload.source is not None:
        updates["source"] = payload.source

    with get_conn() as conn:
        exists = conn.execute("SELECT id FROM plans WHERE id = ?", (plan_id,)).fetchone()
        if not exists:
            raise not_found("plan does not exist")
        if updates:
            assignments = ", ".join(f"{field} = ?" for field in updates)
            conn.execute(
                f"""
                UPDATE plans
                SET {assignments}, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (*updates.values(), plan_id),
            )
        row = conn.execute("SELECT * FROM plans WHERE id = ?", (plan_id,)).fetchone()
    return _to_plan(row)


def delete_plan(plan_id: str) -> None:
    with get_conn() as conn:
        cursor = conn.execute("DELETE FROM plans WHERE id = ?", (plan_id,))
        if cursor.rowcount == 0:
            raise not_found("plan does not exist")
