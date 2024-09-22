from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.blog.models import Blog, Category, Comments
from apps.blog.serializers import BlogSerializer, CategorySerializer, CommentSerializer
from apps.common.permissions import ReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BlogListView(GenericAPIView):
    serializer_class = BlogSerializer
    permission_classes = (ReadOnly,)

    def get(self, request: Request) -> Response:
        blogs = Blog.objects.all()
        return Response(self.get_serializer(blogs, many=True).data)


class BlogItemView(GenericAPIView):
    serializer_class = BlogSerializer
    permission_classes = (ReadOnly, IsAuthenticated)

    def get(self, request: Request, pk: int) -> Response:
        blog: Blog = get_object_or_404(Blog.objects.all(), pk=pk)
        return Response(self.get_serializer(blog).data)


class BlogCreateView(GenericAPIView):
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        # Validate data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Create the blog post
        blog = Blog.objects.create(**validated_data)

        return Response(self.serializer_class(blog).data)


class CreateCommentView(GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        # Validate data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract data from request
        blog_id = serializer.validated_data.get("blog").id
        text = serializer.validated_data.get("text")

        # get blog post
        blog = get_object_or_404(Blog, id=blog_id)

        # create comment
        comment = Comments.objects.create(blog=blog, text=text)

        # Return comment
        return Response(self.get_serializer(comment).data)
