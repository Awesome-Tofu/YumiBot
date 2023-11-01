import random
import requests
import datetime
from typing import Final
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext,
    CallbackQueryHandler,
)
from animegifs import animegifs
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN: Final = "6485368421:AAE0Yg1vIWkDVoTy-25Y0M6J9l1A9P-mF6Q"
# API endpoint URL
BOT_USERNAME: Final = "@tttofubot"
WIBU_KEY = "WIBUAPI-zYNTkxNTMzNTQ4NkRldnNZQm90c1N1cHBvcnQ=x"


# KeyboardInline
import asyncio

START_TEXT = f"Welcome to {BOT_USERNAME} \nYou can get many pervy or sfw tools in this bot that you can enjoy! \n \n \nMy Owner: @samsharah"

button = InlineKeyboardButton("Commands", callback_data="commands")
keyboard = InlineKeyboardMarkup([[button]])


async def commands_callback(update: Update, context: CallbackContext):
    await update.callback_query.answer("Yamatte Kudasai..")
    await update.callback_query.edit_message_caption(
        caption="Here are the commands of this bot \n\n\n⭐PERV MENU\n/search <query> Get xvideos\n\n\n⭐BOORU MENU\n/sb Random sfw safebooru\n/gb Random sfw gelbooru\n/hb Random nsfw gelbooru\n/rb Random nsfw realbooru\n\n\n⭐AI MENU\n/imagine <query> Generates image according to text\n/gpt <query> Ask ChatGPT\n/bard <query> Ask Bard\n\n\n⭐Translation\n/tr <language code> translates the replied message",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Back", callback_data="back")]]
        ),
    )


async def back_callback(update: Update, context: CallbackContext):
    await update.callback_query.answer("Yamatte Kudasai..")
    await update.callback_query.edit_message_caption(
        caption=START_TEXT, reply_markup=keyboard
    )


# Stickers
early_stickers = [
    "CAACAgEAAxkBAAEKp1hlQgdK4uBidgQp6Ei-rm5OK9PusAACXAMAAsumCUZ1PhVwc8tiWDME",
    "CAACAgUAAxkBAAEKp1plQgg10lymL4hgpctdw4CLUEb2-wAC3AcAAhBGOVVF3H4lnQkjqTME",
    "CAACAgIAAxkBAAEKp1xlQghihNNOYcn1e5_psyYPfxuz5wACVSkAAhjUyUnQ527GJmbesTME",
    "CAACAgQAAxkBAAEKp15lQglFIUd-AZjhlpu8dRC2RkEzlAACyxIAAgwc2FJvGyrNzxgzXjME",
    "CAACAgQAAxkBAAEKp2JlQgl4BQ1x3NLPSEAPAZV043DpOAACeQ8AAkgq0VJkLOe9PKhrMTME",
    "CAACAgUAAxkBAAEKp2RlQgmlsGSDSXvdyMptLLJ9gptrZwAC_wUAAh7yOVbtkJm6BRh-UzME",
]

# Start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.message.chat.first_name
    gifs = animegifs.Animegifs()
    gif = gifs.get_gif(
        random.choice(
            ["wave", "kiss", "lick", "poke", "pat", "tease", "blush", "bite", "love"]
        )
    )
    await update.message.reply_sticker(random.choice(early_stickers))
    await update.message.reply_animation(
        gif, caption=f"Hello {first_name},\n" + START_TEXT, reply_markup=keyboard
    )


# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_sticker(random.choice(early_stickers))
    gifs = animegifs.Animegifs()
    gif = gifs.get_gif(
        random.choice(
            ["wave", "kiss", "lick", "poke", "pat", "tease", "blush", "bite", "love"]
        )
    )
    await update.message.reply_animation(
        gif, caption=f"🆘HELP🆘\n\nHere are the help commands", reply_markup=keyboard
    )


# Search command
async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    utext = " ".join(context.args[0:])
    await update.message.reply_sticker(
        "CAACAgUAAxkBAAEKp3NlQg6i2XhPZK7ylgWZvm0kJDM2vwAC2AUAAkPkCFZN51yUcyTGZjME"
    )
    if not utext:
        await update.message.reply_sticker(
            "CAACAgUAAxkBAAEKqAtlQjcJqQFey6ZficYSAxNLLTRFWAACowQAAs5A6FYjoH7KHMPGVzME"
        )
        await update.message.reply_text("Please Input query")
    else:
        api_url = f"https://wibu-api.eu.org/api/xvideos/search?query={utext}&page=1&x_wibu_key={WIBU_KEY}"
        response = requests.get(api_url)
        json_data = response.json()
        if not json_data["result"]:
            await update.message.reply_sticker(
                "CAACAgUAAxkBAAEKp39lQhCw5B8Wub9-6NqgTuprx28NXwACnQYAAn-HAAFWJfXnKGDDPGgzBA"
            )
            await update.message.reply_text("Gomenosai, Not found!")
        else:
            random_object = random.choice(json_data["result"])
            # Fetching DATA
            title = random_object["title"]
            thumb = random_object["files"]["thumb69"]
            duration = str(datetime.timedelta(seconds=random_object["duration"]))
            views = random_object["views"]
            xvideo = random_object["files"]["low"]
            await update.message.reply_video(
                xvideo,
                caption=f"Title: {title}\nDuration: {duration}\nViews: {views}\n\n",
                thumbnail=thumb,
            )


# Midjourney
async def imagine_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    utext = " ".join(context.args[0:])

    if not utext:
        await update.message.reply_sticker(
            "CAACAgUAAxkBAAEKqAtlQjcJqQFey6ZficYSAxNLLTRFWAACowQAAs5A6FYjoH7KHMPGVzME"
        )
        await update.message.reply_text("Please Input query")
    else:
        random_number = random.randint(1, 1000000)
        await update.message.reply_sticker(
            "CAACAgUAAxkBAAEKp3NlQg6i2XhPZK7ylgWZvm0kJDM2vwAC2AUAAkPkCFZN51yUcyTGZjME"
        )
        await update.message.reply_photo(
            f"https://wibu-api.eu.org/api/ai/midjourney?query={utext}&x_wibu_key={WIBU_KEY}&random={random_number}"
        )


# Booru API
# sb
async def sb_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_number = random.randint(1, 1000000)
    await update.message.reply_photo(
        f"https://wibu-api.eu.org/api/booru/sfw/sb?x_wibu_key={WIBU_KEY}&random={random_number}"
    )


# gb
async def gb_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_number = random.randint(1, 1000000)
    await update.message.reply_photo(
        f"https://wibu-api.eu.org/api/booru/sfw/gb?x_wibu_key={WIBU_KEY}&random={random_number}"
    )


# hb
async def hb_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_number = random.randint(1, 1000000)
    await update.message.reply_photo(
        f"https://wibu-api.eu.org/api/booru/nsfw/gb?x_wibu_key={WIBU_KEY}&random={random_number}"
    )


# rb
async def rb_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_number = random.randint(1, 1000000)
    await update.message.reply_photo(
        f"https://wibu-api.eu.org/api/booru/nsfw/rb?x_wibu_key={WIBU_KEY}&random={random_number}"
    )


# GPT
async def gpt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    utext = " ".join(context.args[0:])
    if not utext:
        await update.message.reply_sticker(
            "CAACAgUAAxkBAAEKqAtlQjcJqQFey6ZficYSAxNLLTRFWAACowQAAs5A6FYjoH7KHMPGVzME"
        )
        await update.message.reply_text("Please Input query")
    else:
        gptapi = f"https://api.akuari.my.id/ai/gpt?chat={utext}"
        response = requests.get(gptapi)
        json_data = response.json()
        await update.message.reply_text(json_data["respon"])


# Bard
async def bard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    utext = " ".join(context.args[0:])
    if not utext:
        await update.message.reply_sticker(
            "CAACAgUAAxkBAAEKqAtlQjcJqQFey6ZficYSAxNLLTRFWAACowQAAs5A6FYjoH7KHMPGVzME"
        )
        await update.message.reply_text("Please Input query")
    else:
        bardapi = f"https://api.akuari.my.id/ai/gbard?chat={utext}"
        response = requests.get(bardapi)
        json_data = response.json()["respon"]
        translate_api = (
            f"https://translate-gw3m.onrender.com/translate?q={json_data}&lang=en"
        )
        response_tr = requests.get(translate_api)
        translated_data = response_tr.json()["text"]
        await update.message.reply_text(translated_data)


# Translate
async def tr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    utext = " ".join(context.args[0:])
    mesasage = update.message
    temxt = mesasage.text
    reply_to_message = mesasage.reply_to_message

    if reply_to_message:
        reply_text = reply_to_message.text
        if not utext:
            translate_api = (
                f"https://translate-gw3m.onrender.com/translate?q={reply_text}&lang=en"
            )
            response = requests.get(translate_api)
            json_data = response.json()["text"]
            await update.message.reply_text(f"{json_data}")
        else:
            translate_api = f"https://translate-gw3m.onrender.com/translate?q={reply_text}&lang={utext}"
            response = requests.get(translate_api)
            json_data = response.json()["text"]
            await update.message.reply_text(f"{json_data}")
    else:
        await update.message.reply_sticker(
            "CAACAgUAAxkBAAEKqAtlQjcJqQFey6ZficYSAxNLLTRFWAACowQAAs5A6FYjoH7KHMPGVzME"
        )
        await update.message.reply_text("No text to translate")


# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed:
        return "hey there!"

    return "IDK bruh"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type}")

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("imagine", imagine_command))
    app.add_handler(CommandHandler("sb", sb_command))
    app.add_handler(CommandHandler("gb", gb_command))
    app.add_handler(CommandHandler("hb", hb_command))
    app.add_handler(CommandHandler("rb", rb_command))
    app.add_handler(CommandHandler("gpt", gpt_command))
    app.add_handler(CommandHandler("bard", bard_command))
    app.add_handler(CommandHandler("tr", tr_command))
    app.add_handler(CallbackQueryHandler(commands_callback, pattern="commands"))
    app.add_handler(CallbackQueryHandler(back_callback, pattern="back"))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print("Polling..")
    app.run_polling(poll_interval=3)
