import asyncio
import traceback

from aiogram import types
from aiohttp import web

from General.structure import CreateBot
from General.config import cfg, BotData


async def on_startup(_):
    main_bot = CreateBot(
        bot_id=0,
        token=cfg().main_bot.token,
        admin_id=cfg().main_bot.admin_id,
        is_main_bot=True,
        db_name=cfg().main_bot.db_name
    )

    bots = [
        main_bot
    ]

    await asyncio.gather(*map(lambda x: asyncio.create_task(x.run()), bots))


async def shutdown_bots(bot_data: BotData):
    await bot_data.bot.delete_webhook()
    await bot_data.dp.storage.close()
    await bot_data.bot.close()


async def on_shutdown(_):
    await asyncio.gather(*map(lambda x: asyncio.create_task(shutdown_bots(x)), cfg().meta.all_bots.values()))


async def webhooks_handle(request):
    token = request.match_info['bot_token']
    bot_obj = cfg().meta.all_bots.get(token)

    if bot_obj:
        try:
            update = types.Update.to_object(await request.json())
            await bot_obj.dp.process_update(update)
        except:
            print(traceback.format_exc())

    return web.Response(status=200)


if __name__ == '__main__':
    webapp = web.Application()
    webapp.on_startup.append(on_startup)
    webapp.on_shutdown.append(on_shutdown)
    webapp.router.add_post(cfg().meta.webhook_path, webhooks_handle)
    web.run_app(webapp, host=cfg().meta.webhook_host, port=cfg().meta.webhook_port)
