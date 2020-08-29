from rest_framework import generics, mixins, permissions
from rest_framework.generics import get_object_or_404

from ..models import *
from .serializers import *
from .permissions import *


# using concrete view classes
class EbookListCreateAPIView(generics.ListCreateAPIView):
    # select relevant dataset
    queryset = Ebook.objects.all()
    # serialize data to json
    serializer_class = EbookSerializer

    # add authentication to endpoint
    permission_classes = [IsAdminOrReadOnly]


class EbookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ebook.objects.all()
    serializer_class = EbookSerializer
    permission_classes = [IsAdminOrReadOnly]


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # create review for select ebook
    def perform_create(self, serializer):
        # select relevant ebook pk
        ebook_pk = self.kwargs.get('ebook_pk')
        # select relevant ebook using that pk
        ebook = get_object_or_404(Ebook, pk=ebook_pk)
        # serialise json back to python object and save
        serializer.save(ebook=ebook)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

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
