import asyncio
from django.core.management.base import BaseCommand
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Message


class PrintHandler(Message):
    async def handle_DATA(self, server, session, envelope):
        print("Message from:", envelope.mail_from)
        print("Message to  :", envelope.rcpt_tos)
        print("Message data:")
        print(envelope.content.decode("utf8", errors="replace"))
        print("End of message")
        return "250 Message accepted for delivery"

    async def handle_message(self, message):
        # This method is required by the Message class
        pass


class Command(BaseCommand):
    help = "Starts the development SMTP server"

    def handle(self, *args, **kwargs):
        handler = PrintHandler()
        controller = Controller(handler, hostname="localhost", port=1025)
        controller.start()

        print("SMTP server running at localhost:1025")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            controller.stop()
            loop.close()
