from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    filters,  # Correct import of Filters
    ApplicationBuilder,
)

# States
SELECTING_ACTION, SELECTING_THEATER, SELECTING_MOVIE = range(3)

# Callback functions
def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['List Theaters']]
    update.message.reply_text(
        'Hi! I am MovieBot.\n\nWhat can I do for you today?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return SELECTING_ACTION

def list_theaters(update: Update, context: CallbackContext) -> int:
    text = update.message.text.lower() if update.message.text else None
    if text == 'list theaters':
        reply_keyboard = [['Theater 1', 'Theater 2']]
        update.message.reply_text(
            'Please select a theater:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return SELECTING_MOVIE
    else:
        update.message.reply_text('Please select a valid action.')
        return SELECTING_ACTION

def select_movie(update: Update, context: CallbackContext) -> int:
    user_reply = update.message.text
    update.message.reply_text(f'You selected {user_reply}. What movie would you like to watch?')

    # End conversation
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Cancelled.')
    return ConversationHandler.END

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = Enter your Bot Token here
    application = ApplicationBuilder().token(bot_token).build()

    # Create a ConversationHandler with states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_ACTION: [
                MessageHandler(filters.TEXT & (filters.Command), list_theaters),
            ],
            SELECTING_THEATER: [
                MessageHandler(filters.TEXT & (filters.Command), select_movie),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
