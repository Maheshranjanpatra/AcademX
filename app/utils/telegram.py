"""
Telegram notification helper - outbound only, no webhook.
Requires: pip install requests
Env vars: TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_CHAT_ID
"""
import html
import logging
import os
from datetime import datetime

import requests

logger = logging.getLogger(__name__)

_TG_API = "https://api.telegram.org/bot{token}/{method}"


def send_telegram_message(text: str, chat_id: str | None = None) -> bool:
    """Fire-and-forget. Never raises; returns True on success."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    target = chat_id or os.getenv("TELEGRAM_ADMIN_CHAT_ID")

    if not token or not target:
        logger.warning("Telegram: missing TELEGRAM_BOT_TOKEN or TELEGRAM_ADMIN_CHAT_ID")
        return False

    url = _TG_API.format(token=token, method="sendMessage")
    payload = {
        "chat_id": target,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return True
    except requests.RequestException as e:
        logger.error("Telegram send failed: %s", e)
        return False


def notify_upload(
    uploader: str,
    item_type: str,
    title: str,
    link: str | None = None,
) -> bool:
    timestamp = datetime.utcnow().strftime("%d %b %Y \u00b7 %H:%M UTC")

    safe_type     = html.escape(item_type or "Upload")
    safe_title    = html.escape(title or "(untitled)")
    safe_uploader = html.escape(uploader or "Unknown")

    heavy = "\u2550" * 31
    light = "\u2500" * 31

    lines = [
        f"<code>{heavy}</code>",
        " <b>NEW SUBMISSION</b>",
        f"<code>{heavy}</code>",
        "",
        f"\u2192 <code>{safe_type}</code>",
        "",
        f"\u2192 <b>{safe_title}</b>",
        "",
        f"\u2192 <b>Submitted By</b>  <code>{safe_uploader}</code>",
        f"  <b>Received</b>      <code>{timestamp}</code>",
        "",
        f"<code>{light}</code>",
    ]

    if link:
        safe_link = html.escape(link, quote=True)
        lines.append(f'\u2192 <a href="{safe_link}"><b>Open Admin Panel</b></a>')

    return send_telegram_message("\n".join(lines))
