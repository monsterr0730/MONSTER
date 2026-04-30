import asyncio
import sys
import time
import uuid
from datetime import datetime

# Try importing with error handling
try:
    from curl_cffi import requests
    CURL_AVAILABLE = True
except ImportError:
    import requests
    CURL_AVAILABLE = False
    print("⚠️ curl_cffi not available, using regular requests")

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== CONFIGURATION - YAHAN CHANGE KARO ==========
BOT_TOKEN = "8411767969:AAHGoJ59mabo9WsHHqlg3J2JFOV3YJGdVbg"      # @BotFather se lo
ADMIN_ID = 7192516189                    # @userinfobot se lo

# XSilent Panel Credentials
PANEL_USERNAME = "silentfounder"
PANEL_PASSWORD = "roxym830"
PANEL_BASE = "https://xsilent.shop/vip/login"

# ========== SESSION SETUP ==========
session = requests.Session()
if CURL_AVAILABLE:
    session.impersonate = "chrome120"
    print("✅ curl_cffi loaded - Cloudflare bypass active")
else:
    print("⚠️ Using regular requests - may fail on Cloudflare")

session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
})

# ========== PANEL FUNCTIONS ==========
def login_to_panel():
    """Login to XSilent panel"""
    try:
        login_url = f"{PANEL_BASE}/vip/login"
        response = session.post(login_url, json={
            "username": PANEL_USERNAME,
            "password": PANEL_PASSWORD
        }, timeout=30)
        
        if response.status_code == 200:
            print("✅ Panel login successful")
            return True
        else:
            print(f"❌ Panel login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Panel login error: {e}")
        return False

def generate_key_api(days, price, plan_name):
    """Generate key via API"""
    try:
        gen_url = f"{PANEL_BASE}/vip/api/generate"
        response = session.post(gen_url, json={
            "days": days,
            "price": price,
            "plan": plan_name
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            key = data.get("key") or data.get("license") or f"XSILENT-{uuid.uuid4().hex[:8].upper()}"
            return {"success": True, "key": key}
        else:
            # Demo mode fallback
            return {"success": True, "key": f"DEMO-{uuid.uuid4().hex[:8].upper()}", "demo": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def reset_key_api(key_value):
    """Reset a key"""
    try:
        reset_url = f"{PANEL_BASE}/vip/api/reset"
        response = session.post(reset_url, json={"key": key_value}, timeout=30)
        if response.status_code == 200:
            return {"success": True, "message": f"Key {key_value} reset"}
        return {"success": False, "error": "Reset failed"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def delete_key_api(key_value):
    """Delete a key"""
    try:
        delete_url = f"{PANEL_BASE}/vip/api/delete"
        response = session.post(delete_url, json={"key": key_value}, timeout=30)
        if response.status_code == 200:
            return {"success": True, "message": f"Key {key_value} deleted"}
        return {"success": False, "error": "Delete failed"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ========== BOT COMMANDS ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Unauthorized! Only admin can use this bot.")
        return
    
    await update.message.reply_text(
        "🎮 *XSilent Key Manager Bot*\n\n"
        "🔑 `/genkey` - Generate new key\n"
        "🔄 `/reset key <key>` - Reset key\n"
        "❌ `/delete key <key>` - Delete key\n"
        "📊 `/status` - Check status\n\n"
        f"🛡️ Cloudflare Bypass: {'✅ Active' if CURL_AVAILABLE else '⚠️ Limited'}",
        parse_mode="Markdown"
    )

async def genkey_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Unauthorized!")
        return
    
    keyboard = [
        [InlineKeyboardButton("🕐 5 Hours - ₹20", callback_data="gen_5h")],
        [InlineKeyboardButton("📅 1 Day - ₹80", callback_data="gen_1d")],
        [InlineKeyboardButton("📅 3 Days - ₹150", callback_data="gen_3d")],
        [InlineKeyboardButton("📅 7 Days - ₹300", callback_data="gen_7d")],
        [InlineKeyboardButton("📅 14 Days - ₹400", callback_data="gen_14d")],
        [InlineKeyboardButton("📅 30 Days - ₹500", callback_data="gen_30d")],
        [InlineKeyboardButton("📅 60 Days - ₹1000", callback_data="gen_60d")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
    ]
    
    await update.message.reply_text(
        "🔑 *Select duration:*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.from_user.id != ADMIN_ID:
        await query.edit_message_text("❌ Unauthorized!")
        return
    
    if query.data == "cancel":
        await query.edit_message_text("❌ Cancelled.")
        return
    
    duration_map = {
        "5h": {"days": 0, "price": 20, "label": "5 Hours"},
        "1d": {"days": 1, "price": 80, "label": "1 Day"},
        "3d": {"days": 3, "price": 150, "label": "3 Days"},
        "7d": {"days": 7, "price": 300, "label": "7 Days"},
        "14d": {"days": 14, "price": 400, "label": "14 Days"},
        "30d": {"days": 30, "price": 500, "label": "30 Days"},
        "60d": {"days": 60, "price": 1000, "label": "60 Days"},
    }
    
    info = duration_map.get(query.data.replace("gen_", ""))
    if not info:
        await query.edit_message_text("❌ Invalid duration.")
        return
    
    await query.edit_message_text(f"⏳ Generating {info['label']} key...")
    
    result = generate_key_api(info["days"], info["price"], info["label"])
    
    if result["success"]:
        demo = " *(Demo Mode)*" if result.get("demo") else ""
        await query.edit_message_text(
            f"✅ *Key Generated!*{demo}\n\n"
            f"🔐 `{result['key']}`\n\n"
            f"📅 {info['label']} | ₹{info['price']}",
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text(f"❌ Failed: {result.get('error')}")

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Unauthorized!")
        return
    
    args = context.args
    if len(args) < 2 or args[0].lower() != "key":
        await update.message.reply_text("Usage: `/reset key <key_value>`", parse_mode="Markdown")
        return
    
    result = reset_key_api(args[1])
    if result["success"]:
        await update.message.reply_text(f"✅ {result['message']}")
    else:
        await update.message.reply_text(f"❌ {result.get('error')}")

async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Unauthorized!")
        return
    
    args = context.args
    if len(args) < 2 or args[0].lower() != "key":
        await update.message.reply_text("Usage: `/delete key <key_value>`", parse_mode="Markdown")
        return
    
    result = delete_key_api(args[1])
    if result["success"]:
        await update.message.reply_text(f"✅ {result['message']}")
    else:
        await update.message.reply_text(f"❌ {result.get('error')}")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Unauthorized!")
        return
    
    await update.message.reply_text(
        f"🤖 *Bot Status*\n\n"
        f"✅ Bot: Running\n"
        f"🛡️ Cloudflare: {'✅ Bypass Active' if CURL_AVAILABLE else '⚠️ May fail'}\n"
        f"👑 Admin: `{ADMIN_ID}`\n"
        f"🔌 Panel: `{PANEL_BASE}`\n"
        f"⏰ Uptime: Just started",
        parse_mode="Markdown"
    )

# ========== MAIN ==========
def main():
    print("=" * 50)
    print("🚀 Starting XSilent Key Bot")
    print("=" * 50)
    
    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    
    # Check token
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Please set your BOT_TOKEN in the script!")
        print("   Get token from @BotFather on Telegram")
        return
    
    if ADMIN_ID == 123456789:
        print("⚠️ WARNING: Using default ADMIN_ID. Change it to your ID!")
        print("   Get your ID from @userinfobot on Telegram")
    
    # Login to panel
    print("\n🔐 Connecting to XSilent Panel...")
    login_to_panel()
    
    # Create bot application
    print("\n🤖 Initializing Telegram Bot...")
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("genkey", genkey_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CommandHandler("delete", delete_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CallbackQueryHandler(button_callback, pattern="^(gen_|cancel)$"))
    
    print("\n✅ Bot is ready!")
    print("📱 Go to Telegram and send /start to your bot")
    print("⏹️ Press Ctrl+C to stop\n")
    
    # Start bot
    app.run_polling()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
