with open('../disposable_email_blocklist.conf') as blocklist:
    blocklist_content = {line.rstrip() for line in blocklist.readlines()}

email="abc@mail.tempmail.co"
flag=True
domain_parts = email.partition('@')[2].split(".")
for i in range(len(domain_parts)):
    if ".".join(domain_parts[i:]) in blocklist_content:
        print("Disposable email detected.")
        flag=False
        break

if flag:
    print("Email is valid.")
