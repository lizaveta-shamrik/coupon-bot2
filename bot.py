import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.types import FSInputFile
import asyncio

API_TOKEN = "8307035152:AAH2l9x3KunTdAlsCndQ7qNgk-55W6T9Res"
OWNER_CHAT_ID = 481282193  # <--- Замените на свой ID!

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

coupons = [str(i) for i in range(1, 13)]
used_coupons = set()
last_reply_message = {}

def build_menu():
    kb = InlineKeyboardBuilder()
    for coupon in coupons:
        if coupon not in used_coupons:
            kb.button(text=coupon, callback_data=coupon)
    kb.adjust(4)
    return kb.as_markup()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    photo = FSInputFile("coupons.jpg")
    await message.answer_photo(photo, caption="Выбирай купон, любимый💝", reply_markup=build_menu())

@dp.callback_query()
async def handle_coupon(callback: types.CallbackQuery):
    coupon = callback.data
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    if user_id in last_reply_message:
        try:
            await bot.delete_message(chat_id, last_reply_message[user_id])
        except:
            pass

    used_coupons.add(coupon)

    try:
        await callback.message.edit_reply_markup(reply_markup=build_menu())
    except:
        pass

    await callback.answer()

    reply = await callback.message.answer(
        f"Супер! Ты выбрал купон №{coupon} 💓 Я уже сообщил малыхе, жди когда реализуется 😉"
    )
    last_reply_message[user_id] = reply.message_id

    # Отправить тебе уведомление
    try:
        await bot.send_message(
            OWNER_CHAT_ID,
            f"Пользователь @{callback.from_user.username or 'без username'} выбрал купон №{coupon}"
        )
    except Exception as e:
        logging.warning(f"Не удалось отправить уведомление владельцу: {e}")

    if len(used_coupons) == len(coupons):
        await callback.message.answer("Все купоны закончились, но любовь не заканчивается💕")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
