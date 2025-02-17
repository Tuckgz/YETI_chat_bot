import pickle

# Function to parse the Netscape HTTP Cookie format and convert to a dictionary format suitable for Selenium
def parse_cookies(cookie_file):
    cookies = []
    with open(cookie_file, 'r') as file:
        for line in file:
            if line.startswith('#') or not line.strip():
                continue  # Skip comments and empty lines
            parts = line.strip().split('\t')
            if len(parts) >= 7:
                cookie = {
                    'domain': parts[0],
                    'httpOnly': parts[5] == 'TRUE',
                    'path': parts[2],
                    'secure': parts[3] == 'TRUE',
                    'expiration': int(parts[4]),
                    'name': parts[5],
                    'value': parts[6]
                }
                cookies.append(cookie)
    return cookies

# Save the cookies to a pickle file
def save_cookies(cookies, cookies_file):
    with open(cookies_file, 'wb') as file:
        pickle.dump(cookies, file)

# Example usage:
cookies = parse_cookies('yeti_cookies.txt')
save_cookies(cookies, 'yeti_cookies.pkl')
