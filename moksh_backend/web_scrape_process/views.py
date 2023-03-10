from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import json
from .stores.SephoraScrapper import SephoraScrapper
import multiprocessing
import time

# Create your views here.

def processURL(url):
    scrapperObject = SephoraScrapper()
    scrapperObject.openWindow(url)
    review = scrapperObject.getReviews()
    scrapperObject.closeWindow()

    return review


class GetInfoFromURL(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        body = json.loads(request.body)
        url = body["url"]
        productInfoDict, similarProductsList = [], []

        try:
            scrapperObject = SephoraScrapper()
            scrapperObject.openWindow(url)
            productInfoDict = scrapperObject.getProductInfo()
            similarProductsList = scrapperObject.getSimilarProducts()
            scrapperObject.closeWindow()
        except:
            scrapperObject.closeWindow()
            return Response(status=400, data={
                'message': 'Error in processing data.'
            })

        return Response({
            'productInfo': productInfoDict,
            'similarProducts': similarProductsList
        })

class GetReviewFromURLs(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        body = json.loads(request.body)
        urls = body["urls"]
        outputs = []

        try:
            pool = multiprocessing.Pool()
            pool = multiprocessing.Pool(processes=10)
            outputs = pool.map(processURL, urls)
        except:
            return Response(status=400, data={
                'message': 'Error in processing data.'
            })

        return Response({
            "reviewList": outputs
        })