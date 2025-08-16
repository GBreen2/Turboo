import requests, json

API_URL = "https://ffm-jwt-bot-info.vercel.app/token?uid={}&password={}"

def generate_tokens(input_file):
    try:
        with open(input_file) as f:
            accounts = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: '{input_file}' is not valid JSON or is empty.")
        return
    
    result = {'IND': [], 'BR': [], 'BD': []}
    
    for account in accounts:
        try:
            print(f"Processing: {account['uid']}", end=' ')
            response = requests.get(API_URL.format(account['uid'], account['password']), timeout=5).json()
            
            if 'token' in response:
                region_code = response.get('notiRegion', '').upper()
                if region_code == 'IND':
                    region = 'IND'
                elif region_code in {'BR', 'US', 'SAC', 'NA'}:
                    region = 'BR'
                else:
                    region = 'BD'
                
                result[region].append({
                    'uid': account['uid'],
                    'token': response['token']
                })
                print(f"OK({region})")
            else:
                print("FAIL(no token)")
        except Exception as e:
            print(f"FAIL(error: {str(e)})")
    
    # Save the results by region
    for region, tokens in result.items():
        if tokens:
            filename = f'token_{region.lower()}.json'
            with open(filename, 'w') as f:
                json.dump(tokens, f)
            print(f"Saved {len(tokens)} tokens to {filename}")

generate_tokens("accounts.json")