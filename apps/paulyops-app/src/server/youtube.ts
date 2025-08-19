import axios from 'axios'

const YOUTUBE_API_BASE = 'https://www.googleapis.com/youtube/v3/search'

export interface YouTubeVideo {
  id: string
  title: string
  channel: string
  description: string
  thumbnail: string
  publishedAt: string
}

export async function searchGuides(query: string): Promise<YouTubeVideo[]> {
  try {
    const { data } = await axios.get(YOUTUBE_API_BASE, {
      params: {
        key: process.env.YOUTUBE_API_KEY,
        part: 'snippet',
        q: query,
        maxResults: 5,
        type: 'video',
        videoDuration: 'medium',
        relevanceLanguage: 'en',
        order: 'relevance'
      }
    })

    return data.items?.map((item: any) => ({
      id: item.id.videoId,
      title: item.snippet.title,
      channel: item.snippet.channelTitle,
      description: item.snippet.description,
      thumbnail: item.snippet.thumbnails.medium.url,
      publishedAt: item.snippet.publishedAt
    })) || []
  } catch (error) {
    console.error('YouTube API error:', error)
    return []
  }
}

export async function searchTutorials(topic: string): Promise<YouTubeVideo[]> {
  return searchGuides(`${topic} tutorial guide how to`)
}

export async function searchBestPractices(domain: string): Promise<YouTubeVideo[]> {
  return searchGuides(`${domain} best practices tips`)
}
