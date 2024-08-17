from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/download")
async def download_youtube_channel_videos(channel_url: str = Form(...), num_videos: int = Form(...)):
    urls = get_links(channel_url)
    if len(urls) < num_videos:
        return {"message": f"Only {len(urls)} videos found, downloading all of them."}
    download_content(urls, num_videos, "./videos")
    return {"message": "Download started successfully!"}

def download_youtube_video(url, save_path='./videos'):
    ydl_opts = {
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        print("Downloaded successfully!")

def get_links(channel_url: str):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(channel_url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    anchors = soup.find_all('a', id='video-title')
    href_list = [a.get('href') for a in anchors if a.get('href')]
    driver.quit()
    return href_list

def download_content(url_list: list, n: int, path='.'):
    print("Links are being downloaded!")
    for i in range(n):
        print(f"DOWNLOADING {i+1} of {n}")
        download_youtube_video(f"https://www.youtube.com{url_list[i]}", save_path=path)

if __name__ == "main":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)