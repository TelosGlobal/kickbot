#python2.7

import os
import sys
import json
import sqlite3
import requests
import datetime

### SET the network prefix label
net_ver = ":Stagenet: "
dbFile = "prodState.sqlite3"
prodFile = "producers.json"

# MAINNET WEBHOOK - Replace below with your unique URL provided by Slack
#webhook_url = "https://hooks.slack.com/services/XXXXXXXXXXXXXXXXX"

f = open(prodFile)
data = f.read()
p = json.loads(data)

rows = len(p['rows'])
#print "Number of json records:",rows
print ""
rows = rows - 1

print str(datetime.datetime.now()) + ": Checking to see if database",dbFile,"exists...",
exists = os.path.isfile(dbFile)
if not exists:
    print dbFile, "not found."
    print ""
    print "NOTE:  Since the db file doesn't exist, I am going to build one"
    print "from the current state and then exit.  I will start my comparision"
    print "during the next execution of this script."
    print ""
    print str(datetime.datetime.now()) + ": Building a new state db...",
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()
    c.execute('create table state (owner, is_active, kick_reason_id, kick_reason, times_kicked, kick_penalty_hours, last_time_kicked)')
    print "Done."
    print str(datetime.datetime.now()) + ": Populating state table with json data...",
    for r in range(rows):
        #Build our insert values
        t = (p['rows'][r]['owner'],p['rows'][r]['is_active'],p['rows'][r]['kick_reason_id'],p['rows'][r]['kick_reason'],p['rows'][r]['times_kicked'],p['rows'][r]['kick_penalty_hours'],p['rows'][r]['last_time_kicked'])
        #print "t = ",t

        #Insert current producer record
        c.execute('insert into state (owner, is_active, kick_reason_id, kick_reason, times_kicked, kick_penalty_hours, last_time_kicked) values (?,?,?,?,?,?,?)', t)
    print "Done."
    print str(datetime.datetime.now()) + ": " + dbFile,"built with state table populated."
    print str(datetime.datetime.now()) + ": Exiting...catch you next time!"
    conn.commit()
    conn.close()

else:
    print "database",dbFile,"exists."
    print ""
    print str(datetime.datetime.now()) + ": Starting state comparison..."
    #Compare and alert on a kick within this execution instance
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()

    for r in range(rows):
        ##### Check to see if they previously were active!
        query = "select is_active from state where owner = '" + p['rows'][r]['owner'] + "'"
        c.execute(query)
        result = c.fetchone()
        if result:
            if result[0]==1 and p['rows'][r]['is_active']==0:
                msg = net_ver + p['rows'][r]['owner'] + " UNREGISTERED.  Reason: " + p['rows'][r]['kick_reason']
                slack_data = {'text': msg}
                requests.post(webhook_url, data=json.dumps(slack_data), headers={'Content-Type': 'application/json'})
            elif result[0]==0 and p['rows'][r]['is_active']==1:
                msg = net_ver + p['rows'][r]['owner'] + " REGISTERED."
                slack_data = {'text': msg}
                requests.post(webhook_url, data=json.dumps(slack_data), headers={'Content-Type': 'application/json'})
            else:
                msg = net_ver + p['rows'][r]['owner'] + " state unchanged.  Skipping..."
        else:
            if p['rows'][r]['is_active'] ==1:
                msg = net_ver + p['rows'][r]['owner'] + " REGISTERED."
                slack_data = {'text': msg}
                requests.post(webhook_url, data=json.dumps(slack_data), headers={'Content-Type': 'application/json'})
            else:
                msg = net_ver + p['rows'][r]['owner'] + " state unchanged.  Skipping..."
        print str(datetime.datetime.now()) + ": " + msg

    #Update state table
    print ""
    print str(datetime.datetime.now()) + ": Updating state table..."
    #Delete all records in state
    c.execute('delete from state')
    conn.commit()

    for r in range(rows):
        #Build our insert values
        print str(datetime.datetime.now()) + ": adding record data for",p['rows'][r]['owner'],"..."
        t = (p['rows'][r]['owner'],p['rows'][r]['is_active'],p['rows'][r]['kick_reason_id'],p['rows'][r]['kick_reason'],p['rows'][r]['times_kicked'],p['rows'][r]['kick_penalty_hours'],p['rows'][r]['last_time_kicked'])
        #print "Insert => ",t

        #Insert current producer record
        c.execute('insert into state (owner, is_active, kick_reason_id, kick_reason, times_kicked, kick_penalty_hours, last_time_kicked) values (?,?,?,?,?,?,?)', t)

    conn.commit()

    print str(datetime.datetime.now()) + ": State table updated.   Exiting...bye."


#All Done
conn.close()
f.close()
