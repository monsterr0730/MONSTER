import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ---------- CONFIG ----------
BOT_TOKEN = "8776136132:AAH6g4433xIXO9IhTCtfqPWb2UOik6t5MQ8"
ADMIN_ID = 7857797639  # Your Telegram ID
CHANNEL_LINK = "https://t.me/+YerutxCoLJE1OWI1"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- UNAUTHORIZED MESSAGE (Always shows for restricted commands) ----------
async def unauthorized(update: Update) -> None:
    await update.message.reply_text(
        f"╔══════════════════════════════════╗\n"
        f"║     🔴 ACCESS DENIED 🔴          ║\n"
        f"╠══════════════════════════════════╣\n"
        f"║  ❌ SORRY, YOU ARE NOT           ║\n"
        f"║  AUTHORIZED TO USE THIS COMMAND  ║\n"
        f"╠══════════════════════════════════╣\n"
        f"║  📌 FIRST JOIN OUR CHANNEL:      ║\n"
        f"║  ☑️ {CHANNEL_LINK}  ║\n"
        f"╚══════════════════════════════════╝",
        parse_mode='HTML'
    )

# ---------- /start (Always works - Welcome) ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_msg = (
        f"🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟\n"
        f"⚡ 𝑽𝑵 𝒙 𝑴𝑨𝑮𝑮𝑰 𝐌𝐈𝐀 𝐊𝐇𝐀𝐋𝐈𝐅𝐀 𝐃𝐃𝐎𝐒 ⚡\n"
        f"🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟\n\n"
        f"🔥🔥🔥 WELCOME {user.first_name} 🔥🔥🔥\n\n"
        f"💣 ━━━━━━━━━━━━━━━━━━━━━━━ 💣\n"
        f"     Layer‑4 Stress Testing Power\n"
        f"💣 ━━━━━━━━━━━━━━━━━━━━━━━ 💣\n\n"
        f"👑 𝙾𝚠𝚗𝚎𝚛: {CHANNEL_LINK}\n\n"
        f"📜 ━━━━━━━━━━━━━━━━━━━━━━━ 📜\n"
        f"     ✅ <b>𝐏𝐔𝐁𝐋𝐈𝐂 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒</b> ✅\n"
        f"📜 ━━━━━━━━━━━━━━━━━━━━━━━ 📜\n\n"
        f"🎯 /attack &lt;IP&gt; &lt;PORT&gt; &lt;TIME&gt;\n"
        f"     └─ Launch attack (max 240s)\n\n"
        f"🤖 /botstatus\n"
        f"     └─ Check bot mode\n\n"
        f"✅ /verify\n"
        f"     └─ Re‑check channel membership\n\n"
        f"❓ /help\n"
        f"     └─ Show this menu\n\n"
        f"⚠️━━━━━━━━━━━━━━━━━━━━━━━⚠️\n"
        f"  Use only on your own infrastructure\n"
        f"⚠️━━━━━━━━━━━━━━━━━━━━━━━⚠️"
    )
    await update.message.reply_text(welcome_msg, parse_mode='HTML')

# ---------- /help (Shows unauthorized message) ----------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await unauthorized(update)

# ---------- /attack (Only shows unauthorized message - NO DEMO) ----------
async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await unauthorized(update)

# ---------- /botstatus (Shows unauthorized message) ----------
async def botstatus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await unauthorized(update)

# ---------- /verify (Shows unauthorized message) ----------
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await unauthorized(update)

# ---------- MAIN ----------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("attack", attack))
    app.add_handler(CommandHandler("botstatus", botstatus))
    app.add_handler(CommandHandler("verify", verify))

    logger.info("🚀 Bot started successfully!")
    logger.info(f"📢 Channel link: {CHANNEL_LINK}")
    app.run_polling()

if __name__ == "__main__":
    main()
