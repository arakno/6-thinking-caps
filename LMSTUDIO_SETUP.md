# LM Studio Setup Guide

This guide explains how to use the 6 Thinking Hats Multi-Agent System with a locally running LM Studio model instead of Google Gemini.

## Overview

The application now supports two LLM providers:
- **Google Gemini** (cloud-based, requires API key)
- **LM Studio** (local model, runs on your machine)

## Prerequisites

1. **LM Studio**: Download and install from [https://lmstudio.ai/](https://lmstudio.ai/)
2. **Model**: Download the `ibm/granite-4-h-tiny` model (or any other compatible model) in LM Studio

## Setup Instructions

### Step 1: Configure LM Studio

1. **Open LM Studio** and navigate to the Models section
2. **Download the model**: Search for `ibm/granite-4-h-tiny` and download it
   - Alternative: You can use any other model available in LM Studio
3. **Start the Local Server**:
   - Go to the "Local Server" tab in LM Studio
   - Select your downloaded model from the dropdown
   - Click "Start Server"
   - Verify it's running at `http://127.0.0.1:1234`

### Step 2: Configure the Application

Edit the `backend/.env` file to use LM Studio:

```env
# LLM Provider Configuration
LLM_PROVIDER=lmstudio

# Google Gemini API (required if LLM_PROVIDER=gemini)
GOOGLE_API_KEY=your_google_api_key_here

# LM Studio Configuration (required if LLM_PROVIDER=lmstudio)
LMSTUDIO_BASE_URL=http://127.0.0.1:1234
LMSTUDIO_MODEL=ibm/granite-4-h-tiny

# Application Settings
DEBUG=True
ENVIRONMENT=development
```

**Configuration Options:**

- `LLM_PROVIDER`: Set to `lmstudio` to use local model, or `gemini` to use Google's API
- `LMSTUDIO_BASE_URL`: The URL where LM Studio is running (default: `http://127.0.0.1:1234`)
- `LMSTUDIO_MODEL`: The model identifier (should match the model you loaded in LM Studio)

### Step 3: Run the Application

```bash
# Terminal 1: Start backend
cd backend
uvicorn app:app --reload

# Terminal 2: Start frontend (in a new terminal)
cd frontend
npm run dev
```

Open your browser to `http://localhost:5173` and start analyzing!

## Using Different Models

If you want to use a different model from LM Studio:

1. Download the model in LM Studio
2. Load it in the Local Server
3. Update `LMSTUDIO_MODEL` in `backend/.env` with the model identifier
4. Restart the backend server

Example with a different model:

```env
LMSTUDIO_MODEL=TheBloke/Llama-2-7B-Chat-GGUF
```

## Switching Between Providers

To switch between LM Studio and Google Gemini, simply change the `LLM_PROVIDER` setting:

**For LM Studio (local):**
```env
LLM_PROVIDER=lmstudio
```

**For Google Gemini (cloud):**
```env
LLM_PROVIDER=gemini
```

Restart the backend after changing the provider.

## Troubleshooting

### Error: "Could not connect to LM Studio"

**Solution:**
1. Verify LM Studio is running and the local server is started
2. Check that the URL is correct (default: `http://127.0.0.1:1234`)
3. Ensure no firewall is blocking the connection

### Error: "LM Studio request timed out"

**Solution:**
1. The model might be too large or your machine too slow
2. Try a smaller/faster model
3. Wait longer - first requests can be slower as the model loads

### Model responses are poor quality

**Solution:**
1. Try a larger or more capable model
2. Adjust temperature settings in `backend/services/lmstudio_client.py` if needed
3. The `ibm/granite-4-h-tiny` model is small - consider using a larger model for better results

### Application still using Gemini

**Solution:**
1. Double-check `LLM_PROVIDER=lmstudio` in `backend/.env`
2. Restart the backend server (`Ctrl+C` and run `uvicorn app:app --reload` again)
3. Check the console logs - they should show "Creating LLM client for provider: lmstudio"

## Performance Considerations

- **Local models** run on your hardware - performance depends on your CPU/GPU
- **First request** may be slower as the model loads into memory
- **Smaller models** (like granite-4-h-tiny) are faster but may produce lower quality results
- **Larger models** produce better results but require more resources and are slower

## Benefits of Using LM Studio

✅ **Privacy**: Your data never leaves your machine  
✅ **No API costs**: Completely free after initial setup  
✅ **Offline capable**: Works without internet connection  
✅ **Customizable**: Use any compatible model  
✅ **No rate limits**: Process as many requests as your hardware can handle

## Architecture

The application uses a factory pattern to support multiple LLM providers:

```
BaseAgent (abstract)
    ↓
LLMClient (interface)
    ↓
    ├── GeminiClient (Google Gemini)
    └── LMStudioClient (Local LM Studio)
```

All agents use the same interface, making it easy to switch between providers without changing agent code.

## Additional Resources

- [LM Studio Documentation](https://lmstudio.ai/docs)
- [Hugging Face Model Hub](https://huggingface.co/models) - Browse available models
- [Project README](./README.md) - General application documentation
