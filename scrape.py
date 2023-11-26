import json, time, requests as r, xlsxwriter as x

# To use this script, set the following constants to the correct data corresponding to
# your Keyforge Master Vault account and DecksOfKeyforge account
AUTH_TOKEN = ''
DECK_PAGES = 0
DOK_API_KEY = ''
SESSION_ID = ''
USER_ID = ''

kfmv_decks = []
dok_decks = []

book = x.Workbook('keyscrape_data_test.xlsx')
sheet = book.add_worksheet('Decks')

decks_written = 0

for i in range(1, DECK_PAGES + 1):
    api_val = r.get(
        'https://www.keyforgegame.com/api/users/v2/{}/decks/?page={}&page_size=10&search=&ordering=-date'.format(USER_ID, i),
        headers = {
            'Authorization': 'Token {}'.format(AUTH_TOKEN),
            'Cookie': 'sessionid={}; auth={}'.format(SESSION_ID, AUTH_TOKEN),
            'X-Authorization': 'Token {}'.format(AUTH_TOKEN)
        }
    )
    for deck in api_val.json()['data']:
        kfmv_decks.append(deck)
        r.post(
            'https://decksofkeyforge.com/api/decks/{}/import'.format(deck['id'])
        )
        print('Sent deck {} to DoK API.'.format(deck['name']))
        time.sleep(3) # don't DDOS the Decks of Keyforge API and get locked out

for deck in kfmv_decks:
    dok_deck = r.get(
        'https://decksofkeyforge.com/public-api/v3/decks/{}'.format(deck['id']),
        headers = {
            'Api-Key': DOK_API_KEY
        }
    ).json()['deck']
    time.sleep(3) # don't DDOS the Decks of Keyforge API and get locked out
    try:
        sheet.write(decks_written, 1, dok_deck['name'])
        sheet.write(decks_written, 2, dok_deck['aercScore'])
        sheet.write(decks_written, 3, dok_deck['sasRating'])
        sheet.write(decks_written, 4, dok_deck['housesAndCards'][0]['house'])
        sheet.write(decks_written, 5, dok_deck['housesAndCards'][1]['house'])
        sheet.write(decks_written, 6, dok_deck['housesAndCards'][2]['house'])
        sheet.write(decks_written, 7, dok_deck['expansion'])
        decks_written = decks_written + 1
        print('Wrote deck {} to sheet.'.format(dok_deck['name']))
        dok_decks.append(dok_deck)
    except:
        print('Failed to write deck {} to sheet.'.format(dok_deck))

book.close()

with open("kfmv_decks.json", "w") as text_file:
    text_file.write(json.dumps(kfmv_decks))

with open("dok_decks.json", "w") as text_file:
    text_file.write(json.dumps(kfmv_decks))

