#!/bin/bash
# Build script for GitHub Pages deployment
# Copies necessary files to build directory

set -e

echo "🔨 Starting build process..."

# Create build directory if it doesn't exist
mkdir -p build/web
mkdir -p build/diary

# Copy main files
echo "📄 Copying project-intro.html..."
cp project-intro.html build/

# Copy web directory
echo "🌐 Copying web assets..."
cp -r web/*.html build/web/ 2>/dev/null || true

# Copy diary files if they exist
if [ -d "diary" ]; then
    echo "📔 Copying diary files..."
    cp diary/*.html build/diary/ 2>/dev/null || true
fi

# Copy other necessary directories
for dir in docs analytics; do
    if [ -d "$dir" ] && [ "$(ls -A $dir 2>/dev/null)" ]; then
        echo "📁 Copying $dir..."
        cp -r $dir build/ 2>/dev/null || true
    fi
done

echo "✅ Build complete!"
echo "📂 Files in build directory:"
ls -lh build/
