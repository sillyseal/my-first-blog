import os

# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print('yes')

# import time
# while True:
#     try:
#         time.sleep(1)
#     except KeyboardInterrupt:
#         print('loop is broken, exited')
#         break

# def start_datapush():
import stomp
import time
from datetime import datetime, timedelta

API_KEY = '7kd5sdkv5amapvf'


class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('received an error "%s"' % message)

    def on_message(self, headers, message):
        for k, v in headers.items():
            print('header: key %s , value %s' % (k, v))
            print('received a message "%s"' % message)


conn_list = []  # this is just for testing, only use if you are calling more than one connection
conn = stomp.Connection12(host_and_ports=[('api.bmreports.com', 61613)], use_ssl=True)
conn.set_listener('', MyListener())

conn_list.append(conn)  # this is for testing, not required
conn.start()
conn.connect(API_KEY, API_KEY, True)



conn.subscribe(destination='/topic/bmrsTopic', ack='auto', id='Zen123')

now = datetime.now()
end = now + timedelta(days=1)

while conn.is_connected() and datetime.now() < end:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break  # goes to finally block to disconnect
conn.disconnect()
print('disconnected')

for _conn in conn_list:
    _conn.disconnect()
print('disconnected')