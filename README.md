# aiostreampair
Connect a StreamWriter to a StreamReader.

Have you ever wished to pass a byte stream between two `asyncio` coroutines using the familiar `StreamWriter` and `StreamReader` interfaces? Now you can! Get a unidirectional stream pair by 

    reader, writer = aiostreampair.uni_stream_pair(loop)

and have fun!
