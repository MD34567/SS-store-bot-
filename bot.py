import os
from typing import Final
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("No TELEGRAM_TOKEN found")

BOT_USERNAME: Final = "@SS2_Store_bot"

PRODUCTS = {
    "1": {"name": "Dresses", "price": 1200, "link": "https://t.me/FG33333333/3"},
    "2": {"name": "Stokings", "price": 700, "link": "https://t.me/FG33333333/3"},
    "3": {"name": "Sleeve pitls", "price": 650, "link": "https://t.me/sel8299/611"},
    "4": {"name": "Hair clip 5 piece", "price": 150, "link": ""},
    "5": {"name": "Ear muffs", "price": 1500, "link": ""},
    "6": {"name": "Short sleeves", "price": 950, "link": ""},
    "7": {"name": "Scarfs", "price": 900, "link": ""},
    "8": {"name": "Skirt", "price": 1300, "link": ""},
    "9": {"name": "SHEIN Braclet", "price": 200, "link": ""},
    "10": {"name": "Bags", "price": 750, "link": ""},
    "11": {"name": "Coat", "price": 3000, "link": ""},
    "12": {"name": "Zip up jacket", "price": 1300, "link": ""},
}

user_carts = {}
application = None

def get_application():
    global application
    if application is None:
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("products", products_command))
        application.add_handler(CommandHandler("order", order_command))
        application.add_handler(CommandHandler("cart", cart_command))
        application.add_handler(CommandHandler("checkout", checkout_command))
        application.add_error_handler(error)
    return application

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
🛍 Welcome to SS Store!

Available Commands:

/products - View products
/order <id> - Add product to cart
/cart - View your cart
/checkout - Place your order
/help - Help
"""
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
Need help?

/products - View products
/order <id> - Add item to cart
/cart - View cart
/checkout - Complete order
"""
    )

async def products_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "📦 Available Products:\n\n"
    for pid, product in PRODUCTS.items():
        message += f"{pid}. {product['name']} - {product['price']} ETB\n"
        if product['link']:
            message += f"   📸 {product['link']}\n"
    message += "\nUse /order <product_id>"
    await update.message.reply_text(message)

async def order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /order <product_id>")
        return
    product_id = context.args[0]
    if product_id not in PRODUCTS:
        await update.message.reply_text("❌ Product not found.")
        return
    if user_id not in user_carts:
        user_carts[user_id] = []
    user_carts[user_id].append(PRODUCTS[product_id])
    await update.message.reply_text(f"✅ {PRODUCTS[product_id]['name']} added to cart.")

async def cart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_carts or len(user_carts[user_id]) == 0:
        await update.message.reply_text("🛒 Your cart is empty.")
        return
    total = 0
    message = "🛒 Your Cart:\n\n"
    for item in user_carts[user_id]:
        message += f"{item['name']} - {item['price']} ETB\n"
        total += item["price"]
    message += f"\n💰 Total: {total} ETB"
    await update.message.reply_text(message)

async def checkout_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_carts or len(user_carts[user_id]) == 0:
        await update.message.reply_text("🛒 Your cart is empty.")
        return
    total = sum(item["price"] for item in user_carts[user_id])
    order_summary = ""
    for item in user_carts[user_id]:
        order_summary += f"- {item['name']} ({item['price']} ETB)\n"
    user_carts[user_id] = []
    await update.message.reply_text(
        f"""
✅ Order Placed Successfully!

Items:
{order_summary}

💰 Total: {total} ETB

Thank you for shopping with SS Store.
"""
    )

async def error(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

def run_bot():
    app = get_application()
    print("SS Store Bot is running...")
    app.run_polling()
