# 🚀 GitHub Pages Deployment Guide

This guide will walk you through publishing your **DOI Data Collector** application on GitHub Pages.

## 📋 **Prerequisites**

- ✅ GitHub account
- ✅ Git installed on your computer
- ✅ Your project code ready

## 🎯 **Step-by-Step Deployment**

### **Step 1: Create GitHub Repository**

1. **Go to GitHub.com** and sign in
2. **Click "New repository"** (green button)
3. **Repository name**: `ddc-publication-extractor` (or your preferred name)
4. **Description**: `Publication Metadata Extractor using OpenAlex API`
5. **Make it Public** (required for free GitHub Pages)
6. **Don't initialize** with README (we already have one)
7. **Click "Create repository"**

### **Step 2: Push Your Code to GitHub**

```bash
# Navigate to your project directory
cd /path/to/your/DDC/project

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial commit: DOI Data Collector application"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/ddc-publication-extractor.git

# Push to GitHub
git push -u origin main
```

### **Step 3: Enable GitHub Pages**

1. **Go to your repository** on GitHub
2. **Click "Settings"** tab
3. **Scroll down to "Pages"** section (left sidebar)
4. **Source**: Select "Deploy from a branch"
5. **Branch**: Select "gh-pages" (will be created automatically)
6. **Folder**: Leave as "/ (root)"
7. **Click "Save"**

### **Step 4: Automatic Deployment**

The GitHub Actions workflow will automatically:
- ✅ **Build and test** your application
- ✅ **Deploy to gh-pages branch**
- ✅ **Make it available** at `https://YOUR_USERNAME.github.io/ddc-publication-extractor`

## 🌐 **Your Live Application**

Once deployed, your application will be available at:
```
https://YOUR_USERNAME.github.io/ddc-publication-extractor
```

## 🔧 **What's Included in the Static Version**

### **Features:**
- ✅ **Same beautiful design** as your Flask app
- ✅ **DOI processing** with OpenAlex API
- ✅ **Results display** in responsive table
- ✅ **CSV download** functionality
- ✅ **Professional color scheme** and logo
- ✅ **Mobile responsive** design

### **Technical Details:**
- **Frontend Only**: Runs entirely in the browser
- **API Integration**: Direct calls to OpenAlex API
- **No Backend**: No server required
- **CORS Handling**: Built-in error handling
- **Rate Limiting**: Respects API limits

## 📁 **File Structure for GitHub Pages**

```
docs/
├── index.html          # Main application
├── assets/
│   └── ddc_logo.png   # Your logo
└── README.md          # Documentation

.github/
└── workflows/
    └── deploy.yml     # Auto-deployment workflow
```

## 🚨 **Important Notes**

### **API Limitations:**
- **OpenAlex API** is free but has rate limits
- **CORS restrictions** may apply in some browsers
- **API availability** depends on OpenAlex service

### **Browser Compatibility:**
- ✅ **Chrome/Edge**: Full support
- ✅ **Firefox**: Full support
- ✅ **Safari**: Full support
- ⚠️ **Mobile browsers**: May have limitations

## 🔄 **Updating Your Live Application**

### **Automatic Updates:**
1. **Make changes** to your code
2. **Commit and push** to GitHub
3. **GitHub Actions** automatically deploys
4. **Your live site updates** within minutes

### **Manual Updates:**
```bash
# Make your changes
# Then push to GitHub
git add .
git commit -m "Update application"
git push origin main
```

## 🐛 **Troubleshooting**

### **Common Issues:**

#### **Page Not Loading:**
- Check if GitHub Pages is enabled
- Verify the gh-pages branch exists
- Wait a few minutes for deployment

#### **Logo Not Showing:**
- Ensure `docs/assets/ddc_logo.png` exists
- Check file permissions
- Verify image path in HTML

#### **API Errors:**
- Check browser console for CORS errors
- Verify OpenAlex API is accessible
- Check network connectivity

### **Debug Steps:**
1. **Check GitHub Actions** for build errors
2. **Verify file structure** in docs folder
3. **Test locally** before pushing
4. **Check browser console** for JavaScript errors

## 🎉 **Success!**

Once deployed, you'll have:
- 🌐 **Public URL** for your application
- 🔄 **Automatic updates** on every push
- 📱 **Mobile-friendly** interface
- 🎨 **Professional appearance**
- 📊 **Full functionality** without hosting costs

## 📞 **Need Help?**

- **GitHub Issues**: Create an issue in your repository
- **GitHub Pages Docs**: [pages.github.com](https://pages.github.com)
- **GitHub Actions**: Check the Actions tab in your repository

---

**Your DOI Data Collector is now ready to go live on the web!** 🚀
