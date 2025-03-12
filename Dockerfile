FROM python:3.12.4-slim
WORKDIR /app
COPY . .
RUN pip isstall --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn","src.index:app","--host","0.0.0.0","--port","8000"]