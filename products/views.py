import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from products.models import Category, SubCategory, Product


class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        result = [
            {
                'category_id'    : category.id, 
                'name'           : category.name,
                'products_count' : category.subcategory_set.filter(
                    product__sub_category__in = category.subcategory_set.all()).count(),
                'sub_categories' : [
                    {
                        'id'             : sub_category.id,
                        'name'           : sub_category.name,
                        'products_count' : sub_category.product_set.all().count() 
                    } for sub_category in category.subcategory_set.all()
                ] 
            } for category in categories
        ]

        return JsonResponse({'result' : result}, status = 200)

class ProductListView(View):
    def get(self, request):
        try:
            if request.GET.get('category_id'):
                category_id = request.GET['category_id']
                q           = Q(product__category_id = category_id)

            if request.GET.get('sub_category_id'):
                category_id = request.GET['sub_category_id']
                q           = Q(product__sub_category_id = category_id)

            result = { 
                'category' : None,
                'products' : [
                    {
                        'id'               : product.id,
                        'name'             : product.name,
                        'tag'              : product.tag,
                        'is_new'           : product.is_new,
                        'is_vegan'         : product.is_vegan,
                        'is_only_online'   : product.is_only_online,
                        'is_made_in_korea' : product.is_made_in_korea,
                        'is_sold_out'      : not product.item_set.exclude(stock__exact = 0).exists(),
                        'price'            : int(product.item_set.order_by('price')[0].price), 
                        'image_url'        : [image.url for image in product.imgaeurl_set.all()]
                } for product in Product.objects.filter(q)],
            }
            category = Category.objects.get(q)
            category_information = {
                'id'        : category.id,
                'content'   : category.content,
                'image_url' : category.image_url,
            }

            result['category'] = category_information
                
            return JsonResponse({'result' : result}, status = 200) 


            # if request.GET.get('category_id'):
            # category_id = request.GET['category_id']
            # products    = Product.objects.filter(sub_category__category_id = category_id)
            
            # q = Q()
            # if category_id:
            #     q =
            #     category = Category.objects.get(id=category_id)
            # if sub_category:
            #     q = 
            #     category = SubCategory.objects.get(id=sub_category_id) 
            
            
            # sub_category_id = request.GET['sub_category_id']
            # sub_category    = SubCategory.objects.get(id = sub_category_id)
            # products        = sub_category.product_set.all()
            
            # result = {
            #     'sub_cateogry_id' : sub_category.id,
            #     'content'         : sub_category.content,
            #     'image_url'       : sub_category.image_url, 
            #     'products'        : [
            #         {
            #             'id'               : product.id,
            #             'name'             : product.name,
            #             'tag'              : product.tag,
            #             'is_new'           : product.is_new,
            #             'is_vegan'         : product.is_vegan,
            #             'is_only_online'   : product.is_only_online,
            #             'is_made_in_korea' : product.is_made_in_korea,
            #             'is_sold_out'      : not product.item_set.exclude(stock__exact = 0).exists(),
            #             'price'            : int(product.item_set.order_by('price')[0].price), 
            #             'image_url'        : [image.url for image in product.imgaeurl_set.all()]
            #         } for product in products],
            #     }    

            return JsonResponse({'result' : result}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)

        except SubCategory.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Category'}, status = 400)

class ProductView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id = product_id)

            result = {
                'product_id' : product_id,
                'name'       : product.name,
                'tag'        : product.tag,
                'image'      : [url for url in product.imgaeurl_set.all()],
                'manual'     : product.manual,
                'content'    : product.content,
                'components' : [
                    {
                        'id'        : component.id,
                        'name'      : component.name,
                        'important' : component.productcomponent_set.get(product_id = product_id).important
                    } for component in product.component.all()
                ],
                'items' : [
                    {
                        'id'     : item.id,
                        'size_g' : item.size.size_g,
                        'price'  : int(item.price),
                        'stock'  : item.stock,
                        'image'  : item.image_url
                    }for item in product.item_set.order_by('size__size_g')
                ] 
            }
            
            return JsonResponse({'result' : result}, status = 200)
        
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Product'}, status = 400)