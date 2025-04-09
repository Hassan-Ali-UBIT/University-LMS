"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Loader2, MessageSquare, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import VideoPlayer from "@/components/lessons/VideoPlayer";
import CommentSection from "@/components/lessons/CommentSection";
import WatchTimeIndicator from "@/components/lessons/WatchTimeIndicator";

// Mock data - replace with actual API calls
const mockLesson = {
  id: "1",
  title: "Introduction to React Hooks",
  description: "Learn the basics of React Hooks and how to use them in your applications.",
  videoUrl: "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
  duration: 600, // 10 minutes in seconds
  watchedTime: 240, // 4 minutes in seconds
  isCompleted: false,
};

export default function LessonView() {
  const params = useParams();
  const lessonId = params.id as string;
  
  const [lesson, setLesson] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [watchProgress, setWatchProgress] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);

  useEffect(() => {
    // Fetch lesson data from API
    // For now, using mock data
    setTimeout(() => {
      setLesson(mockLesson);
      setWatchProgress((mockLesson.watchedTime / mockLesson.duration) * 100);
      setIsCompleted(mockLesson.isCompleted);
      setLoading(false);
    }, 1000);
  }, [lessonId]);

  const handleTimeUpdate = (currentTime: number) => {
    // Update watch progress
    const progress = (currentTime / lesson.duration) * 100;
    setWatchProgress(progress);
    
    // In a real app, you would send this to your backend
    console.log(`Watched ${currentTime} seconds out of ${lesson.duration}`);
  };

  const handleMarkAsComplete = () => {
    // Update completion status
    setIsCompleted(true);
    
    // In a real app, you would send this to your backend
    console.log(`Marked lesson ${lessonId} as complete`);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4 md:px-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <h1 className="text-2xl font-bold mb-4">{lesson.title}</h1>
          
          {/* Video Player */}
          <div className="rounded-lg overflow-hidden mb-6">
            <VideoPlayer 
              videoUrl={lesson.videoUrl} 
              onTimeUpdate={handleTimeUpdate}
            />
          </div>
          
          {/* Watch Progress */}
          <div className="mb-6">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium">
                Watch Progress: {Math.round(watchProgress)}%
              </span>
              <Button 
                variant={isCompleted ? "outline" : "default"}
                size="sm"
                onClick={handleMarkAsComplete}
                disabled={isCompleted}
              >
                <CheckCircle className="mr-2 h-4 w-4" />
                {isCompleted ? "Completed" : "Mark as Complete"}
              </Button>
            </div>
            <Progress value={watchProgress} className="h-2" />
          </div>
          
          {/* Lesson Description */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-2">About this lesson</h2>
            <p className="text-muted-foreground">{lesson.description}</p>
          </div>
          
          <Separator className="my-8" />
          
          {/* Comments Section */}
          <div>
            <div className="flex items-center mb-6">
              <MessageSquare className="mr-2 h-5 w-5" />
              <h2 className="text-xl font-semibold">Discussion</h2>
            </div>
            <CommentSection lessonId={lessonId} />
          </div>
        </div>
        
        {/* Sidebar */}
        <div className="lg:col-span-1">
          <div className="bg-card rounded-lg p-6 shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Watch Time</h2>
            <WatchTimeIndicator 
              duration={lesson.duration}
              watchedTime={lesson.watchedTime}
            />
            
            <Separator className="my-6" />
            
            <div className="space-y-4">
              <h3 className="text-lg font-medium">Resources</h3>
              <ul className="space-y-2">
                <li>
                  <a href="#" className="text-primary hover:underline">Lesson Slides</a>
                </li>
                <li>
                  <a href="#" className="text-primary hover:underline">Exercise Files</a>
                </li>
                <li>
                  <a href="#" className="text-primary hover:underline">Additional Reading</a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
