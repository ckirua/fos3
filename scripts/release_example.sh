# Create an annotated tag (recommended for releases)
git tag -a v0.0.2 -m "Release version 0.0.2"

# Push the tag to GitHub
git push origin v0.0.2

# Delete the tag locally
git tag -d v0.0.2

# Delete the tag from GitHub
git push origin --delete v0.0.2