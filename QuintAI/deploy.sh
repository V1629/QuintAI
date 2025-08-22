#!/bin/bash

echo "🚀 QuintAI Deployment Script"
echo "=============================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    echo "Please run this script from your QuintAI project directory"
    exit 1
fi

# Check if all required files exist
echo "📋 Checking required files..."
required_files=(
    "api_server_prod.py"
    "requirements_prod.txt"
    "render.yaml"
    "start_prod.sh"
    "index.html"
    "agent1.py"
    "agent2.py"
    "agent3.py"
    "agent4.py"
    "judgellm.py"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ Missing required files:"
    printf '   %s\n' "${missing_files[@]}"
    echo "Please ensure all files are present before deploying"
    exit 1
fi

echo "✅ All required files found"

# Check git status
echo "📊 Checking git status..."
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  You have uncommitted changes:"
    git status --short
    echo ""
    read -p "Do you want to commit these changes? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter commit message: " commit_msg
        git add .
        git commit -m "${commit_msg:-Prepare for Render deployment}"
        echo "✅ Changes committed"
    else
        echo "⚠️  Please commit your changes before deploying"
        exit 1
    fi
fi

# Check if we're up to date with remote
echo "🔄 Checking remote status..."
git fetch origin
if [ "$(git rev-list HEAD...origin/main --count)" != "0" ]; then
    echo "⚠️  Your local branch is not up to date with remote"
    echo "Please pull the latest changes:"
    echo "   git pull origin main"
    exit 1
fi

echo "✅ Local branch is up to date"

# Push to remote
echo "🚀 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub"
    echo ""
    echo "🎯 Next Steps:"
    echo "1. Go to https://render.com"
    echo "2. Sign in/Sign up"
    echo "3. Click 'New +' → 'Blueprint'"
    echo "4. Connect your GitHub account"
    echo "5. Select your QuintAI repository"
    echo "6. Click 'Apply' to deploy"
    echo ""
    echo "📋 Don't forget to:"
    echo "- Set environment variables in Render"
    echo "- Ensure your PDF file is accessible"
    echo "- Test the deployment"
    echo ""
    echo "🌐 Your QuintAI will be available at:"
    echo "- Website: https://quintai-website.onrender.com"
    echo "- API: https://quintai-api.onrender.com"
else
    echo "❌ Failed to push to GitHub"
    exit 1
fi 