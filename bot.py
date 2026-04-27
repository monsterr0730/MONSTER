import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ---------- CONFIG ----------
BOT_TOKEN = "8411767969:AAHGoJ59mabo9WsHHqlg3J2JFOV3YJGdVbg"
ADMIN_ID = 7192516189  # Your Telegram ID
CHANNEL_LINK = "https://t.me/+ndCYGs-yIuQ1M2U1"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- UNAUTHORIZED MESSAGE (Always shows for restricted commands) ----------
async def unauthorized(update: Update) -> None:
    await update.message.reply_text(
        f"🔴SORRY , YOU ARE NOT AUTHORIZED TO USE THIS COMMAND🔴\n\n"
        f"FIRST JOIN☑️\n{CHANNEL_LINK}",
        parse_mode='HTML'
    )

# ---------- /start (Always works - Welcome) ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_msg = (
        f"⚡ 𝑽𝑵 𝒙 𝑴𝑨𝑮𝑮𝑰 ⚡\n\n"
        f"🔥 Welcome {user.first_name},\n"
        f"💣 Layer‑4 Stress Testing Power\n\n"
        f"👑 Owner: https://t.me/+ndCYGs-yIuQ1M2U1\n\n"
        f"✅ <b>Public Commands:</b>\n"
        f"• /attack &lt;IP&gt; &lt;PORT&gt; &lt;TIME&gt; – Launch attack (max 240s)\n"
        f"• /botstatus – Check bot mode\n"
        f"• /verify – Re‑check channel membership\n"
        f"• /changelink &lt;new_link&gt; – Owner only: Change required channel link\n"
        f"• /help – Show this menu\n\n"
        f"⚠️ Use only on your own infrastructure"
    )
    await update.message.reply_text(welcome_msg, parse_mode='HTML')

# ---------- /help (Shows after unauthorized message) ----------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await unauthorized(update)

# ---------- /attack (Shows unauthorized message + demo) ----------
async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await unauthorized(update)
    
    # Still show demo attack for promotion
    args = context.args
    if len(args) == 3:
        ip, port, duration = args
        await update.message.reply_text(
            f"🚀 <b>Demo Attack (Promotional Only)</b> 🚀\n\n"
            f"Target: {ip}:{port}\n"
            f"Duration: {duration}s\n\n"
            f"🔥 Join channel first to use real features!\n{CHANNEL_LINK}",
            parse_mode='HTML'
        )

# ---------- /botstatus (Shows unauthorized message) ----------
async def botstatus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await unauthorized(update)

# ---------- /verify (Shows unauthorized message) ----------
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await unauthorized(update)

# ---------- /changelink (Owner Only - Changes the channel link) ----------
async def changelink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Check if user is owner
    if user_id != ADMIN_ID:
        await update.message.reply_text("🔴 Only the bot owner can change the channel link.")
        return
    
    args = context.args
    if len(args) != 1:
        await update.message.reply_text(
            "⚠️ Usage: /changelink <new_channel_link>\n"
            "Example: /changelink https://t.me/+newinvitecode"
        )
        return
    
    global CHANNEL_LINK
    old_link = CHANNEL_LINK
    new_link = args[0]
    
    # Basic validation
    if not (new_link.startswith("https://t.me/") or new_link.startswith("http://t.me/")):
        await update.message.reply_text("❌ Invalid link. Use format: https://t.me/+invitecode")
        return
    
    CHANNEL_LINK = new_link
    
    await update.message.reply_text(
        f"✅ Channel link updated successfully!\n\n"
        f"📌 Old link: {old_link}\n"
        f"📌 New link: {new_link}",
        parse_mode='HTML'
    )
    
    # Save to file
    try:
        with open("channel_link.txt", "w") as f:
            f.write(new_link)
        await update.message.reply_text("💾 Link saved for next restart.")
    except:
        pass

# ---------- LOAD SAVED LINK ON STARTUP ----------
def load_saved_link():
    global CHANNEL_LINK
    try:
        with open("channel_link.txt", "r") as f:
            saved_link = f.read().strip()
            if saved_link:
                CHANNEL_LINK = saved_link
                logger.info(f"Loaded saved channel link: {CHANNEL_LINK}")
    except FileNotFoundError:
        logger.info("No saved link found, using default.")

# ---------- MAIN ----------
def main():
    load_saved_link()
    
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("attack", attack))
    app.add_handler(CommandHandler("botstatus", botstatus))
    app.add_handler(CommandHandler("verify", verify))
    app.add_handler(CommandHandler("changelink", changelink))

    logger.info("Bot started (PROMOTIONAL MODE - No membership verification)")
    logger.info(f"Current channel link: {CHANNEL_LINK}")
    app.run_polling()

if __name__ == "__main__":
    main()
