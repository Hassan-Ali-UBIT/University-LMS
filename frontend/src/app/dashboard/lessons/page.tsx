"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Progress } from "@/components/ui/progress";
import { Search, ChevronLeft, ChevronRight } from "lucide-react";

// Dummy data for lessons
const dummyLessons = [
  {
    id: 1,
    title: "Introduction to React",
    description: "Learn the basics of React and its core concepts",
    progress: 75,
    duration: "2 hours",
    thumbnail: "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800&auto=format&fit=crop&q=60",
  },
  {
    id: 2,
    title: "Advanced TypeScript",
    description: "Deep dive into TypeScript advanced features",
    progress: 30,
    duration: "3 hours",
    thumbnail: "https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=800&auto=format&fit=crop&q=60",
  },
  {
    id: 3,
    title: "Next.js Fundamentals",
    description: "Master the basics of Next.js framework",
    progress: 90,
    duration: "4 hours",
    thumbnail: "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800&auto=format&fit=crop&q=60",
  },
  {
    id: 4,
    title: "CSS Grid Layout",
    description: "Learn modern CSS Grid layout techniques",
    progress: 45,
    duration: "2.5 hours",
    thumbnail: "https://images.unsplash.com/photo-1507721999472-8ed4421c4af2?w=800&auto=format&fit=crop&q=60",
  },
  {
    id: 5,
    title: "State Management",
    description: "Understanding state management in React",
    progress: 60,
    duration: "3.5 hours",
    thumbnail: "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&auto=format&fit=crop&q=60",
  },
  {
    id: 6,
    title: "API Integration",
    description: "Learn how to integrate APIs in your applications",
    progress: 85,
    duration: "2 hours",
    thumbnail: "https://images.unsplash.com/photo-1555066931-4365d14e8c96?w=800&auto=format&fit=crop&q=60",
  },
  {
    id: 7,
    title: "Testing with Jest",
    description: "Master testing your React applications",
    progress: 20,
    duration: "4 hours",
    thumbnail: "https://images.unsplash.com/photo-1507721999472-8ed4421c4af2?w=800&auto=format&fit=crop&q=60",
  },
  {
    id: 8,
    title: "Performance Optimization",
    description: "Learn techniques to optimize React applications",
    progress: 50,
    duration: "3 hours",
    thumbnail: "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&auto=format&fit=crop&q=60",
  },
  {
    id: 9,
    title: "Authentication & Authorization",
    description: "Implement secure authentication in your apps",
    progress: 70,
    duration: "2.5 hours",
    thumbnail: "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800&auto=format&fit=crop&q=60",
  },
];

const ITEMS_PER_PAGE = 6;

export default function LessonsPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [lessons] = useState(dummyLessons);

  const filteredLessons = lessons.filter((lesson) =>
    lesson.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const totalPages = Math.ceil(filteredLessons.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;
  const currentLessons = filteredLessons.slice(startIndex, endIndex);

  return (
    <div className="container mx-auto p-4 space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <h1 className="text-3xl font-bold">Lessons</h1>
        <Dialog>
          <DialogTrigger asChild>
            <Button>Create Lesson</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[600px]">
            <DialogHeader>
              <DialogTitle>Create New Lesson</DialogTitle>
              <DialogDescription>
                Add a new lesson with video and materials
              </DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <Label htmlFor="title">Title</Label>
                <Input id="title" placeholder="Enter lesson title" />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="content">Content</Label>
                <Textarea
                  id="content"
                  placeholder="Enter lesson content"
                  className="min-h-[100px]"
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="video">Video File (Optional)</Label>
                <Input id="video" type="file" accept="video/*" />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="materials">Lesson Materials (Optional)</Label>
                <Input id="materials" type="file" multiple />
              </div>
            </div>
            <div className="flex justify-end gap-4">
              <Button variant="outline">Cancel</Button>
              <Button>Create Lesson</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search lessons..."
          className="pl-9"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {currentLessons.map((lesson) => (
          <Card key={lesson.id} className="overflow-hidden group">
            <div className="relative h-48 overflow-hidden -mx-6 -mt-6">
              <img
                src={lesson.thumbnail}
                alt={lesson.title}
                className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
              />
              <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            </div>
            <CardHeader>
              <CardTitle>{lesson.title}</CardTitle>
              <CardDescription>{lesson.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>Progress</span>
                  <span>{lesson.progress}%</span>
                </div>
                <Progress value={lesson.progress} className="h-2" />
                <p className="text-sm text-muted-foreground">
                  Duration: {lesson.duration}
                </p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-2 mt-8">
          <Button
            variant="outline"
            size="icon"
            onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <div className="flex items-center gap-1">
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
              <Button
                key={page}
                variant={currentPage === page ? "default" : "outline"}
                size="sm"
                onClick={() => setCurrentPage(page)}
                className="w-8 h-8"
              >
                {page}
              </Button>
            ))}
          </div>
          <Button
            variant="outline"
            size="icon"
            onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
            disabled={currentPage === totalPages}
          >
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      )}
    </div>
  );
} 