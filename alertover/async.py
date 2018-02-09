# coding: utf-8 -*-
import aiohttp
from asyncio import sleep, ensure_future
import  logging

API_BASE = "https://api.alertover.com/v1/alert"


class Session:
    def __init__(self, source, receiver, logger=None, suppress_exception=False,
                 auto_retry=False, max_retry=3, loop=None,
                 **kargs):
        self.source = source
        self.receiver = receiver
        self.auto_retry = auto_retry
        self.max_retry = (max_retry if max_retry > 0 else 3) if auto_retry else 1
        self.kargs = kargs
        self.loop = loop
        self.logger=logger
        self.suppress_exception = suppress_exception

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            if self.logger:
                self.logger.exception("An exception occurred while sending message to your device.")
            if self.suppress_exception:
                return True

    async def send(self,
             title="",
             urgent=False,
             sound="default",
             content="",
             url=""):
        """
        Send a message to your device(s).
        :param title:  Message title.
        :param urgent: Message priority, True if urgent.
        :param sound:  Notification sound to be played on your device(s).
            Options:
                "intermission", "bugle", "spacealarm", "incoming", "silent",
                "cashregister", "classic", "default", "updown", "cosmic",
                "persistent", "pianobar", "echo", "failling", "bike" ,"magic"
                "tugboat", "system"
        :param content: Content of your message
        :param url (Optional): Url you desired to contained in your message.
        :return: None
        """
        params = {"source": self.source,
                  "receiver": self.receiver,
                  "title": title,
                  "priority": 1 if urgent else 0,
                  "sound": sound,
                  "content": content,
                  "url": url}

        async with aiohttp.ClientSession(loop=self.loop) as session:
            trails = 0
            error = None
            while trails < self.max_retry:
                try:
                    await session.post(url=API_BASE, data=params, **self.kargs)
                except aiohttp.ClientError as e:
                    error = e
                    if self.auto_retry:
                        await sleep(5 << trails)
                    trails += 1
                else:
                    break
            else:
                raise error


async def send(source, receiver,
         title="",
         urgent=False,
         sound="default",
         content="",
         url="",
         auto_retry=False,
         max_retry=3):
    with Session(source, receiver,
                 auto_retry=auto_retry,
                 max_retry=max_retry) as session:
        await session.send(title=title,
                           urgent=urgent,
                           sound=sound,
                           content=content,
                           url=url)


class AlertOverHandler(logging.Handler):
    def __init__(self, source, receiver, level=logging.ERROR, loop=None, **kargs):
        super(AlertOverHandler, self).__init__(level=level)
        self.session = Session(source, receiver, loop=loop, **kargs)
        self.formatter = {}
        self.default_msg_attr = {
            "title": "AlertOver",
            "urgent": False,
            "sound": "default",
            "url": ""
        }
        self.loop = loop

    def set_default_msg_attr(self, **kargs):
        self.default_msg_attr.update(kargs)

    def emit(self, record):
        def done_callback(future):
            if future.exception():
                self.handleError(record)

        msg = self.format(record)
        with self.session as session:
            task = ensure_future(session.send(title=getattr(record, "title", self.default_msg_attr["title"]),
                                              urgent=getattr(record, "urgent", self.default_msg_attr["urgent"]),
                                              sound=getattr(record, "sound", self.default_msg_attr["sound"]),
                                              url=getattr(record, "url", self.default_msg_attr["url"]),
                                              content=msg))
            task.add_done_callback(done_callback)