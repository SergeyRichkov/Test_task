import csv
from django.db import connection
from django.http import HttpResponse
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from store.models import Sales
from store.serializers import SalesSerializer


class SalesViewSet(ModelViewSet):
    """ ViewSet для продаж """

    queryset = Sales.objects.all()
    serializer_class = SalesSerializer




    def create(self, request):
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE store_sales RESTART IDENTITY")
        file = request.GET.get('filename')
        with open(file, 'r', encoding='utf-8') as csvfile:
            deals_reader = csv.reader(csvfile, delimiter=',')
            next(deals_reader)

            for line in deals_reader:
                Sales.objects.create(customer=line[0], item=line[1],
                                     total=float(line[2]),
                                     quantity=line[3],
                                     date=line[4],
                                     )
        print('Kavabanga!!')
        return Response('hgvjghv')

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     # print(serializer.data)
    #     return Response({'response': '' }, status.HTTP_205_RESET_CONTENT)
    #
    #
    def list(self, request, *args, **kwargs):
        kk = []
        pp = []
        summ = 0
        queryset = self.filter_queryset(self.get_queryset())
        customer_queryset = queryset.distinct('customer')
        serializer = self.get_serializer(queryset, many=True)
        serializer1 = self.get_serializer(customer_queryset, many=True)

        for k in serializer1.data:
            kk.append(k['customer'])
        for customer in kk:
            for quer in queryset:
                if customer == quer.customer:
                    summ += quer.total
            pp.append([customer, summ])
        pp.sort(key=lambda i: i[1], reverse=True)
        print(pp[0:5])
        gg = []
        kamni = []
        hhhhh = pp[0:5]
        for cus in hhhhh:
            gg.append(queryset.filter(customer=cus[0]).values('item').distinct())
            kamni.extend(queryset.filter(customer=cus[0]).values('item').distinct())

        for i, qq in enumerate(gg):
            for qqq in qq:
                if kamni.count(qqq) > 1:
                    hhhhh[i].append(qqq['item'])

        return Response(hhhhh, status.HTTP_205_RESET_CONTENT)





