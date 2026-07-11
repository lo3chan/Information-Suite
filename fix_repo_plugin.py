with open("repo/build.gradle", "r") as f:
    content = f.read()

content = content.replace("apply plugin: 'com.google.devtools.ksp'", "apply plugin: 'kotlin-kapt'")
content = content.replace("ksp Libs2.AndroidX.Room.compiler", "kapt Libs2.AndroidX.Room.compiler")

with open("repo/build.gradle", "w") as f:
    f.write(content)
