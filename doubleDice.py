from decouple import config
import logging
import time

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup  # button

# Callback Query
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackQueryHandler

# get token
bot_token = config("token")  # create .env file and add token=<your-token>

# Log errors
logger = logging.getLogger(__name__)

# Set up logging
logging.basicConfig(
    filename='./logs.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARN
)

# In-memory dictionary to store user cooldowns
user_cooldowns = {}
COOLDOWN_DURATION = 4  # Cooldown duration in seconds

# call back data has a 64 character limitation
keys = [
    # When use callback query, url not necessary
    [InlineKeyboardButton("Roll a Dice", callback_data="1"),
     InlineKeyboardButton("Roll Double", callback_data="2")],
]
keys_markup = InlineKeyboardMarkup(keys)

empty_key = [[InlineKeyboardButton("Sponsor", url="https://reza-taheri.ir")]]
empty_key_markup = InlineKeyboardMarkup(empty_key)

now = time.time


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str = None):
    try:
        chat_id = update.effective_chat.id

        if not text:
            text = "Welcome! What would you like to do?"

        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keys_markup
        )
    except Exception as e:
        logger.error(f"Error in start function: {e}")


async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery = None):
    try:
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id

        if chat_id in user_cooldowns:  # O(1)
            elapsed_time = now() - user_cooldowns[user_id]
            if elapsed_time < COOLDOWN_DURATION:
                # Inform user that they are still on cooldown
                await context.bot.sendMessage(chat_id=chat_id,
                                              text=f"Please wait {COOLDOWN_DURATION - int(elapsed_time)} seconds before rolling again."
                                              )
                return
            else:
                # Remove user from cooldown since the duration has passed
                del user_cooldowns[user_id]

        if not query:
            # Get the full command text
            command_text = update.message.text  # e.g., "/example some text"
            command = command_text.split()[0]
        else:
            command = query.data
            # edit previous buttons and remove them
            await query.edit_message_reply_markup(reply_markup=empty_key_markup)

        for _ in range(int(command[-1])):
            await context.bot.send_dice(
                chat_id=chat_id
            )

        # Store the current time as the last action time
        user_cooldowns[user_id] = time.time()

        await start(update, context, "What would you like to do next?")
    except Exception as e:
        logger.error(f"Error in roll_dice function: {e}")


async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query: CallbackQuery = update.callback_query
        await query.answer()
        await roll_dice(update, context, query)
    except Exception as e:
        logger.error(f"Error in callback_query_handler function: {e}")


# Global Error Handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.error(msg="Exception while handling an update:",
                     exc_info=context.error)

        # Notify the user (optional)
        if update and update.effective_user:
            await update.effective_message.reply_text('An error occurred. The bot will continue to work.')

    except Exception as e:
        logger.error(f"Error in error_handler: {e}")


def main():
    app = Application.builder().token(bot_token).build()

    handlers: list = [
        CommandHandler("start", start),
        CommandHandler("roll1", roll_dice),
        CommandHandler("roll2", roll_dice),
        CallbackQueryHandler(callback_query_handler)
    ]

    app.add_handlers(handlers)

    app.add_error_handler(error_handler)

    app.run_polling()


if __name__ == "__main__":
    main()


# what is the different between context.bot.send_message and update._bot.send_message?
