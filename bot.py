import os
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
)

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("No TELEGRAM_TOKEN found")

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

def get_application():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("products", products_command))
    dp.add_handler(CommandHandler("order", order_command))
    dp.add_handler(CommandHandler("cart", cart_command))
    dp.add_handler(CommandHandler("checkout", checkout_command))
    dp.add_error_handler(error)
    
    return updater

def start_command(update: Update, context: CallbackContext):
    update.message.reply_text(
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

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        """
Need help?
/products - View products
/order <id> - Add item to cart
/cart - View cart
/checkout - Complete order
"""
    )

def products_command(update: Update, context: CallbackContext):
    message = "📦 Available Products:\n\n"
    for pid, product in PRODUCTS.items():
        message += f"{pid}. {product['name']} - {product['price']} ETB\n"
        if product['link']:
            message += f"   📸 {product['link']}\n"
    message += "\nUse /order <product_id>"
    update.message.reply_text(message)

def order_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    
    if len(context.args) == 0:
        update.message.reply_text("Usage: /order <product_id>")
        return
    
    product_id = context.args[0]
    
    if product_id not in PRODUCTS:
        update.message.reply_text("❌ Product not found.")
        return
    
    if user_id not in user_carts:
        user_carts[user_id] = []
    
    user_carts[user_id].append(PRODUCTS[product_id])
    update.message.reply_text(f"✅ {PRODUCTS[product_id]['name']} added to cart.")

def cart_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    
    if user_id not in user_carts or len(user_carts[user_id]) == 0:
        update.message.reply_text("🛒 Your cart is empty.")
        return
    
    total = 0
    message = "🛒 Your Cart:\n\n"
    
    for item in user_carts[user_id]:
        message += f"{item['name']} - {item['price']} ETB\n"
        total += item["price"]
    
    message += f"\n💰 Total: {total} ETB"
    update.message.reply_text(message)

def checkout_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    
    if user_id not in user_carts or len(user_carts[user_id]) == 0:
        update.message.reply_text("🛒 Your cart is empty.")
        return
    
    total = sum(item["price"] for item in user_carts[user_id])
    order_summary = ""
    
    for item in user_carts[user_id]:
        order_summary += f"- {item['name']} ({item['price']} ETB)\n"
    
    user_carts[user_id] = []
    
    update.message.reply_text(
        f"""
✅ Order Placed Successfully!

Items:
{order_summary}

💰 Total: {total} ETB

Thank you for shopping with SS Store.
"""
    )

def error(update, context):
    print(f"Update {update} caused error {context.error}")
