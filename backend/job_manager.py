import os
import json
import time
from datetime import datetime
from threading import Thread

class JobManager:
    def __init__(self, db_dir='db'):
        self.db_dir = db_dir
        self.jobs_file = os.path.join(db_dir, 'build_jobs.json')
        os.makedirs(db_dir, exist_ok=True)
        
        # Initialize jobs file if doesn't exist
        if not os.path.exists(self.jobs_file):
            self._save_jobs({})
    
    def _load_jobs(self):
        """Load jobs from JSON file"""
        try:
            with open(self.jobs_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_jobs(self, jobs):
        """Save jobs to JSON file"""
        with open(self.jobs_file, 'w') as f:
            json.dump(jobs, f, indent=2)
    
    def create_job(self, job_id, app_name, url, has_icon=False):
        """Create a new build job"""
        jobs = self._load_jobs()
        
        jobs[job_id] = {
            'job_id': job_id,
            'app_name': app_name,
            'url': url,
            'has_icon': has_icon,
            'status': 'pending',
            'progress': 0,
            'message': 'Job created, waiting to start...',
            'apk_path': None,
            'error': None,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'completed_at': None
        }
        
        self._save_jobs(jobs)
        return jobs[job_id]
    
    def get_job(self, job_id):
        """Get job details"""
        jobs = self._load_jobs()
        return jobs.get(job_id)
    
    def update_job(self, job_id, **updates):
        """Update job details"""
        jobs = self._load_jobs()
        
        if job_id in jobs:
            jobs[job_id].update(updates)
            jobs[job_id]['updated_at'] = datetime.now().isoformat()
            self._save_jobs(jobs)
            return jobs[job_id]
        return None
    
    def set_processing(self, job_id, message='Processing...'):
        """Set job status to processing"""
        return self.update_job(
            job_id,
            status='processing',
            message=message,
            progress=10
        )
    
    def set_progress(self, job_id, progress, message):
        """Update job progress"""
        return self.update_job(
            job_id,
            progress=progress,
            message=message
        )
    
    def set_completed(self, job_id, apk_path):
        """Set job as completed"""
        return self.update_job(
            job_id,
            status='completed',
            progress=100,
            message='APK build completed successfully!',
            apk_path=apk_path,
            completed_at=datetime.now().isoformat()
        )
    
    def set_failed(self, job_id, error_message):
        """Set job as failed"""
        return self.update_job(
            job_id,
            status='failed',
            message='Build failed',
            error=error_message,
            completed_at=datetime.now().isoformat()
        )
    
    def cleanup_old_jobs(self, days=7):
        """Remove jobs older than specified days"""
        jobs = self._load_jobs()
        current_time = time.time()
        cutoff_time = current_time - (days * 24 * 60 * 60)
        
        jobs_to_keep = {}
        for job_id, job in jobs.items():
            job_time = datetime.fromisoformat(job['created_at']).timestamp()
            if job_time > cutoff_time:
                jobs_to_keep[job_id] = job
        
        self._save_jobs(jobs_to_keep)
        return len(jobs) - len(jobs_to_keep)
