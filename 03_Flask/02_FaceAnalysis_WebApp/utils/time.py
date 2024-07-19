from datetime import datetime

def relative_time(time):
    input_time = datetime.strptime(str(time), "%Y-%m-%d %H:%M:%S.%f")
    current_time = datetime.now()
    diff = current_time - input_time
    seconds = diff.total_seconds()

    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    
    if seconds < 3600:
        return f"{int(seconds//60)} minutes ago"
    
    if seconds < 86400:
        return f"{int(seconds // 3600)} hours ago"
    
    else:
        return f"{int(seconds // 86400)} days ago"

