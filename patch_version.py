with open("VERSION.md", "w") as f:
    f.write("0.31.0\n")

with open("CHANGELOG.md", "r") as f:
    content = f.read()

content = content.replace(
    "## [0.30.0]",
    "## [0.31.0] - Social Accountability\n- Added `is_public` user privacy property, accessible via Settings.\n- Created `SocialView.vue` and `Community` tab to list users who have their accounts marked as public, along with their recent goals.\n\n## [0.30.0]",
)

with open("CHANGELOG.md", "w") as f:
    f.write(content)
