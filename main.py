from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
import strawberry
import sqlite3
from typing import List

app = FastAPI()

# 啟用 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 允許 React 應用的源
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有方法
    allow_headers=["*"],  # 允許所有頭
)

@strawberry.type
class BlogPost:
    id: int
    title: str
    content: str
    date: str
    blog_name: str

@strawberry.type
class Query:
    @strawberry.field
    def blog_posts(self, page: int = 1, per_page: int = 10) -> List[BlogPost]:
        conn = sqlite3.connect('blogdb.sqlite')
        cur = conn.cursor()
        offset = (page - 1) * per_page
        cur.execute("SELECT id, title, content, date, blog_name FROM blog_posts LIMIT ? OFFSET ?", (per_page, offset))
        posts = cur.fetchall()
        cur.close()
        conn.close()
        
        return [BlogPost(id=p[0], title=p[1], content=p[2], date=p[3], blog_name=p[4]) for p in posts]

    @strawberry.field
    def total_posts(self) -> int:
        conn = sqlite3.connect('blogdb.sqlite')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM blog_posts")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "Welcome to the Blog Scraper API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)