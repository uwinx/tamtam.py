=================
👮‍♂️ tamtam.py
=================

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black
    :alt: tamtam.py-code-style

.. image:: https://img.shields.io/badge/Python%203.7-blue.svg
    :target: https://www.python.org/
    :alt: tamtam.py-python-version

**TamTam.py requires ujson, pydantic, aiohttp**


::

    pip install https://github.com/uwinx/tamtam.py/archive/master.zip


**ℹ️ Setting bot-info:**


.. code-block:: python

    from tamtam import Bot, types, run_async

    Bot("put token @PrimeBot gave")

    async def func():
        info = await types.SetInfo(
            name="MyBotsName",
            description="smth...",
        )
        print(info)

    run_async(func())

------------------------------
❓ Polling TamTam for updates
------------------------------

.. code-block:: python

    from tamtam import Bot, Dispatcher, types, run_poller

    bot = Bot("put token @PrimeBot gave")
    dp = Dispatcher(bot)

    @dp.message_handler()
    async def msg_handler(msg: types.Message):
        await msg.reply("Hello!")

    run_poller(func())


--------------------------------
☂️ Write fancy decorators
--------------------------------

.. code-block:: python

    @dp.bot_started()
    async def start_handler(upd: types.BotStarted):
        await upd.respond("you started bot")

---------------------------------------------------
👟 ⇒ 👞 Easily switch from polling to webhook
---------------------------------------------------

.. code-block:: python

    from tamtam import Bot, Dispatcher, types, run_sever

    bot = Bot("token")
    dp = Dispatcher(bot)

    @dp.bot_started()
    async def handler(upd: types.BotStarted):
        await upd.respond("Sup!")

    run_server()

-----------------------
If not configured:
-----------------------

.. code-block:: python

    # better example in repo/examples/
    async def sub(url):
        if not (await bot.subscribe(url))["success"]:
            # something went wrong
            ...
        ...

    url = "https://my.domain/path"  # or use yarl.URL.build

    from tamtam import run_async
    run_async(sub(url))


-------------------------------------
Easy function based message filters
-------------------------------------

.. code-block:: python

    @dp.message_handler(MessageFilters.match(r"^.ban \d$"))
    async def ban_user_handler(message: types.Message):
        ...


============
Buttons
============

You can use `tamtam.types.attachments::InlineKeyboardAttachment`, but ... I find it quite inconvenient to utilize and, that's why we have `tamtam.types.attachments::ButtonsArray`
Think of `ButtonsArray` as an abstraction from `list[list[button]]`.


.. code-block:: python

    from tamtam.buttons import ButtonsArray, CallbackButton, InlineKeyboardAttachment

    array = ButtonsArray()
    row, index = array.add_row(1)  # pass None for dynamic row
    row.add(CallbackButton("text", "payload", "negative"))
    row2, index2 = array.add_row(1)

    array.delete_row(index2)

    # further actions, e.g send message
    attachments = (InlineKeyboardAttachment.from_array(array), )

=======================
Bots using tamtam.py
=======================

`GetJson
<https://tt.me/getjson>`_  this bot returns sent message's json (useful for developers or no)

See `examples
<https://github.com/uwinx/tamtam.py/tree/master/examples>`_ for more.

If your bot using tamtam.py, let me know!

=========================
Some advices from author
=========================

- Try to avoid using webhooks :) For safety.
- I prohibit using other libraries for tamtam (I checked them all. It's for your sake, python coders are brainless today).
- async/await syntax is easy. asyncio does not eat people. Stay modern.
