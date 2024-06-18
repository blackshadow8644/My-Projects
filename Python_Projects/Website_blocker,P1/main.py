import os

def block_website(website):
    # Get the full path to the hosts file (different for each OS)
    hosts_path = os.path.join(r"C:\\Windows\System32\drivers\etc", "hosts")  # For Windows
    # Modify the path for MacOS or Linux based on your system

    # Open the hosts file in append mode
    with open(hosts_path, "a") as hosts_file:
        # Add a new line mapping the website to the loopback address (127.0.0.1)
        hosts_file.write(f"\n127.0.0.1 {website}")

website = input("Enter webiste url")
block_website(website)
print(f"Website {website} blocked successfully!")
