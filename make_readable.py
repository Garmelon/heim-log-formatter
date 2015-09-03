# I do know this is very badly written :P

import json, sys, time, operator

INPUTFILE = sys.argv[1]
OUTPUTFILE = sys.argv[2]

def room_to_string(room, ilvl = 0): # iteration level
	string = []
	indentation = []
	indentation.append("|  "*ilvl)
	#for message in room:
	for message in reversed(room):
	#for index in range(len(room), 0):
		#message = room[index]
		s = "[" + message["sender"] + "] "
		ss = "".ljust(len(s))
		for i, line in enumerate(message["content"].strip().splitlines()):
			if i == 0:
				string.append(time.strftime("%d.%m.%Y %H:%M:%S ",  time.gmtime(message["time"])))
				string.extend(indentation)
				string.append(s)
			else:
				string.append("                    ")
				string.extend(indentation)
				string.append(ss)
			string.append(line)
			string.append("\r\n")
		string.extend(room_to_string(message["children"], ilvl = ilvl + 1))
	return string

# read all messages
with open(INPUTFILE, "r") as f:
	messages = json.load(f)

# threading
imessages = {} # imessages[id] = smsg
for msg in messages:
	imessages[msg["id"]] = {u"time":msg["time"], u"sender":msg["sender"]["name"], u"content":msg["content"], u"id":msg["id"], u"children":[]}
	if u"parent" in msg:
		imessages[msg["id"]][u"parent"] = msg["parent"]
for mid in imessages:
	msg = imessages[mid]
	if "parent" in msg:
		if msg["parent"] in imessages:
			imessages[msg["parent"]]["children"].append(msg)
		#else:
			#del(msg["parent"])
room = []
for mid in imessages:
	msg = imessages[mid]
	msg["children"].sort(key=operator.itemgetter("id"))
	msg["children"].reverse()
	if not "parent" in msg:
		room.append(msg)
room.sort(key=operator.itemgetter("id"))
room.reverse()

# save in outputfile
with open(OUTPUTFILE, "w") as f:
	strlist = room_to_string(room)
	f.write("".join(strlist).encode("utf8"))
