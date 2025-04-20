"use client";

import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { format } from "date-fns";
import { Loader2, Reply, MoreVertical } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";

// Mock data - replace with actual API calls
const mockComments = [
  {
    id: "1",
    content: "This was a really helpful lesson! I especially liked the explanation of useState.",
    author: {
      id: "user1",
      name: "Jane Cooper",
      avatar: "https://i.pravatar.cc/150?img=1",
    },
    createdAt: new Date(2023, 5, 15, 10, 30),
    replies: [
      {
        id: "reply1",
        content: "I agree! The useState explanation was very clear.",
        author: {
          id: "user2",
          name: "Alex Johnson",
          avatar: "https://i.pravatar.cc/150?img=2",
        },
        createdAt: new Date(2023, 5, 15, 11, 45),
      }
    ]
  },
  {
    id: "2",
    content: "Could you explain the useEffect dependency array in more detail?",
    author: {
      id: "user3",
      name: "Robert Fox",
      avatar: "https://i.pravatar.cc/150?img=3",
    },
    createdAt: new Date(2023, 5, 16, 9, 15),
    replies: []
  }
];

const formSchema = z.object({
  content: z.string().min(1, "Comment cannot be empty"),
});

interface CommentSectionProps {
  lessonId: string;
}

export default function CommentSection({ lessonId }: CommentSectionProps) {
  const [comments, setComments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [replyingTo, setReplyingTo] = useState<string | null>(null);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      content: "",
    },
  });

  const replyForm = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      content: "",
    },
  });

  useEffect(() => {
    // Fetch comments from API
    // For now, using mock data
    setTimeout(() => {
      setComments(mockComments);
      setLoading(false);
    }, 1000);
  }, [lessonId]);

  const onSubmit = (values: z.infer<typeof formSchema>) => {
    // Add new comment
    const newComment = {
      id: `comment-${Date.now()}`,
      content: values.content,
      author: {
        id: "currentUser",
        name: "Current User",
        avatar: "https://i.pravatar.cc/150?img=8",
      },
      createdAt: new Date(),
      replies: [],
    };

    setComments([newComment, ...comments]);
    form.reset();
  };

  const onReplySubmit = (values: z.infer<typeof formSchema>) => {
    if (!replyingTo) return;

    // Add new reply
    const newReply = {
      id: `reply-${Date.now()}`,
      content: values.content,
      author: {
        id: "currentUser",
        name: "Current User",
        avatar: "https://i.pravatar.cc/150?img=8",
      },
      createdAt: new Date(),
    };

    const updatedComments = comments.map(comment => {
      if (comment.id === replyingTo) {
        return {
          ...comment,
          replies: [...comment.replies, newReply],
        };
      }
      return comment;
    });

    setComments(updatedComments);
    replyForm.reset();
    setReplyingTo(null);
  };

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <Loader2 className="h-6 w-6 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Comment form */}
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          <FormField
            control={form.control}
            name="content"
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <Textarea
                    placeholder="Add a comment..."
                    className="min-h-[100px]"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <div className="flex justify-end">
            <Button type="submit" disabled={form.formState.isSubmitting}>
              {form.formState.isSubmitting ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Posting...
                </>
              ) : (
                "Post Comment"
              )}
            </Button>
          </div>
        </form>
      </Form>

      {/* Comments list */}
      <div className="space-y-6">
        {comments.length === 0 ? (
          <p className="text-center text-muted-foreground py-8">
            No comments yet. Be the first to comment!
          </p>
        ) : (
          comments.map((comment) => (
            <div key={comment.id} className="space-y-4">
              <div className="bg-card rounded-lg p-4 shadow-sm">
                <div className="flex justify-between items-start mb-2">
                  <div className="flex items-center space-x-2">
                    <Avatar>
                      <AvatarImage src={comment.author.avatar} alt={comment.author.name} />
                      <AvatarFallback>{comment.author.name.charAt(0)}</AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="font-medium">{comment.author.name}</p>
                      <p className="text-xs text-muted-foreground">
                        {format(new Date(comment.createdAt), "MMM d, yyyy 'at' h:mm a")}
                      </p>
                    </div>
                  </div>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon">
                        <MoreVertical className="h-4 w-4" />
                        <span className="sr-only">More</span>
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem>Report</DropdownMenuItem>
                      {comment.author.id === "currentUser" && (
                        <>
                          <DropdownMenuItem>Edit</DropdownMenuItem>
                          <DropdownMenuItem>Delete</DropdownMenuItem>
                        </>
                      )}
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
                <p className="text-sm">{comment.content}</p>
                <div className="mt-2 flex justify-end">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setReplyingTo(comment.id)}
                  >
                    <Reply className="mr-1 h-3 w-3" />
                    Reply
                  </Button>
                </div>
              </div>

              {/* Reply form */}
              {replyingTo === comment.id && (
                <div className="ml-8">
                  <Form {...replyForm}>
                    <form onSubmit={replyForm.handleSubmit(onReplySubmit)} className="space-y-4">
                      <FormField
                        control={replyForm.control}
                        name="content"
                        render={({ field }) => (
                          <FormItem>
                            <FormControl>
                              <Textarea
                                placeholder={`Reply to ${comment.author.name}...`}
                                className="min-h-[80px]"
                                {...field}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <div className="flex justify-end space-x-2">
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          onClick={() => setReplyingTo(null)}
                        >
                          Cancel
                        </Button>
                        <Button
                          type="submit"
                          size="sm"
                          disabled={replyForm.formState.isSubmitting}
                        >
                          {replyForm.formState.isSubmitting ? (
                            <>
                              <Loader2 className="mr-2 h-3 w-3 animate-spin" />
                              Posting...
                            </>
                          ) : (
                            "Post Reply"
                          )}
                        </Button>
                      </div>
                    </form>
                  </Form>
                </div>
              )}

              {/* Replies */}
              {comment.replies.length > 0 && (
                <div className="ml-8 space-y-4">
                  {comment.replies.map((reply: any) => (
                    <div key={reply.id} className="bg-card rounded-lg p-4 shadow-sm">
                      <div className="flex justify-between items-start mb-2">
                        <div className="flex items-center space-x-2">
                          <Avatar>
                            <AvatarImage src={reply.author.avatar} alt={reply.author.name} />
                            <AvatarFallback>{reply.author.name.charAt(0)}</AvatarFallback>
                          </Avatar>
                          <div>
                            <p className="font-medium">{reply.author.name}</p>
                            <p className="text-xs text-muted-foreground">
                              {format(new Date(reply.createdAt), "MMM d, yyyy 'at' h:mm a")}
                            </p>
                          </div>
                        </div>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="icon">
                              <MoreVertical className="h-4 w-4" />
                              <span className="sr-only">More</span>
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem>Report</DropdownMenuItem>
                            {reply.author.id === "currentUser" && (
                              <>
                                <DropdownMenuItem>Edit</DropdownMenuItem>
                                <DropdownMenuItem>Delete</DropdownMenuItem>
                              </>
                            )}
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </div>
                      <p className="text-sm">{reply.content}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
