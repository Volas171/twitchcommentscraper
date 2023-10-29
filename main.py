import requests
import socket
import calendar
import datetime
import pandas as pd

# Replace with Twitch channel name and your OAuth token
channel_name = "thechannel"
oauth_token = "oauth:xxxxxxxx" #find this in https://twitchapps.com/tmi/

# Connect to Twitch IRC
server = "irc.chat.twitch.tv"
port = 6667
nickname = "yourchannelname"

# Connect to the IRC server
sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {oauth_token}\r\n".encode("utf-8"))
sock.send(f"NICK {nickname}\r\n".encode("utf-8"))
sock.send(f"JOIN #{channel_name}\r\n".encode("utf-8"))

header = ['time', 'user', 'message']

# Create an empty list to store chat entries
chat_entries = []

# Listen for messages
while True:
    try:
        response = sock.recv(2048).decode("utf-8")
        if "PING" in response:
            sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        elif "PRIVMSG" in response:
            date = datetime.datetime.utcnow()
            now = calendar.timegm(date.utctimetuple())
            username = response.split('!')[0][1:]
            message = response.split('PRIVMSG #')[1].split(' :')[1]
            if message.__contains__("@"):
                message = ""
            else:
                print(f"{username}: {message}")
                data = [now, username, message]
                chat_entries.append(data)
    except KeyboardInterrupt:
        # Close the connection and save the chat entries to a CSV file
        sock.close()
        data2 = pd.DataFrame(chat_entries, columns=header)
        data2.to_csv('dataset.csv', index=False)
        break



