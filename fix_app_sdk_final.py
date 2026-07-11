with open("buildSrc/src/main/java/com/bernaferrari/buildsrc/dependencies.kt", "r") as f:
    content = f.read()

content = content.replace('val compileSdk = 33', 'val compileSdk = 34')
content = content.replace('val targetSdk = 33', 'val targetSdk = 34')

with open("buildSrc/src/main/java/com/bernaferrari/buildsrc/dependencies.kt", "w") as f:
    f.write(content)
