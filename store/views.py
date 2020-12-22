import csv
from django.db import connection
from rest_framework import status, viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from store.models import Sales
from store.serializers import SalesSerializer


class SalesViewSet(ModelViewSet):
    """ ViewSet для продаж """
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer

    def create(self, request, *args, **kwargs):
        try:
            cursor = connection.cursor()
            cursor.execute("TRUNCATE TABLE store_sales RESTART IDENTITY")
            file = request.GET.get('filename')
            with open(file, 'r', encoding='utf-8') as csvfile:
                deals_reader = csv.reader(csvfile, delimiter=',')
                next(deals_reader)

                for line in deals_reader:
                    Sales.objects.create(customer=line[0],
                                         item=line[1],
                                         total=float(line[2]),
                                         quantity=line[3],
                                         date=line[4],
                                         )

            return Response({'Status': "ОК"}, status.HTTP_201_CREATED)

        except:
            return Response({'Status': 'Error', 'Desc': status.HTTP_400_BAD_REQUEST},
                            status.HTTP_400_BAD_REQUEST)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        all_customer = [k['customer'] for k in queryset.values()]

        customer_spent = []
        for customer in set(all_customer,):
            summ = 0
            for quer in queryset:
                if customer == quer.customer:
                    summ += quer.total
            customer_spent.append([customer, summ, []])
        customer_spent.sort(key=lambda i: i[1], reverse=True)

        each_customers_gems = []
        all_gems_set = []

        five_largest_spending = customer_spent[0:5]
        for customer in five_largest_spending:
            each_customers_gems.append(queryset.filter(customer=customer[0]).values('item').distinct())
            all_gems_set.extend(queryset.filter(customer=customer[0]).values('item').distinct())

        for i, gems in enumerate(each_customers_gems):
            for gem in gems:
                if all_gems_set.count(gem) > 1:
                    five_largest_spending[i][2].append(gem['item'])

        response_list = []
        for zz in five_largest_spending:
            response_list.append(dict(zip(['username', 'spent_money', 'gems'], zz)))

        return Response({'response': response_list}, status.HTTP_201_CREATED)






