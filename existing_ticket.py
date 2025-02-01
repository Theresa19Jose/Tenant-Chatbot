from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from api.ticket_status import get_ticket_status



async def existing_ticket(query, context) -> None:
    await query.answer()
    context.user_data['conversation_state'] = 'WAITING_FOR_TICKETNUMBER'
    await query.message.reply_text("Please enter the Ticket Number:")


async def fetch_ticket_status(update, context) -> None:
    if 'conversation_state' in context.user_data and context.user_data['conversation_state'] == 'WAITING_FOR_TICKETNUMBER':
        ticket_number = update.message.text
        ticket_status = get_ticket_status(ticket_number)

        if ticket_status:
            request_subject_line = ticket_status.get('requestSubjectLine')
            request_description = ticket_status.get('requestDescription')
            request_status = ticket_status.get('requestStatus')

            await update.message.reply_text(
                f"Ticket Status:\n"
                f"Subject: {request_subject_line}\n"
                f"Description: {request_description}\n"
                f"Status: {request_status}"
            )
        else:
            await update.message.reply_text("Failed to retrieve ticket status.")

        # Clear conversation state after displaying ticket status
        if 'conversation_state' in context.user_data:
            del context.user_data['conversation_state']
    else:
        await update.message.reply_text("Please enter your ticket number first.")
