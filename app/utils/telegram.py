"""
Telegram notification helper - outbound only, no webhook.
Requires: pip install requests
Env vars: TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_CHAT_ID
"""
import html
import logging
import os
from datetime import datetime, timezone

import requests

logger = logging.getLogger(__name__)

_TG_API = "https://api.telegram.org/bot{token}/{method}"


def _escape_limited(value: str, limit: int) -> str:
    escaped = []
    length = 0
    for character in value:
        safe_character = html.escape(character)
        char_length = len(safe_character.encode("utf-16-le")) // 2
        if length + char_length > limit - 3:
            return "".join(escaped) + "..."
        escaped.append(safe_character)
        length += char_length
    return "".join(escaped)


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
    timestamp = datetime.now(timezone.utc).strftime(
        "%d %b %Y · %H:%M UTC"
    )

    safe_type = _escape_limited(item_type or "Upload", 100)
    safe_title = _escape_limited(title or "(untitled)", 600)
    safe_uploader = _escape_limited(uploader or "Unknown", 120)

    heavy = "═" * 31
    light = "─" * 31

    lines = [
        f"<code>{heavy}</code>",
        "      <b>ACADEMX / NEW SUBMISSION</b>",
        f"<code>{heavy}</code>",
        "",
        "          [^_^]  <i>UPLOAD DETECTED</i>",
        "",
        f"  <b>» Category</b>    <code>{safe_type}</code>",
        "",
        f"  <b>» Title</b>",
        f"  <b>{safe_title}</b>",
        "",
        f"  <b>» Submitted By</b>  <code>{safe_uploader}</code>",
        f"  <b>» Received</b>      <code>{timestamp}</code>",
        "",
        f"<code>{light}</code>",
        "  <code>[ STATUS: SUCCESSFUL ]</code>",
        "",
        "  <i>New material has entered the system.</i>",
    ]

    if link:
        safe_link = html.escape(link, quote=True)
        lines.extend([
            "",
            f'  → <a href="{safe_link}"><b>OPEN ADMIN PANEL</b></a>',
        ])

    lines.extend([
        "",
        "  <i>AcademX Notification System</i>",
        "  <code>(⌐■_■)  Submission logged.</code>",
    ])

    return send_telegram_message("\n".join(lines))




def notify_question(
    asker: str,
    title: str,
    body: str,
    link: str | None = None,
) -> bool:
    timestamp = datetime.now(timezone.utc).strftime(
        "%d %b %Y · %H:%M UTC"
    )

    safe_asker = _escape_limited(asker or "Unknown", 120)
    safe_title = _escape_limited(title or "(untitled)", 600)
    escaped_body = _escape_limited(
        body or "(no details provided)", 2200
    )

    heavy = "═" * 31
    light = "─" * 31

    lines = [
        f"<code>{heavy}</code>",
        "   <b>ACADEMX  /  INCOMING QUESTION</b>",
        f"<code>{heavy}</code>",
        "",
        "       ¯\_(ツ)_/¯",
        "",
        f"  <b>» {safe_title}</b>",
        "",
        f"<blockquote>{escaped_body}</blockquote>",
        "",
        f"  <b>» Asked By</b>   <code>{safe_asker}</code>",
        f"  <b>» Received</b>   <code>{timestamp}</code>",
        "",
        f"<code>{light}</code>",
        "  <i>Another question just landed.</i>",
        "",
        "  <code>[ SYSTEM: QUESTION RECEIVED ]</code>",
    ]

    if link:
        safe_link = html.escape(link, quote=True)
        lines.extend([
            "",
            f'  → <a href="{safe_link}"><b>OPEN ADMIN PANEL</b></a>',
        ])

    lines.extend([
        "",
        "  <i>AcademX Notification System</i>",
        "  <code>(•_•)  Stay curious.</code>",
    ])

    return send_telegram_message("\n".join(lines))



def notify_signin(user_id, department, link=None):
    timestamp = datetime.now(timezone.utc).strftime(
        "%d %b %Y · %H:%M UTC"
    )

    safe_user = _escape_limited(user_id or "Unknown", 100)
    safe_department = _escape_limited(department or "Unknown", 150)

    separator = "━━━━━━━━━━━━━━━━━━━━━━━━"

    lines = [
        f"<b>ACADEMX | USER ACTIVITY</b>",
        f"<code>{separator}</code>",
        "",
        "<b>[ NEW SIGN-IN ]</b>",
        "",
        f"<b>User ID</b>       <code>{safe_user}</code>",
        f"<b>Department</b>    <code>{safe_department}</code>",
        f"<b>Timestamp</b>    <code>{timestamp}</code>",
        "",
        f"<code>{separator}</code>",
        "<b>STATUS:</b> <code>SUCCESSFUL</code>",
        "",
        "<i>AcademX Notification System</i>",
    ]

    if link:
        safe_link = html.escape(link, quote=True)
        lines.extend([
            "",
            f'<a href="{safe_link}">[ OPEN ADMIN DASHBOARD ]</a>'
        ])

    return send_telegram_message("\n".join(lines))
