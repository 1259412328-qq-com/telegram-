# scripts/send_signin.py
import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def main():
    session_str = os.environ.get("TG_SESSION_STRING")
    api_id = os.environ.get("TG_API_ID")
    api_hash = os.environ.get("TG_API_HASH")
    target = os.environ.get("TARGET_USERNAME", "@QingBaoJuXuanwubot")
    message = os.environ.get("SIGN_MESSAGE", "📅 签到")

    if not session_str:
        raise SystemExit("Missing TG_SESSION_STRING (set as GitHub Secret).")
    if not api_id or not api_hash:
        raise SystemExit("Missing TG_API_ID or TG_API_HASH (set as GitHub Secrets).")

    api_id = int(api_id)

    async with TelegramClient(StringSession(session_str), api_id, api_hash) as client:
        # 确保目标存在（对 username 或者 @username 都能工作）
        try:
            entity = await client.get_entity(target)
        except Exception:
            # 直接发送也行（Telethon 会抛错时尝试用字符串）
            entity = target
        await client.send_message(entity, message)
        print(f"Sent message to {target!s}: {message!s}")

if __name__ == "__main__":
    asyncio.run(main())
