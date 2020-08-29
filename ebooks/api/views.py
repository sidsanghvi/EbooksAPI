from rest_framework import generics, mixins, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from ..models import *
from .serializers import *
from .permissions import *
from .pagination import *


# using concrete view classes
class EbookListCreateAPIView(generics.ListCreateAPIView):
    # select relevant dataset
    # .order_by cuz unordered query set could lead to pagination inconsistency
    # '-id' to show latest entry first
    queryset = Ebook.objects.all().order_by('-id')
    # serialize data to json
    serializer_class = EbookSerializer

    # add authentication to endpoint
    permission_classes = [IsAdminOrReadOnly]

    # add pagination
    pagination_class = SmallSetPagination


class EbookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ebook.objects.all()
    serializer_class = EbookSerializer
    permission_classes = [IsAdminOrReadOnly]


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # create review for select ebook
    def perform_create(self, serializer):
        # select relevant ebook pk
        ebook_pk = self.kwargs.get('ebook_pk')
        # select relevant ebook using that pk
        ebook = get_object_or_404(Ebook, pk=ebook_pk)

        # select current user to be author
        review_author = self.request.user

        # check if user has already reviewed
        # query review set for review from this user
        review_queryset = Review.objects.filter(
            ebook=ebook, review_author=review_author)
        # raise error if review exists
        if review_queryset.exists():
            raise ValidationError('Book already reviewed')

        # serialise json back to python object and save with selected info
        serializer.save(ebook=ebook, review_author=review_author)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]

# # using genericAPIview and mixin ONLY
# class EbookListCreateAPIView(mixins.ListModelMixin,
#                              mixins.CreateModelMixin,
#                              generics.GenericAPIView):

#     queryset = Ebook.objects.all()
#     serializer_class = EbookSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
