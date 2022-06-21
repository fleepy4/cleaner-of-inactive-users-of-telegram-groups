from pyrogram import Client
import asyncio

app = Client('account_for_clearing', api_id=18146570, api_hash='99451116216b56186092b3a9d7101bd9')


@app.on_message()
async def waiting(client, message):
    if message.text == '/inkick':
        im = await app.get_chat_member(message.chat.id, "me")
        if str(im.status) == 'ChatMemberStatus.ADMINISTRATOR':
            if im.privileges.can_restrict_members:
                # bot has all permission
                sender = await app.get_chat_member(message.chat.id, message.from_user.id)
                if str(sender.status) == 'ChatMemberStatus.ADMINISTRATOR':
                    # ok. admin requested to clear the chat
                    async for user in app.get_chat_members(message.chat.id):
                        if str(user.user.status) == 'UserStatus.LONG_AGO' or str(user.user.status) == 'UserStatus.LAST_MONTH':
                            try:
                                await app.ban_chat_member(message.chat.id, user.user.id)
                                await asyncio.sleep(0.1)
                                await app.unban_chat_member(message.chat.id, user.user.id)
                            except Exception as ex:
                                print(ex)
                                if "3 seconds" in str(ex):
                                    await asyncio.sleep(3)
                                    await app.ban_chat_member(message.chat.id, user.user.id)
                    await app.send_message(message.chat.id, 'Очистка чата окончена.')

                else:
                    await app.send_message(message.chat.id, 'Отказано в доступе. Данная функция доступна только ' +
                                           'администрации чата')
            else:
                await app.send_message(message.chat.id, 'Отказано в доступ. Бот не может банить пользователей.')
        else:
            await app.send_message(message.chat.id, 'Отказано в доступе. Боту нужен доступ администратора')


app.run()
