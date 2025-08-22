# 🚀 QuintAI Deployment Guide - Render

This guide will walk you through deploying your QuintAI application to Render, making it accessible to the world!

## 📋 Prerequisites

Before deploying, ensure you have:

1. **GitHub Repository**: Your QuintAI project pushed to GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **API Keys**: All required API keys ready
4. **PDF File**: Your source PDF file in the repository

## 🎯 Deployment Strategy

We'll deploy **two services** on Render:

1. **QuintAI API Server** (`quintai-api`) - Python web service
2. **QuintAI Website** (`quintai-website`) - Static website

## 🚀 Step-by-Step Deployment

### **Step 1: Prepare Your Repository**

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Verify these files are in your repo**:
   - `api_server_prod.py` ✅
   - `requirements_prod.txt` ✅
   - `render.yaml` ✅
   - `start_prod.sh` ✅
   - `index.html` ✅
   - All your agent files ✅

### **Step 2: Deploy to Render**

#### **Option A: Using render.yaml (Recommended)**

1. **Connect GitHub to Render**:
   - Go to [render.com](https://render.com)
   - Sign in/Sign up
   - Click "New +" → "Blueprint"
   - Connect your GitHub account
   - Select your QuintAI repository

2. **Deploy with Blueprint**:
   - Render will automatically detect `render.yaml`
   - Click "Apply" to deploy both services
   - Wait for deployment to complete

#### **Option B: Manual Deployment**

1. **Deploy API Server**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Configure:
     - **Name**: `quintai-api`
     - **Environment**: `Python`
     - **Build Command**: `pip install -r requirements_prod.txt`
     - **Start Command**: `gunicorn api_server_prod:app`
     - **Plan**: `Starter` (free tier)

2. **Deploy Website**:
   - Click "New +" → "Static Site"
   - Connect your GitHub repo
   - Configure:
     - **Name**: `quintai-website`
     - **Build Command**: `echo "Static site - no build needed"`
     - **Publish Directory**: `.`

### **Step 3: Configure Environment Variables**

In your **API Server** service, add these environment variables:

1. **GROQ_API_KEY**: Your Groq API key
2. **GROQ1_API_KEY**: Your second Groq API key (for judge)
3. **GEMINI_API_KEY**: Your Google Gemini API key

**How to add them**:
- Go to your API service dashboard
- Click "Environment" tab
- Add each variable with its value
- Click "Save Changes"

### **Step 4: Deploy PDF and Data Files**

**Important**: Your PDF file and ChromaDB need to be accessible in production.

#### **Option A: Include in Repository**
```bash
# Add PDF to git (if not too large)
git add "A Psycho-Cybernetics__-_Maxwell_Maltz.pdf"
git commit -m "Add PDF for production"
git push origin main
```

#### **Option B: Use Render's Persistent Disk**
- In your API service, enable "Persistent Disk"
- Upload your PDF and ChromaDB files
- Update file paths in your code

### **Step 5: Test Your Deployment**

1. **Check API Health**:
   ```
   https://quintai-api.onrender.com/health
   ```

2. **Test API Endpoint**:
   ```bash
   curl -X POST https://quintai-api.onrender.com/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What is artificial intelligence?"}'
   ```

3. **Visit Your Website**:
   ```
   https://quintai-website.onrender.com
   ```

## 🔧 Configuration Details

### **API Server Configuration**

- **Port**: Automatically set by Render (`$PORT`)
- **Workers**: 1 (free tier limitation)
- **Timeout**: 120 seconds (for long AI processing)
- **Health Check**: `/health` endpoint

### **Website Configuration**

- **Static Files**: Served from root directory
- **SPA Routing**: All routes redirect to `index.html`
- **CORS**: Configured for production domains

## 🚨 Common Issues & Solutions

### **Issue 1: Module Import Errors**
```
Error: No module named 'flask'
```
**Solution**: Ensure `requirements_prod.txt` is in your repo and contains all dependencies.

### **Issue 2: API Keys Not Working**
```
Error: API key not found
```
**Solution**: Check environment variables in Render dashboard.

### **Issue 3: PDF File Not Found**
```
Error: PDF file not accessible
```
**Solution**: Include PDF in repository or use persistent disk.

### **Issue 4: CORS Errors**
```
Error: CORS policy violation
```
**Solution**: Check CORS configuration in `api_server_prod.py`.

### **Issue 5: Timeout Errors**
```
Error: Request timeout
```
**Solution**: Increase timeout in Render service settings.

## 📊 Monitoring & Maintenance

### **Health Checks**
- Monitor `/health` endpoint
- Set up alerts for unhealthy status
- Check Render logs regularly

### **Performance Monitoring**
- Monitor response times
- Check memory usage
- Watch for timeout issues

### **Updates**
- Push changes to GitHub
- Render auto-deploys on push
- Monitor deployment logs

## 🌐 Custom Domain (Optional)

1. **Add Custom Domain**:
   - Go to your website service
   - Click "Settings" → "Custom Domains"
   - Add your domain
   - Update DNS records

2. **Update CORS**:
   - Edit `api_server_prod.py`
   - Add your domain to CORS origins

## 💰 Cost Optimization

### **Free Tier Limits**:
- **API Server**: 750 hours/month
- **Website**: Unlimited
- **Bandwidth**: 100GB/month

### **Upgrade When**:
- Exceed free tier limits
- Need better performance
- Want custom domains
- Need persistent storage

## 🎉 Success Checklist

- [ ] Both services deployed successfully
- [ ] Environment variables configured
- [ ] PDF file accessible
- [ ] API health check passes
- [ ] Website loads correctly
- [ ] Live demo works
- [ ] All agents responding
- [ ] Judge LLM working

## 🔗 Useful Links

- [Render Documentation](https://render.com/docs)
- [Python on Render](https://render.com/docs/deploy-python)
- [Static Sites on Render](https://render.com/docs/static-sites)
- [Environment Variables](https://render.com/docs/environment-variables)

## 🆘 Getting Help

1. **Check Render Logs**: Service dashboard → Logs
2. **Render Status**: [status.render.com](https://status.render.com)
3. **Community**: [Render Community](https://community.render.com)
4. **Support**: [Render Support](https://render.com/support)

---

**🎯 Your QuintAI will be live at:**
- **Website**: `https://quintai-website.onrender.com`
- **API**: `https://quintai-api.onrender.com`

**🚀 Share your AI system with the world!** 🤖✨ 