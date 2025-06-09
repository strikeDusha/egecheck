import asyncio
from aiogram import Bot, Dispatcher, types
from parser import reload_and_parse



cfg = open('cfg.txt')
token = cfg.readline().strip()
chat_id = int(cfg.readline())
cfg.close()

dp = Dispatcher()
bot = Bot(token=token)
res = {}

async def background_checker():
    global res
    while True:
        try:
            current = reload_and_parse()
            if current and current != res:
                res = current
                text = "\n".join(f"{k}: {v}" for k, v in current.items())
                await bot.send_message(chat_id, f"Обновились результаты ЕГЭ:\n\n{text}")
            await asyncio.sleep(900)  # 15 минут
        except Exception as e:
            print(f"Ошибка в фоне: {e}")
            await asyncio.sleep(60)

@dp.message()
async def cmd_start(message: types.Message):
    await message.answer(
        f"<b>Привет {message.from_user.full_name}!</b>\n"
        f"github: <a href='https://github.com/strikeDusha'>ссылка</a>\n"
        f"id - <code>{message.from_user.id}</code>",
        parse_mode="HTML"
    )



async def main():
    asyncio.create_task(background_checker())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
