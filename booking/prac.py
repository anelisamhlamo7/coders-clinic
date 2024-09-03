def create_events_or_slots():

    event1 = {
        'summary': 'code-clinic session1',
        'location': 'Cape Town Campus- booth 2',
        'description': 'one-on-one session advise on the coding problem at hand.',
        'colorId': 6,
        'start': {
            'dateTime': '2024-03-02T14:00:00', 
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': '2024-03-02T14:30:00',
            'timeZone': 'Africa/Johannesburg',
        },
        'attendees': [
             
        ]
    }

    return event1


volunteers = [{     'slot1': 'lee@gmail.com',
                    'slot2': 'thabo@gmail.com',
                    'slot3': 'sam@gmail.com'
                }]
    

def handling_slots():

    event = create_events_or_slots()
            
    booked_slot = volunteers[0]['slot2']

    user = input('enter email: ')
    
    emails = [booked_slot, user]


    event["attendees"].append({'email':emails[0]})
    event["attendees"].append({'email' : user})

    print (event)

handling_slots()