"use client";

import { Clock } from "lucide-react";
import { Progress } from "@/components/ui/progress";

interface WatchTimeIndicatorProps {
  duration: number; // in seconds
  watchedTime: number; // in seconds
}

export default function WatchTimeIndicator({ duration, watchedTime }: WatchTimeIndicatorProps) {
  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    
    if (hours > 0) {
      const remainingMinutes = minutes % 60;
      return `${hours}h ${remainingMinutes}m`;
    }
    
    return `${minutes}m`;
  };
  
  const percentageWatched = (watchedTime / duration) * 100;
  
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center text-muted-foreground">
          <Clock className="mr-2 h-4 w-4" />
          <span className="text-sm">Total Duration: {formatTime(duration)}</span>
        </div>
        <span className="text-sm font-medium">{Math.round(percentageWatched)}% complete</span>
      </div>
      
      <Progress value={percentageWatched} className="h-2" />
      
      <div className="grid grid-cols-2 gap-4 mt-4">
        <div className="bg-muted rounded-md p-3">
          <p className="text-xs text-muted-foreground mb-1">Watched</p>
          <p className="font-medium">{formatTime(watchedTime)}</p>
        </div>
        <div className="bg-muted rounded-md p-3">
          <p className="text-xs text-muted-foreground mb-1">Remaining</p>
          <p className="font-medium">{formatTime(duration - watchedTime)}</p>
        </div>
      </div>
    </div>
  );
}
