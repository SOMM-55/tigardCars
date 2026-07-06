#!/usr/bin/env python3
"""
مدیریت progress بررسی پروژه — برای پشتیبانی از پروژه‌های بزرگ
و توانایی ادامه در session جدید.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


CHECKS = [
    "observability",
    "logging", 
    "security_network",
    "security_database",
    "security_app",
    "business_reporting",
    "api_standards",
    "documentation"
]


def init_progress(repo_path: str, output_dir: str) -> dict:
    """ایجاد فایل progress جدید"""
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    progress = {
        "session_id": session_id,
        "repo_path": repo_path,
        "output_dir": output_dir,
        "completed_checks": [],
        "pending_checks": CHECKS.copy(),
        "partial_results": {},
        "scores": {},
        "last_updated": datetime.now().isoformat(),
        "status": "in_progress"
    }
    save_progress(progress, output_dir)
    return progress


def load_progress(output_dir: str) -> dict | None:
    """بارگذاری progress موجود"""
    progress_file = Path(output_dir) / "audit-progress.json"
    if progress_file.exists():
        with open(progress_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def save_progress(progress: dict, output_dir: str):
    """ذخیره وضعیت فعلی"""
    progress["last_updated"] = datetime.now().isoformat()
    progress_file = Path(output_dir) / "audit-progress.json"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def mark_check_complete(progress: dict, check_name: str, 
                         results: dict, score: float, output_dir: str):
    """ثبت نتیجه یک check و بروزرسانی progress"""
    if check_name in progress["pending_checks"]:
        progress["pending_checks"].remove(check_name)
    if check_name not in progress["completed_checks"]:
        progress["completed_checks"].append(check_name)
    
    progress["partial_results"][check_name] = results
    progress["scores"][check_name] = score
    save_progress(progress, output_dir)
    print(f"✓ [{check_name}] امتیاز: {score:.1f} — ذخیره شد", file=sys.stderr)


def get_total_score(progress: dict) -> float:
    """محاسبه امتیاز کل از checks انجام‌شده"""
    weights = {
        "observability": 20,
        "logging": 20,
        "security_network": 15,
        "security_database": 15,
        "security_app": 15,
        "business_reporting": 10,
        "api_standards": 5,
        "documentation": 0  # bonus
    }
    total = 0
    for check, score in progress["scores"].items():
        weight = weights.get(check, 0)
        total += (score / 100) * weight
    return total


def print_progress_summary(progress: dict):
    """نمایش خلاصه progress"""
    print("\n" + "="*50)
    print(f"📊 وضعیت ممیزی: {progress['repo_path']}")
    print(f"Session: {progress['session_id']}")
    print("-"*50)
    
    completed = progress["completed_checks"]
    pending = progress["pending_checks"]
    
    print(f"✅ تکمیل‌شده ({len(completed)}): {', '.join(completed) if completed else 'هیچ'}")
    print(f"⏳ باقی‌مانده ({len(pending)}): {', '.join(pending) if pending else 'هیچ'}")
    
    if progress["scores"]:
        total = get_total_score(progress)
        print(f"\n💯 امتیاز فعلی: {total:.1f}/100")
    
    print("="*50 + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("استفاده: python progress_manager.py <output_dir> [--status]")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    progress = load_progress(output_dir)
    
    if progress:
        print_progress_summary(progress)
    else:
        print("فایل progress یافت نشد.")
