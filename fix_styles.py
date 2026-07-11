import re

with open('app/src/main/res/values/styles.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<style name="AboutLight".*?</style>', '', content, flags=re.DOTALL)
content = re.sub(r'<style name="AboutDark".*?</style>', '', content, flags=re.DOTALL)

with open('app/src/main/res/values/styles.xml', 'w') as f:
    f.write(content)
