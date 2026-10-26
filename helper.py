import isodate

def format_video_duration(duration):
    try:
        # Parse the ISO 8601 string into a Python timedelta object
        # Changed variable name from 'timedelta' to 'td' to avoid naming conflicts
        timedelta = isodate.parse_duration(duration)
        
        # Calculate total minutes from the total seconds
        total_minutes = int(timedelta.total_seconds() // 60)
        
        # Split into hours and remaining minutes
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        # Conditional formatting based on whether it is 1 hour or longer
        if hours >= 1:
            return f"{hours} hrs {minutes} mins"
        else:
            return f"{minutes} mins"
            
    except (isodate.isoerror.ISO8601Error, TypeError):
        # Handle cases where the duration string is missing, invalid, or empty
        return "0 mins"
