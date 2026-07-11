import re
with open("repo/src/main/AndroidManifest.xml", "r") as f:
    content = f.read()

content = re.sub(r'package="[^"]+"', '', content)

with open("repo/src/main/AndroidManifest.xml", "w") as f:
    f.write(content)
