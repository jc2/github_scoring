from fastapi import FastAPI, HTTPException

from clients.github import is_popular, GitHubClientError

app = FastAPI()


@app.get("/api/v1/score/{username}/{repo_name}")
def read_item(username: str, repo_name: str):

    try:
        response = is_popular(username, repo_name)
    except GitHubClientError as e:
        raise HTTPException(status_code=400,
                            detail=f"Error ocurring calling Github: Error number: {e.code} - {e.message}")

    return {"is_popular": response}
