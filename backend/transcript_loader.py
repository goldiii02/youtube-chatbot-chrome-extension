"""
YouTube Transcript Loader
Fetches and processes YouTube video transcripts
"""
import os
import json
import hashlib
from typing import Optional, List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable


class TranscriptLoader:
    """Handles YouTube transcript fetching and caching"""
    
    def __init__(self, cache_dir: str = "./cache"):
        """
        Initialize transcript loader with cache directory
        
        Args:
            cache_dir: Directory to cache transcripts
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, video_id: str) -> str:
        """Generate cache file path for video ID"""
        return os.path.join(self.cache_dir, f"{video_id}.json")
    
    def _load_from_cache(self, video_id: str) -> Optional[List[Dict]]:
        """Load transcript from cache if exists"""
        cache_path = self._get_cache_path(video_id)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading cache: {e}")
        return None
    
    def _save_to_cache(self, video_id: str, transcript: List[Dict]):
        """Save transcript to cache"""
        cache_path = self._get_cache_path(video_id)
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(transcript, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def fetch_transcript(self, video_id: str, languages: List[str] = None) -> List[Dict]:
        """
        Fetch YouTube video transcript
        
        Args:
            video_id: YouTube video ID
            languages: Preferred languages (default: ['en', 'en-US', 'en-GB'])
        
        Returns:
            List of transcript segments with 'text', 'start', and 'duration'
        
        Raises:
            ValueError: If transcript cannot be fetched
        """
        if languages is None:
            languages = ['en', 'en-US', 'en-GB']
        
        # Try loading from cache first
        cached_transcript = self._load_from_cache(video_id)
        if cached_transcript:
            return cached_transcript
        
        try:
            # Try to get transcript in preferred languages
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try fetching manually generated transcript first
            try:
                transcript = transcript_list.find_manually_created_transcript(languages)
            except:
                # Fall back to auto-generated transcript
                transcript = transcript_list.find_generated_transcript(languages)
            
            # Fetch the actual transcript data
            transcript_data = transcript.fetch()
            
            # Save to cache
            self._save_to_cache(video_id, transcript_data)
            
            return transcript_data
            
        except TranscriptsDisabled:
            raise ValueError(f"Transcripts are disabled for video {video_id}")
        except NoTranscriptFound:
            raise ValueError(f"No transcript found for video {video_id}")
        except VideoUnavailable:
            raise ValueError(f"Video {video_id} is unavailable or private")
        except Exception as e:
            raise ValueError(f"Error fetching transcript: {str(e)}")
    
    def get_full_text(self, video_id: str) -> str:
        """
        Get full transcript text as a single string
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            Full transcript text
        """
        transcript = self.fetch_transcript(video_id)
        return " ".join([item['text'] for item in transcript])
    
    def get_text_with_timestamps(self, video_id: str) -> str:
        """
        Get transcript text with timestamps
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            Formatted transcript with timestamps
        """
        transcript = self.fetch_transcript(video_id)
        lines = []
        for item in transcript:
            minutes = int(item['start'] // 60)
            seconds = int(item['start'] % 60)
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            lines.append(f"{timestamp} {item['text']}")
        return "\n".join(lines)

