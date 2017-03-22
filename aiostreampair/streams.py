'''Stream Pairs. StreamWriter connected directly to StreamReader.
'''

import asyncio

__all__ = ['StreamPairUnidirectionalTransport', 'uni_stream_pair']

class StreamPairUnidirectionalTransport(asyncio.transports.Transport):
    '''A transport linking a StreamWriter to a StreamReader.
    
    Any data received via write() is directly written to the reader. No 
    buffering is done by the transport.'''
    
    def __init__(self, loop, protocol, extra=None):
        super().__init__(extra=extra)
        self._loop = loop
        self._protocol = protocol
        
        self._closed = False
        self._eof = False
        
        self._protocol.connection_made(self)
    
    def set_protocol(self, protocol):
        self._protocol = protocol
    
    def get_protocol(self):
        return self._protocol
    
    def close(self):
        if self._closed:
            return
        self._closed = True
        #self.write_eof()
        self._loop.call_soon(self._protocol.connection_lost, None)
    
    def is_closing(self):
        return self._closed
    
    def get_write_buffer_size(self):
        return 0
    
    def set_write_buffer_limits(self, high=None, low=None):
        pass
    
    def get_write_buffer_limits(self):
        return (0, 0)
    
    def write(self, data):
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError('data argument must be a bytes-like object, '
                    'not %r' % type(data).__name__)
            
        if self._eof:
            raise RuntimeError('Cannot call write() after write_eof()')
        
        self._protocol.data_received(data)
    
    def can_write_eof(self):
        return True
    
    def write_eof(self):
        if self._eof:
            return
        self._eof = True
        
        keep_open = self._protocol.eof_received()
        if not keep_open:
            self.close()
    
    def abort(self):
        self.close()

def uni_stream_pair(loop = None):
    '''Create a unidirectional stream pair.
    
    Returns (reader, writer) where reader is a StreamReader and writer is a 
    StreamWriter. Data written to the writer can be read from the reader.'''
    
    if loop is None:
        loop = asyncio.get_event_loop()
    
    reader = asyncio.streams.StreamReader(loop=loop)
    protocol = asyncio.streams.StreamReaderProtocol(reader, loop=loop)
    transport = StreamPairUnidirectionalTransport(loop, protocol)
    writer = asyncio.streams.StreamWriter(transport, protocol, reader, loop)
    
    return (reader, writer)