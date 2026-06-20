from __future__ import annotations

import argparse
import json
import os
import sys
from urllib import request

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv не установлен, используем системные переменные окружения


def main() -> int:
    parser = argparse.ArgumentParser(description="Configure Telegram webhook.")
    parser.add_argument("--token", default=os.getenv("TELEGRAM_BOT_TOKEN"))
    parser.add_argument("--url", default=os.getenv("TELEGRAM_WEBHOOK_URL"))
    parser.add_argument("--secret", default=os.getenv("TELEGRAM_WEBHOOK_SECRET"))
    parser.add_argument("--drop-pending-updates", action="store_true")
    args = parser.parse_args()

    if not args.token:
        print("TELEGRAM_BOT_TOKEN is required.", file=sys.stderr)
        return 2
    if not args.url:
        print("TELEGRAM_WEBHOOK_URL or --url is required.", file=sys.stderr)
        return 2
    if not args.url.startswith("https://"):
        print("Telegram webhook URL must be public HTTPS.", file=sys.stderr)
        return 2

    payload: dict[str, object] = {
        "url": args.url,
        "allowed_updates": ["message"],
        "drop_pending_updates": args.drop_pending_updates,
    }
    if args.secret:
        payload["secret_token"] = args.secret

    api_url = f"https://api.telegram.org/bot{args.token}/setWebhook"
    body = json.dumps(payload).encode("utf-8")
    http_request = request.Request(
        api_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with request.urlopen(http_request, timeout=30) as response:
        response_body = response.read().decode("utf-8")
        print(response_body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
