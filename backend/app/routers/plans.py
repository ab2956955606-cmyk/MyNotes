from fastapi import APIRouter

from ..schemas import PlanCreate, PlanOut, PlanUpdate
from ..services.plans import create_plan, delete_plan, list_plans, update_plan

router = APIRouter(prefix="/api/plans", tags=["plans"])


@router.get("", response_model=list[PlanOut])
def get_plans(date: str) -> list[PlanOut]:
    return list_plans(date)


@router.post("", response_model=PlanOut)
def post_plan(payload: PlanCreate) -> PlanOut:
    return create_plan(payload)


@router.patch("/{plan_id}", response_model=PlanOut)
def patch_plan(plan_id: str, payload: PlanUpdate) -> PlanOut:
    return update_plan(plan_id, payload)


@router.delete("/{plan_id}", status_code=204)
def remove_plan(plan_id: str) -> None:
    delete_plan(plan_id)
