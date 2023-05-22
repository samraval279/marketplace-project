import json
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, parsers, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.mail import send_mail
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from MPbackend.global_resposne import ResponseInfo
from account.models import *
from account.serializers import *
from account.permissions import *
from account.filters import *
# Create your views here.
def myindex(request):
    return HttpResponse("AO backend server is running")

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [UserPermission]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = UserSerializer
    http_method_names = ['get','post','put','delete']

    action_serializers = {
        'login':LoginSerializer,
        'create':UserCreateSerializer,
        'retrieve':UserGetSerializer,
        'get_current_user':UserGetSerializer,
        'forgot_password':ForgotPasswordSerializer,
        'reset_password':ResetPasswordSerializer,
        'change_password':ChangePasswordSerializer
    }


    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)

    def get_authenticated_user(self):
        user = get_object_or_404(self.queryset, pk=self.request.user.pk)
        self.check_object_permissions(self.request, user)
        return user

    def list(self, request):

        response = super(UserViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    
    def retrieve(self, request, pk):

        response = super(UserViewset, self).retrieve(request,pk=pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def create(self, request):
        super(UserViewset, self).create(request)

        res = ResponseInfo({}, "User successfully added", True, 200)
        return Response(res.custom_success_payload())


    def update(self, request, pk):

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        res = ResponseInfo({}, "User successfully updated", True, 200)
        return Response(res.custom_success_payload())


    def destroy(self, request, pk ):

        super(UserViewset, self).destroy(request,pk=pk)

        res = ResponseInfo({}, "User successfully deleted", True, 200)
        return Response(res.custom_success_payload())

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny,])
    def login(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):       
            res=ResponseInfo(serializer.data,'Logged In', True, 200)
            return Response(res.custom_success_payload())

    @action(methods=['get'], detail=False,permission_classes=[permissions.IsAuthenticated,])
    def get_current_user(self, request, pk=None):
        """
        get logged in user
        """
        serializer = self.get_serializer(self.get_authenticated_user())
        # prepare response
        res = ResponseInfo(serializer.data, "Sucess", True, 200)
        return Response(res.custom_success_payload())
    
    @action(methods=['post'],detail=False,permission_classes=[permissions.AllowAny])
    def forgot_password(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            send_mail(
                from_email="bhagyesh@samcomtechnobrains.com",
                message=f"your reset password code is:{serializer.data['code']}",
                subject="Reset Password Code",
                recipient_list= [serializer.data['email']]
                )
            res = ResponseInfo({},"code sent to your email",True,200)
            return Response(res.custom_success_payload())
        
        except Exception as e :
            raise e 
    
    @action(methods=["post"], detail=False, permission_classes=[permissions.AllowAny])
    def reset_password(self, request, pk=None):
        """
        reset password
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            code = serializer.data.get("code")
            password = serializer.data.get("password")
            invite = ForgotPasswordInvite.objects.filter(code=code, email=email).first()
            if invite:
                user = User.objects.filter(email=invite.email).first()

                if user is not None:
                    user.set_password(password)
                    user.save()
                    refresh = RefreshToken.for_user(user)
                    # prepare response
                    res = ResponseInfo(
                        {
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        },
                        "Password changed",
                        True,
                        200,
                    )
                    ForgotPasswordInvite.objects.filter(code=code, email=email).delete()
                    return Response(res.custom_success_payload())
            res = ResponseInfo({}, "user_not_found", False, 400)
            return Response(res.custom_success_payload())

    @action(methods=['post'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def change_password(self ,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")
            user = authenticate(email=email,password=old_password)
            if user is not None:
                user.set_password(new_password)
                user.save()
                refresh = RefreshToken.for_user(user)
                # prepare response
                res = ResponseInfo(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    "Password changed",
                    True,
                    200,
                )
                return Response(res.custom_success_payload())
            res = ResponseInfo({}, "user_not_found", False, 400)
            return Response(res.custom_success_payload()) 
        

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [CategoryPermissions]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = CategorySerializer
    http_method_names = ['get','post','delete']
    lookup_field='name'

    action_serializers = {
        'all_categories':CategoryAllSerializer,
        'create':CategoryCreateSerializer,
        'update':CategoryCreateSerializer,
    }

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)

    def list(self, request):

        response = super(CategoryViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    
    def retrieve(self, request, name):

        response = super(CategoryViewset, self).retrieve(request,name=name)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def create(self, request):
        super(CategoryViewset, self).create(request)

        res = ResponseInfo({}, "category successfully added", True, 200)
        return Response(res.custom_success_payload())


    # def update(self, request, name):

    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     res = ResponseInfo({}, "category successfully updated", True, 200)
    #     return Response(res.custom_success_payload())


    def destroy(self, request, pk):

        super(CategoryViewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "Category successfully deleted", True, 200)
        return Response(res.custom_success_payload())
    
    @action(methods=['get'],detail=False,permission_classes=[permissions.AllowAny])
    def all_categories(self, request):

        serializer = self.get_serializer()
        res = ResponseInfo(serializer.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [CategoryPermissions]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    http_method_names = ['get','post','put','delete']
    # lookup_field='name'

    filterset_class = ProductFilters
    search_fields = ['brand','product_name','category__label',]
    ordering_fields = ['publish_price', 'created_at',]

    # filterset_fields = ['price','publish_price__gte']

    action_serializers = {
        'retrieve':ProductRetrieveSerializer,
        'create':ProductCreateSerializer,
        'update':ProductUpdateSerializer,
        'recommendations':RecommendationSerializer,
        'add_preference':AddPreferenceSerializer    
        }

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)

    def get_queryset(self):
        qs = self.queryset.filter(status=True)
        ordering = self.request.query_params.get('sort_by', None)
        if ordering:
            if ordering == 'popularity':
                qs = qs.order_by('product_cart')

            elif ordering == 'price_low':
                qs = qs.order_by('publish_price')

            elif ordering == 'price_high':
                qs = qs.order_by('-publish_price')

            elif ordering == 'newest':
                qs = qs.order_by('-created_date')

            elif ordering == 'alphabetical_az':
                qs = qs.order_by('product_name')

            elif ordering == 'alphabetical_za':
                qs = qs.order_by('-product_name')
        return qs
        # qs = self.queryset.filter(status=True)
        # return qs
    

    def list(self, request):

        response = super(ProductViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    
    def retrieve(self, request, pk):

        response = super(ProductViewset, self).retrieve(request,pk=pk)
        # serializer = self.get_serializer()

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def create(self, request):
        attribute = request.data.pop('attribute')
        request.data['attribute'] = json.loads(attribute[0])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        res = ResponseInfo({}, "Product added successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def update(self, request, pk):

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        res = ResponseInfo({},"Product updated successfully",True, 200)
        return Response(res.custom_success_payload())
    
    def destroy(self, request, pk):

        super(ProductViewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "Product successfully deleted", True, 200)
        return Response(res.custom_success_payload())
    

    @action(methods=['get'], detail=False, permission_classes=[permissions.AllowAny,])
    def get_brand_names(self, request, pk=None):
        """
        get brand names
        """
        # serializer = self.get_serializer()
        # serializer.is_valid(raise_exception=True)
        name = self.request.query_params.get("category")
        category = Category.objects.get(name=name)
        sub_categories = category.get_children_and_self()
        products = self.queryset.filter(category__in=sub_categories)
        brands = products.values_list('brand',flat=1).distinct()

        # prepare response
        res = ResponseInfo(brands, "Sucess", True, 200)
        return Response(res.custom_success_payload())
    
    @action(methods=['GET'],detail=False,permission_classes=[permissions.AllowAny])
    def get_all_attributes(self, request):
        # attribute_names = ProductAttribute.objects.values_list("name",flat=True).distinct()
        data = {}
        name = self.request.query_params.get("category")
        category = Category.objects.get(name=name)
        sub_categories = category.get_children_and_self()
        products = self.queryset.filter(category__in=sub_categories)
        attributes = ProductAttribute.objects.filter(product__in=products).all()
        for attr in attributes:    
            data[attr.name] = attributes.filter(name=attr.name).values_list('value',flat=True).distinct()
        
        res = ResponseInfo(data, "Sucess", True, 200)
        return Response(res.custom_success_payload())
        
    @action(methods=['GET'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def recommendations(self, request):

        serializer = self.get_serializer(request.data)

        res = ResponseInfo(serializer.data, "Success", True, 200)
        return Response(res.custom_success_payload())

    @action(methods=['POST'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def add_preference(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = ResponseInfo({}, "product added into preference successfully", True, 200)
        return Response(res.custom_success_payload())

class ImageViewset(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    permission_classes = [CategoryPermissions]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = ImageSerializer
    http_method_names = ['post','delete']


    # def list(self, request):

    #     response = super(ImageViewset, self).list(request)

    #     res = ResponseInfo(response.data, "success", True, 200)
    #     return Response(res.custom_success_payload())
    
    # def retrieve(self, request, pk):

    #     response = super(ImageViewset, self).retrieve(request,pk=pk)

    #     res = ResponseInfo(response.data, "success", True, 200)
    #     return Response(res.custom_success_payload())

    def create(self, request):

        super(ImageViewset, self).create(request)

        res = ResponseInfo({}, "Image added successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def destroy(self, request, pk):

        super(ImageViewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "Image successfully deleted", True, 200)
        return Response(res.custom_success_payload())
    


class SpecificationViewset(viewsets.ModelViewSet):
    queryset = ProductSpecification.objects.all()
    permission_classes = [CategoryPermissions]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = SpecificationSerializer
    http_method_names = ['get','post','put','delete']


    def list(self, request):

        response = super(SpecificationViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    
    def retrieve(self, request, pk):

        response = super(SpecificationViewset, self).retrieve(request,pk=pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def create(self, request):

        super(SpecificationViewset, self).create(request)

        res = ResponseInfo({}, "Specification added successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def update(self, request, pk):

        # response = super(SpecificationViewset, self).partial_update(request,pk=pk)
        obj = self.get_object()
        serializer = self.get_serializer(obj, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        res = ResponseInfo(serializer.data, "Specification updated successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def destroy(self, request, pk):

        super(SpecificationViewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "specification successfully deleted", True, 200)
        return Response(res.custom_success_payload())
    

class SizechartViewset(viewsets.ModelViewSet):
    queryset = ProductDimension.objects.all()
    permission_classes = [CategoryPermissions]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = SizechartSerializer
    http_method_names = ['get','post','put','delete']


    def list(self, request):

        response = super(SizechartViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    
    def retrieve(self, request, pk):

        response = super(SizechartViewset, self).retrieve(request,pk=pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())

    def create(self, request):

        super(SizechartViewset, self).create(request)

        res = ResponseInfo({}, "Size Chart added successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def update(self, request, pk):

        # response = super(SizechartViewset, self).partial_update(request,pk=pk)
        obj = self.get_object()
        serializer = self.get_serializer(obj, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        res = ResponseInfo(serializer.data, "Size Chart updated successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def destroy(self, request, pk):

        super(SizechartViewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "Size Chart successfully deleted", True, 200)
        return Response(res.custom_success_payload())
    

class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    permission_classes = [CategoryPermissions]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = ReviewSerializer
    http_method_names = ['post','put','delete']

    action_serializers = {
            "create":ReviewCreateSerializer
    }
    
    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)

    def create(self, request):  
        super(ReviewViewset, self).create(request)

        res = ResponseInfo({}, "Review added successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def update(self, request, pk):

        # response = super(ReviewViewset, self).partial_update(request,pk=pk)
        obj = self.get_object()
        serializer = self.get_serializer(obj,request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        res = ResponseInfo(serializer.data, "Review updated successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def destroy(self, request, pk):

        super(ReviewViewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "Review successfully deleted", True, 200)
        return Response(res.custom_success_payload())
    

class ServiceRequestViewset(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all()
    permission_classes = [ServiceRequestPermissions]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = ServiceRequestSerializer
    http_method_names = ['get','post','delete']

    def list(self, request):
        response = super(ServiceRequestViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

    def retrieve(self, request, pk):
        response = super(ServiceRequestViewset, self).retrieve(request , pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

    def create(self, request):
        super(ServiceRequestViewset, self).create(request)

        res = ResponseInfo({}, "request sent successfully", True, 200)
        return Response(res.custom_success_payload())
    

    def destroy(self, request, pk):
        super(ServiceRequestViewset, self).destroy(request, pk=pk)

        res = ResponseInfo({}, "request deleted successfully", True, 200)
        return Response(res.custom_success_payload())
    



class CartViewset(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = CartSerializer
    http_method_names = ['get','post','put','delete']

    action_serializers = {
            "create":CartCreateSerializer
    }
    
    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)
    
    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user, is_visible=True)
        return qs
    
    def list(self, request):
        response = super(CartViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

    def retrieve(self, request, pk):
        response = super(CartViewset, self).retrieve(request , pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

    def create(self, request):
        super(CartViewset, self).create(request)

        res = ResponseInfo({}, "product added successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def update(self, request, pk):

        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        res = ResponseInfo(serializer.data, "product updated successfully", True, 200)
        return Response(res.custom_success_payload())

    def destroy(self, request, pk):
        super(CartViewset, self).destroy(request, pk=pk)

        res = ResponseInfo({}, "product removed successfully", True, 200)
        return Response(res.custom_success_payload())
    


class FavViewset(viewsets.ModelViewSet):
    queryset = Favourite.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = FavSerializer
    http_method_names = ['get','post','delete']

    action_serializers = {
            "create":FavCreateSerializer
    }
    
    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)
    
    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user)
        return qs
    
    def list(self, request):
        response = super(FavViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

    def retrieve(self, request, pk):
        response = super(FavViewset, self).retrieve(request , pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

    def create(self, request):
        super(FavViewset, self).create(request)

        res = ResponseInfo({}, "product added successfully", True, 200)
        return Response(res.custom_success_payload())
    

    def destroy(self, request, pk):
        super(FavViewset, self).destroy(request, pk=pk)

        res = ResponseInfo({}, "product removed successfully", True, 200)
        return Response(res.custom_success_payload())
    

class AddressViewset(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = AddressSerializer
    http_method_names = ['get','post','put','delete']

    action_serializers = {
            "create":AddressCreateSerializer
    }
    
    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)
    
    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user)
        return qs
    
    def list(self, request):
        response = super(AddressViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

    def retrieve(self, request, pk):
        response = super(AddressViewset, self).retrieve(request , pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

    def create(self, request):
        super(AddressViewset, self).create(request)

        res = ResponseInfo({}, "address added successfully", True, 200)
        return Response(res.custom_success_payload())
    

    def update(self, request, pk):

        obj = self.get_object()
        serializer = self.serializer_class(obj, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        res = ResponseInfo({}, "address updated successfully", True, 200)
        return Response(res.custom_success_payload())
    

    def destroy(self, request, pk):
        super(AddressViewset, self).destroy(request, pk=pk)

        res = ResponseInfo({}, "address removed successfully", True, 200)
        return Response(res.custom_success_payload())
    


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = OrderSerializer
    http_method_names = ['get','post']

    action_serializers = {
            "create":OrderCreateSerializer,
            "list":OrderListSerializer,
            "verify_payment":VerifyPaymentSerializer
    }
    
    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)
    

    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user)
        return qs

    def list(self, request):
        response = super(OrderViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

    def retrieve(self, request, pk):
        response = super(OrderViewset, self).retrieve(request , pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

    def create(self, request):
        payment = super(OrderViewset, self).create(request)

        res = ResponseInfo(payment.data, "Order added successfully", True, 200)
        return Response(res.custom_success_payload())    

    @action(methods=['POST'],detail=False,permission_classes=[permissions.IsAuthenticated])
    def verify_payment(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        razorpay_client = razorpay.Client(auth=('YOUR_RAZORPAY_API_KEY', 'YOUR_RAZORPAY_API_SECRET'))
        try:
            order = Order.objects.get(id=serializer.validated_data.order_id)
            result = razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': serializer.validated_data.razorpay_order_id, 
                'razorpay_payment_id': serializer.validated_data.razorpay_payment_id, 
                'razorpay_signature': serializer.validated_data.razorpay_signature
                })
            order.order_amount=result['amount']
            order.order_payment_id = serializer.validated_data.razorpay_payment_id
            order.order_payment_status = 'succeeded'
            order.save()
            return Response({'message': 'Payment successful'})
        except Exception as e:
            return Response({'message': 'Payment failed', 'error': str(e)})
        
class GlobleSizeViewset(viewsets.ModelViewSet):
    queryset = GlobleSize.objects.all()
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = GlobleSizeSerializer
    http_method_names = ['get','post','put','delete']


    def list(self, request):
        response = super(GlobleSizeViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

    def retrieve(self, request, pk):
        response = super(GlobleSizeViewset, self).retrieve(request,pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    
    
    def create(self, request):
        response = super(GlobleSizeViewset, self).create(request)

        res = ResponseInfo({},'size added successfully', True, 200)
        return Response(res.custom_success_payload())
    
    def update(self, request, pk):

        obj = self.get_object()
        serializer = self.get_serializer(obj, request.data, partial=True)
        serializer.save()

        res = ResponseInfo(serializer.data, 'size updated successfully', True, 200)
        return Response(res.custom_success_payload())

    def destroy(self, request, pk):

        super(GlobleSizeViewset, self).destroy(request, pk)

        res = ResponseInfo({}, 'size deleted successfully', True, 200)
        return Response(res.custom_success_payload())
    
class SiteReviwViewset(viewsets.ModelViewSet):
    queryset = SiteReview.objects.all()
    permission_classes = [CategoryPermissions]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = SiteReviewSerializer
    http_method_names = ['post','get','put','delete']

    action_serializers = {
            "create":SiteReviewCreateSerializer
    }
    
    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)
    
    def list(self, request):
        response = super(SiteReviwViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    
    def retrieve(self, request, pk):
        response = super(SiteReviwViewset, self).retrieve(request,pk=pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

    def create(self, request):  
        super(SiteReviwViewset, self).create(request)

        res = ResponseInfo({}, "Review added successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def update(self, request, pk):

        # response = super(ReviewViewset, self).partial_update(request,pk=pk)
        obj = self.get_object()
        serializer = self.get_serializer(obj,request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        res = ResponseInfo(serializer.data, "Review updated successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def destroy(self, request, pk):

        super(SiteReviwViewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "Review successfully deleted", True, 200)
        return Response(res.custom_success_payload())
    
'''
newsletter/alerts/subscription viewset
'''

class AlertViewset(viewsets.ModelViewSet):
    queryset = Alerts.objects.all()
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = AlertSerializer
    http_method_names = ['post','get','delete']

    action_serializers = {
            "create":AlertCreateSerializer
    }
    
    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)
    
    def list(self, request):
        response = super(AlertViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    
    def retrieve(self, request, pk):
        response = super(AlertViewset, self).retrieve(request,pk=pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

    def create(self, request):  
        super(AlertViewset, self).create(request)

        res = ResponseInfo({}, "Alert added successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def destroy(self, request, pk):

        super(AlertViewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "Alert deleted successfully", True, 200)
        return Response(res.custom_success_payload())
    
'''
coupon code 
'''
class CouponViewset(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    permission_classes = [CategoryPermissions]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = CouponSerializer
    http_method_names = ['post','get','put','delete']

    action_serializers = {
        'create':CouponCreateSerializer,
        'apply_coupon':ApplyCouponSerializer
    }

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)

    def list(self, request):
        response = super(CouponViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    
    def retrieve(self, request, pk):
        response = super(CouponViewset, self).retrieve(request,pk=pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    
    def create(self, request):  
        super(CouponViewset, self).create(request)

        res = ResponseInfo({}, "Coupon added successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def update(self, request, pk):
        obj =self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        res = ResponseInfo(serializer.data, "Coupon updated successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def destroy(self, request, pk):

        super(CouponViewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "Coupon deleted successfully", True, 200)
        return Response(res.custom_success_payload())
    
    @action(methods=['POST'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def apply_coupon(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        res = ResponseInfo(serializer.data,"coupon successfully applied", False, 200)
        return Response(res.custom_success_payload())
    
'''
offer apis
'''
class OfferViewset(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    permission_classes = [CategoryPermissions]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    serializer_class = OfferSerializer
    http_method_names = ['post', 'get', 'put', 'delete']

    action_serializers = {
            "create":OfferCreateSerializer,
            "retrieve":OfferGetSerializer
            }
    
    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)
    
    def get_queryset(self):
        qs = self.queryset.filter(active=True)
        return qs
    
    def list(self, request):
        response = super(OfferViewset, self).list(request)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    
    def retrieve(self, request, pk):
        response = super(OfferViewset, self).retrieve(request,pk=pk)

        res = ResponseInfo(response.data, "success", True, 200)
        return Response(res.custom_success_payload())
    

    def create(self, request):  
        super(OfferViewset, self).create(request)

        res = ResponseInfo({}, "offer added successfully", True, 200)
        return Response(res.custom_success_payload())

    def update(self, request, pk):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        res = ResponseInfo({}, "offer updated successfully", True, 200)
        return Response(res.custom_success_payload())
    
    def destroy(self, request, pk):

        super(OfferViewset,self).destroy(request, pk=pk)

        res = ResponseInfo({}, "offer deleted successfully", True, 200)
        return Response(res.custom_success_payload())