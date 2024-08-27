import datetime
import time

# Function to get user input for websites to block
def get_websites_to_block():
    websites = []
    print("Enter the websites you want to block (type 'done' to finish):")
    while True:
        website = input("Website: ")
        if website.lower() == 'done':
            break
        websites.append(website)
    return websites

# Get the list of websites to block from the user
site_block = get_websites_to_block()

# Ensure both versions of the domain are blocked
site_block += ["www." + site if not site.startswith("www.") else site.replace("www.", "") for site in site_block]

end_time = datetime.datetime(2024, 8, 31)
host_path = "C:/Windows/System32/drivers/etc/hosts"
redirect = "127.0.0.1"

while True:
    if datetime.datetime.now() < end_time:  # Specifying date if in blocked dates
        print("Start Blocking")
        with open(host_path, "r+") as host_file:
            content = host_file.read()
            for website in site_block:
                if website not in content:
                    host_file.write(redirect + " " + website + "\n")  # Websites that are blocked
                else:
                    pass
    else:  # Removing Blocked Websites
        print("Removing Blocks")
        with open(host_path, "r+") as host_file:
            content = host_file.readlines()
            host_file.seek(0)
            for lines in content:
                if not any(website in lines for website in site_block):
                    host_file.write(lines)
            host_file.truncate()

    time.sleep(5)