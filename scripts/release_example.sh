# Create an annotated tag (recommended for releases)
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push the tag to GitHub
git push origin v1.0.0

# Delete the tag locally
git tag -d v1.0.0

# Delete the tag from GitHub
git push origin --delete v1.0.0