from sqlalchemy.orm import Session
from models.notes import Notes

def retrive_data(db: Session, user_id: int):
    data = []
    notes = db.query(Notes).filter(Notes.user_id == user_id).all()
    for note in notes:
        data.append(
            {
                "title": note.title,
                "user_id": note.user_id,
                "timestamp": note.created_at,
                "content": note.content,
            }
        )
    return data

def download_user_memories(db: Session, user_id: int):
    data = retrive_data(db, user_id)
    yield """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>My Memories</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f5f5f5;
                padding: 40px;
            }
            .container {
                max-width: 700px;
                background: white;
                padding: 30px;
                margin: 20px auto;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
            }
            .meta {
                font-size: 0.9em;
                color: #777;
                margin-bottom: 20px;
            }
            .content {
                font-size: 1.1em;
                line-height: 1.6;
                color: #444;
            }
        </style>
    </head>
    <body>
    """
    for item in data:
        yield f"""
        <div class="container">
        <h1>{item["title"]}</h1>
            <div class="meta">
                User ID: {item["user_id"]}<br>
                Created at: {item["timestamp"]}
            </div>
            <div class="content">
                {item["content"]}
            </div>
        </div>
        """
    yield """
    </body>
    </html>
    """