import re
with open("app/build.gradle.kts", "r") as f:
    content = f.read()

if "namespace" not in content:
    content = re.sub(r'android\s*\{', 'android {\n    namespace = "com.bernaferrari.changedetection"\n', content)

with open("app/build.gradle.kts", "w") as f:
    f.write(content)
