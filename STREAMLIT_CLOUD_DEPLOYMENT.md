# Streamlit Cloud Deployment Guide

This guide explains how to deploy MedSafe AI to Streamlit Cloud.

## Prerequisites

1. GitHub account
2. Streamlit Cloud account (sign up at https://streamlit.io/cloud)
3. Cloud-hosted Ollama instance OR alternative AI API (OpenAI, etc.)

## Important Notes

### AI Model Considerations

Streamlit Cloud does not support running Ollama locally. You have two options:

**Option 1: Cloud-Hosted Ollama (Recommended for this project)**
- Deploy Ollama on a cloud server (AWS, DigitalOcean, etc.)
- Expose Ollama API endpoint
- Configure the endpoint in Streamlit secrets

**Option 2: Alternative AI Provider**
- Use OpenAI API, Anthropic Claude, or similar
- Modify code to use alternative AI provider
- Configure API keys in Streamlit secrets

## Deployment Steps

### Step 1: Prepare Repository

1. Ensure all code is committed to GitHub
2. Verify `requirements.txt` is complete
3. Verify `packages.txt` exists (for Tesseract OCR)
4. Verify `.streamlit/config.toml` exists

```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### Step 2: Set Up Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Select branch (usually `main`)
6. Set main file path: `streamlit_app.py`
7. Click "Advanced settings"

### Step 3: Configure Secrets

In the Advanced settings, add secrets:

```toml
[ollama]
base_url = "http://your-ollama-cloud-instance:11434"
model = "llama3"
```

OR if using OpenAI:

```toml
[openai]
api_key = "your-openai-api-key"
model = "gpt-3.5-turbo"
```

### Step 4: Deploy

1. Click "Deploy"
2. Wait for deployment to complete (5-10 minutes)
3. Monitor deployment logs for any errors
4. Access your app at the provided URL

## Code Modifications for Cloud Deployment

### Option 1: Using Cloud-Hosted Ollama

Modify `ocr_utils.py`, `symptom.py`, and `risk_engine.py` to read Ollama URL from secrets:

```python
import streamlit as st

# In __init__ or setup
if "ollama" in st.secrets:
    ollama_url = st.secrets["ollama"]["base_url"]
    ollama_model = st.secrets["ollama"]["model"]
else:
    # Fallback to local
    ollama_url = "http://localhost:11434"
    ollama_model = "llama3"

self.llm = Ollama(
    base_url=ollama_url,
    model=ollama_model
)
```

### Option 2: Using OpenAI API

Replace Ollama with OpenAI in AI-using modules:

```python
import streamlit as st
from langchain_openai import ChatOpenAI

# In __init__ or setup
if "openai" in st.secrets:
    self.llm = ChatOpenAI(
        api_key=st.secrets["openai"]["api_key"],
        model=st.secrets["openai"]["model"]
    )
else:
    # Fallback to Ollama
    from langchain_community.llms import Ollama
    self.llm = Ollama(model="llama3")
```

## Setting Up Cloud-Hosted Ollama

### Using DigitalOcean Droplet

1. Create a Droplet (Ubuntu 22.04, 2GB RAM minimum)
2. SSH into the droplet
3. Install Ollama:

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

4. Pull LLaMA 3 model:

```bash
ollama pull llama3
```

5. Configure Ollama to accept external connections:

```bash
# Edit systemd service
sudo systemctl edit ollama.service

# Add these lines:
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"

# Restart service
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

6. Configure firewall:

```bash
sudo ufw allow 11434/tcp
```

7. Get your droplet's IP address and use it in Streamlit secrets:

```toml
[ollama]
base_url = "http://YOUR_DROPLET_IP:11434"
model = "llama3"
```

### Using AWS EC2

Similar steps, but:
1. Launch EC2 instance (t2.medium or larger)
2. Configure Security Group to allow port 11434
3. Follow same Ollama installation steps
4. Use EC2 public IP in Streamlit secrets

## Tesseract OCR on Streamlit Cloud

Tesseract OCR is automatically installed via `packages.txt`. No additional configuration needed.

## Troubleshooting

### Issue: "Ollama connection failed"

**Solution:**
- Verify your cloud Ollama instance is running
- Check firewall rules allow port 11434
- Verify the base_url in secrets is correct
- Test connection: `curl http://YOUR_IP:11434/api/tags`

### Issue: "Tesseract not found"

**Solution:**
- Verify `packages.txt` exists in repository root
- Verify it contains `tesseract-ocr` and `tesseract-ocr-eng`
- Redeploy the app

### Issue: "Module not found"

**Solution:**
- Verify all dependencies are in `requirements.txt`
- Check for typos in package names
- Ensure version compatibility

### Issue: "Out of memory"

**Solution:**
- Streamlit Cloud has memory limits
- Optimize image processing (resize before OCR)
- Implement caching to reduce redundant operations
- Consider upgrading Streamlit Cloud plan

## Testing Cloud Deployment

After deployment, test all modules:

1. **Medicine Interaction Checker**
   - Test fuzzy matching
   - Verify interaction detection
   - Check database access

2. **Prescription OCR**
   - Upload test prescription
   - Verify OCR extraction
   - Test AI parsing (if enabled)
   - Check interaction detection

3. **Symptom Analyzer**
   - Test with and without AI
   - Verify severity assessment
   - Check recommendations

4. **Side Effect Monitor**
   - Test analysis
   - Verify AI integration
   - Check recommendations

5. **Risk Predictor**
   - Test risk calculation
   - Verify AI safety notes
   - Check recommendations

## Monitoring and Maintenance

### View Logs

1. Go to Streamlit Cloud dashboard
2. Click on your app
3. Click "Manage app"
4. View logs in real-time

### Update Deployment

1. Push changes to GitHub
2. Streamlit Cloud auto-deploys on push
3. Monitor deployment logs
4. Verify changes in deployed app

### Manage Secrets

1. Go to app settings
2. Click "Secrets"
3. Update secrets as needed
4. App automatically restarts

## Cost Considerations

### Streamlit Cloud
- Free tier: 1 app, limited resources
- Paid plans: Multiple apps, more resources
- Check current pricing at https://streamlit.io/cloud

### Cloud-Hosted Ollama
- DigitalOcean Droplet: ~$12-24/month (2-4GB RAM)
- AWS EC2: ~$15-30/month (t2.medium)
- Consider reserved instances for cost savings

### Alternative: OpenAI API
- Pay per token usage
- More expensive for high usage
- No server maintenance required
- Check pricing at https://openai.com/pricing

## Security Best Practices

1. **Never commit secrets to repository**
   - Use `.gitignore` for `secrets.toml`
   - Use Streamlit Cloud secrets management

2. **Secure your Ollama instance**
   - Use firewall rules
   - Consider VPN or private network
   - Implement authentication if possible

3. **Limit API access**
   - Use API keys with limited permissions
   - Monitor usage and set alerts
   - Rotate keys regularly

4. **HTTPS**
   - Streamlit Cloud provides HTTPS automatically
   - Ensure Ollama instance uses HTTPS (or VPN)

## Rollback Procedure

If deployment fails:

1. Go to Streamlit Cloud dashboard
2. Click "Manage app"
3. Click "Reboot app" or "Redeploy"
4. Or revert GitHub commit and redeploy

## Support

- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-community-cloud
- Streamlit Forum: https://discuss.streamlit.io/
- Ollama Docs: https://github.com/ollama/ollama

## Next Steps

After successful deployment:

1. Share app URL with users
2. Monitor usage and performance
3. Gather user feedback
4. Plan improvements and updates
5. Consider custom domain (paid feature)
