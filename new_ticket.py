import os
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from api.service_request import service_request
from api.premise import get_premise
from api.media_request import upload_media

async def new_ticket(query, context, reference_id: str) -> None:
    premise_data = get_premise(reference_id)

    if not premise_data:
        await query.message.reply_text("Failed to retrieve premise details.")
        return

    if len(premise_data) == 1:
        premise = premise_data[0]
        context.user_data['domain'] = premise['domain']
        context.user_data['identifier'] = premise['identifier']

        premise_name = premise.get("name", "")
        premise_address = premise.get("address", "")
        await query.message.reply_text(f"Your Premise is:\nName: {premise_name}\nAddress: {premise_address}")

        await query.message.reply_text("Please enter the issue:")
        context.user_data['conversation_state'] = 'WAITING_FOR_SUBJECT'
    else:
        keyboard = [
            [InlineKeyboardButton(f"{p.get('name', '')} - {p.get('address', '')}", callback_data=f"select_premise:{p['domain']}:{p['identifier']}")]
            for p in premise_data
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Please choose a premise:", reply_markup=reply_markup)

async def select_premise(update, context) -> None:
    query = update.callback_query
    await query.answer()

    domain, identifier = query.data.split(':')[1:3]
    context.user_data['domain'] = domain
    context.user_data['identifier'] = identifier

    await query.message.reply_text("Please enter the issue:")
    context.user_data['conversation_state'] = 'WAITING_FOR_SUBJECT'

async def capture_request_subject(update, context) -> None:
    context.user_data['request_subject'] = update.message.text
    await update.message.reply_text("Please enter the description:")
    context.user_data['conversation_state'] = 'WAITING_FOR_DESCRIPTION'

async def capture_request_description(update, context) -> None:
    context.user_data['request_description'] = update.message.text
    await update.message.reply_text("Please upload any relevant media (photo/video/audio):")
    context.user_data['conversation_state'] = 'WAITING_FOR_MEDIA'

async def save_media_file(bot, file_id, directory):
    try:
        file = await bot.get_file(file_id)
        file_url = file.file_path

        os.makedirs(directory, exist_ok=True)
        file_name = os.path.join(directory, os.path.basename(file_url))

        # Download file content
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(response.content)
            return file_name
        else:
            print(f"Failed to download media file. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Failed to save media file: {e}")
        return None

async def capture_request_media(update, context) -> None:
    media_file = None
    if update.message.photo:
        media_file = update.message.photo[-1].file_id
    elif update.message.video:
        media_file = update.message.video.file_id

    if media_file:
        context.user_data['media_file'] = media_file

        domain = context.user_data.get('domain')
        identifier = context.user_data.get('identifier')
        request_subject = context.user_data.get('request_subject')
        request_description = context.user_data.get('request_description')

        payload = {
            "requestType": "MAINTENANCE",
            "requestSubjectLine": request_subject,
            "requestDescription": request_description,
            "domain": domain,
            "spaces": [
                {
                    "type": "Floor",
                    "data": {
                        "domain": domain,
                        "identifier": identifier
                    }
                }
            ],
            "priority": "P1",
            "discipline": "TFM"
        }

        ticket_number , request_number = service_request(payload)

        if ticket_number:
            saved_file_path = await save_media_file(context.bot, media_file, 'media_files')
            print(f"Media file saved to {saved_file_path}")

            if saved_file_path:
                # Call the new media upload function
                success, response_data = upload_media(saved_file_path, domain, request_number)

                if success:
                    await update.message.reply_text("Media uploaded successfully.")
                else:
                    await update.message.reply_text("Failed to upload media file to server.")
            else:
                await update.message.reply_text("Failed to save media file.")

            await update.message.reply_text(f"Complaint successfully submitted. \nYour Ticket number is: {ticket_number}")

            # Clear session data
            context.user_data.clear()

            # Set flag indicating that a ticket has been generated
            context.user_data['ticket_generated'] = True
        else:
            await update.message.reply_text("Failed to submit complaint.")
    else:
        await update.message.reply_text("No media file detected. Please upload a photo or video.")

async def handle_new_message(update, context) -> None:
    if context.user_data.get('ticket_generated'):
        # Clear the flag and reset the conversation to the initial state
        context.user_data.clear()
        await update.message.reply_text("Welcome! Please start by providing the reference ID.")
    else:
        # Handle other states as needed
        current_state = context.user_data.get('conversation_state')
        if current_state == 'WAITING_FOR_SUBJECT':
            await capture_request_subject(update, context)
        elif current_state == 'WAITING_FOR_DESCRIPTION':
            await capture_request_description(update, context)
        elif current_state == 'WAITING_FOR_MEDIA':
            await capture_request_media(update, context)
        else:
            await update.message.reply_text("Welcome! Please start by providing the reference ID.")
