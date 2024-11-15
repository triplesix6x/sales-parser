from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn


app = FastAPI(
    default_response_class=ORJSONResponse)


def main():
    uvicorn.run(
        "main:app",
        reload=True)


if __name__ == "__main__":
    main()
