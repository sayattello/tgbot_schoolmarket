from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import json

app = FastAPI()

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Bot handlers (same as in Colab)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot running on Vercel!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

# Webhook endpoint
@app.post("/webhook")
async def webhook(request: Request):
    if not TOKEN:
        return {"error": "Bot token not configured"}
    
    # Get update from request
    data = await request.json()
    update = Update.de_json(data, None)
    
    # Build application
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Process update
    await application.process_update(update)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "Bot is running on Vercel!"}
