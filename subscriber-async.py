import asyncio
import aiomqtt
from dotenv import load_dotenv
from colorama import Fore
import os

load_dotenv()

broker = os.getenv("BROKER")
port = int(os.getenv("PORT"))
topic = os.getenv("TOPIC")
if os.getenv("USER_NAME") is None or os.getenv("USER_NAME") == "":
    user_name = None
    pass_word = None
else:
    user_name = os.getenv("USER_NAME")
    pass_word = os.getenv("PASSWORD")


# Sample async function to be called
async def processSnapshot(message: aiomqtt.Message):
    await asyncio.sleep(1)


# This gets called whenever when we get an MQTT message
async def mqtt_on_message(msg: aiomqtt.Message):
    print(
        Fore.WHITE
        + "TOPIC: "
        + Fore.LIGHTYELLOW_EX
        + str(msg.topic)
        + Fore.WHITE
        + "\tDATA: "
        + Fore.GREEN
        + " "
        + msg.payload.decode("utf-8", "ignore")
    )

    return await processSnapshot(msg.payload.decode("utf-8", "ignore"))


async def main():
    ...
    try:
        async with aiomqtt.Client(
            hostname=broker,
            port=port,
            username=user_name,
            password=pass_word,
        ) as client:
            async with client.messages() as messages:
                await client.subscribe(topic)
                # await client.subscribe(topic-2)
                async for message in messages:
                    asyncio.ensure_future(mqtt_on_message(message))
    except Exception as x:
        print("application has shutdown or could not start\n", x)


if __name__ == "__main__":
    asyncio.run(main())
