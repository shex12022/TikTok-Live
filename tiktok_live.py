#!/usr/bin/env python3
import asyncio
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ViewerCountUpdateEvent, LikeEvent, CommentEvent
from datetime import datetime

class LiveMonitor:
    def __init__(self, username: str):
        self.client = TikTokLiveClient(f"@{username}")
        self.start_time = datetime.now()
        self.max_viewers = 0
        self.likes = 0
        self.comments = 0
        self.current_viewers = 0

        # 🎯 Event listeners
        self.client.add_listener("viewer_count_update", self.update_viewers)
        self.client.add_listener("like", self.add_like)
        self.client.add_listener("comment", self.add_comment)

    async def start(self):
        try:
            await self.client.start()
            print("\n🔥 Connected to LIVE! Press Ctrl+C to exit")
        except Exception as e:
            print(f"\n❌ Connection failed: {str(e)}")

    def update_viewers(self, event: ViewerCountUpdateEvent):
        self.current_viewers = event.viewer_count
        self.max_viewers = max(self.max_viewers, event.viewer_count)

    def add_like(self, event: LikeEvent):
        self.likes += event.like_count

    def add_comment(self, event: CommentEvent):
        self.comments += 1

    def show_stats(self):
        duration = datetime.now() - self.start_time
        print(f"\n📊 LIVE @ {datetime.now().strftime('%H:%M:%S')}")
        print(f"👀 Viewers: {self.current_viewers} | ❤️ Likes: {self.likes}")
        print(f"💬 Comments: {self.comments} | 🚀 Peak: {self.max_viewers}")
        print(f"⏱️ Duration: {duration}\n{'━'*30}")

async def main():
    url = input("\n🎬 Enter TikTok LIVE URL: ").strip()
    username = url.split("/")[3].replace("@", "") if "@" in url else url
    
    monitor = LiveMonitor(username)
    await monitor.start()
    
    while True:
        await asyncio.sleep(2)
        monitor.show_stats()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Session stopped!")