import axios from "axios";
const YT = "https://www.googleapis.com/youtube/v3/search";
export async function searchGuides(q: string) {
  const { data } = await axios.get(YT, {
    params: { key: process.env.YOUTUBE_API_KEY, part: "snippet", q, maxResults: 5, type: "video" }
  });
  return (data.items || []).map((i:any) => ({
    id: i.id.videoId,
    title: i.snippet.title,
    channel: i.snippet.channelTitle
  }));
}


