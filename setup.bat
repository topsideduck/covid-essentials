@echo off

pip install -r requirements.txt
cd chatbot
rasa run actions & rasa run -m models --enable-api --cors '*'