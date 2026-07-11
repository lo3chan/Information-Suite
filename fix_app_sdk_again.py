import re
with open("app/build.gradle.kts", "r") as f:
    content = f.read()

content = re.sub(r'compileSdk = \d+', 'compileSdk = 34', content)
content = re.sub(r'targetSdk = \d+', 'targetSdk = 34', content)

with open("app/build.gradle.kts", "w") as f:
    f.write(content)
