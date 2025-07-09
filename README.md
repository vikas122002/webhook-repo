# webhook-repo

This is the Flask backend for receiving GitHub webhooks and serving them to the frontend.

## Features
- Receives webhook events (Push, Pull Request, Merge)
- Saves data to MongoDB
- Provides API endpoint for frontend to fetch events

##  Setup

### 1. Clone repo
```bash
git clone https://github.com/vikas122002/webhook-repo.git
cd webhook-repo
