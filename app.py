from bot import get_application

if __name__ == "__main__":
    app = get_application()
    print("Bot is running!")
    app.run_polling()
