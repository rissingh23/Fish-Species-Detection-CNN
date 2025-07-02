# Fish-Species-Detection-CNN
Fish species detection based on images and videos using a convolutional neural network. 

Using https://www.kaggle.com/datasets/crowww/a-large-scale-fish-dataset for dataset. 

File: README.md (root)

# Fish Species Classifier

This repository contains a FastAPI backend and a React frontend for uploading a fish image and receiving a predicted species along with extra info.

## Structure


fish-classifier/
├── backend/         # FastAPI app
├── frontend/        # React UI
├── .gitignore
└── README.md        # This file


## Getting Started

1. Clone the repo:
   ```bash
git clone git@github.com:YOUR_USERNAME/fish-classifier.git
cd fish-classifier

Run the backend 

# Backend (FastAPI)

## Setup
```bash
cd backend
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

Run the frontend 

## Setup
```bash
cd frontend
npm install
npm start