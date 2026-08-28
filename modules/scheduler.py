"""
Scheduler Module
Video generation और upload को schedule करता है
Daily, weekly, या custom intervals पर
"""

import schedule
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TaskScheduler:
    def __init__(self, autopilot):
        """
        Initialize scheduler
        
        Args:
            autopilot: YouTubeAutopilot instance
        """
        self.autopilot = autopilot
        self.config = autopilot.config
    
    def schedule_daily(self, time_str='10:00'):
        """
        हर दिन एक specific time पर upload करो
        
        Args:
            time_str: Time in 'HH:MM' format (e.g., '10:00')
        """
        schedule.every().day.at(time_str).do(self.autopilot.generate_video_content)
        logger.info(f"✅ Scheduled daily upload at {time_str}")
    
    def schedule_multiple_daily(self, times):
        """
        हर दिन multiple times पर upload करो
        
        Args:
            times: List of times (e.g., ['09:00', '14:00', '20:00'])
        """
        for time_str in times:
            schedule.every().day.at(time_str).do(self.autopilot.generate_video_content)
            logger.info(f"✅ Scheduled upload at {time_str}")
    
    def schedule_weekly(self, day='monday', time_str='10:00'):
        """
        हर हफ्ते एक specific दिन पर upload करो
        
        Args:
            day: Day name (e.g., 'monday', 'tuesday')
            time_str: Time in 'HH:MM' format
        """
        day_func = getattr(schedule.every(), day.lower())
        day_func.at(time_str).do(self.autopilot.generate_video_content)
        logger.info(f"✅ Scheduled weekly upload every {day} at {time_str}")
    
    def schedule_interval(self, hours=6):
        """
        हर N घंटों में upload करो
        
        Args:
            hours: Interval in hours
        """
        schedule.every(hours).hours.do(self.autopilot.generate_video_content)
        logger.info(f"✅ Scheduled upload every {hours} hours")
    
    def start(self):
        """Scheduler को start करो और continuously चलाओ"""
        logger.info("🔄 Starting scheduler...")
        logger.info("⏰ Press Ctrl+C to stop")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("⏹️  Scheduler stopped")
            self.stop()
    
    def stop(self):
        """Scheduler को stop करो"""
        schedule.clear()
        logger.info("✅ All scheduled tasks cleared")
    
    def get_jobs(self):
        """सभी scheduled jobs को दिखाओ"""
        jobs = schedule.get_jobs()
        logger.info(f"📋 Total scheduled jobs: {len(jobs)}")
        
        for i, job in enumerate(jobs, 1):
            logger.info(f"  {i}. {job}")
        
        return jobs
    
    def remove_job(self, job):
        """किसी specific job को remove करो"""
        schedule.cancel_job(job)
        logger.info(f"✅ Job removed: {job}")
