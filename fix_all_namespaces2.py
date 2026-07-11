import re

def add_namespace(filepath, namespace):
    with open(filepath, 'r') as f:
        content = f.read()

    if "namespace" not in content:
        if filepath.endswith('.kts'):
            content = re.sub(r'android\s*\{', f'android {{\n    namespace = "{namespace}"\n', content)
        else:
            content = re.sub(r'android\s*\{', f'android {{\n    namespace "{namespace}"\n', content)

    with open(filepath, 'w') as f:
        f.write(content)

add_namespace("base/build.gradle", "com.bernaferrari.base")
add_namespace("base-android/build.gradle", "com.bernaferrari.ui")
add_namespace("diffutils/build.gradle.kts", "com.bernaferrari.diffutils")
add_namespace("repo/build.gradle", "com.bernaferrari.repo")
