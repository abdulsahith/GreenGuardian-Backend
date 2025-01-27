from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.sessions.models import Session
from .models import MachinePyro,MachineBsfl,Admingreen,Usergreen
from .serializers import Pyro_serial,bsfl_serial,admin_serial,user_serial
import uuid
from django.core.cache import cache
from rest_framework import status

@api_view(['GET', 'POST'])
def Pyro(request):
    if request.method == 'GET':
        record_id=request.session.get('pyromachineid')
        data = MachinePyro.objects.filter(machineid=record_id)
        serializer = Pyro_serial(data, many=True)
        return Response(serializer.data)
 
      
    elif request.method == 'POST':
        record_id = request.session.get('machineid')
        if not record_id:
            return Response({'error': 'Record ID not provided'}, status=400)

        try:
             
            instance = MachinePyro.objects.get(machineid=record_id)
            pyroadd=Usergreen.objects.get(machineid=record_id)
            new_pyro_value = pyroadd.pyroweigh
            if new_pyro_value:
                instance.addpyro += int(new_pyro_value)
            serializer = Pyro_serial(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Successfully saved!'}, status=200)
            return Response(serializer.errors, status=400)
        except MachinePyro.DoesNotExist:
            return Response({'error': 'Record not found'}, status=404)
        


@api_view(['GET', 'POST'])
def Bsfl(request):
    if request.method == 'GET':
        
        record_id=request.session.get('bsflmachineid')
        data = MachineBsfl.objects.filter(machineid=record_id)
        serializer = bsfl_serial(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
    
        record_id =request.session.get('machineid')
        if not record_id:
            return Response({'error': 'Record ID not provided'}, status=400)
        
        try:
             
            instance = MachineBsfl.objects.get(machineid=record_id)

            bsfladd=Usergreen.objects.get(Bsmachineid=record_id)
            new_bsfl_value = bsfladd.bsflweight
            if new_bsfl_value:
                instance.addbsfl += int(new_bsfl_value)
            serializer = bsfl_serial(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Successfully saved!'}, status=200)
            return Response(serializer.errors, status=400)
        except MachineBsfl.DoesNotExist:
            return Response({'error': 'Record not found'}, status=404)

@api_view(['POST'])
def Admin(request):
    adname = request.data.get('adname')
    password = request.data.get('password')
    
    try:
        admin = Admingreen.objects.get(adname=adname, password=password)
        
        request.session['adname'] = admin.adname
        request.session['machineid'] = admin.machineid
       
        page=""
        if(request.session.get('machineid')=='TN001'):
            page='pyro'
        else:
            page='bsfl'
            

        return Response({
            'success': page,
            'message': 'Login successful!',
            'data': admin_serial(admin).data,
        })
    except Admingreen.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Invalid username or password',
        }, status=401)
    


@api_view(['POST'])
def user(request):
    username = request.data.get('username')
    password = request.data.get('password')
 
    try:
        # Validate the user
        user = Usergreen.objects.get(username=username, password=password)
        token = str(uuid.uuid4())
        request.session['user_token'] = token
        request.session['pyromachineid']=user.machineid
        request.session['bsflmachineid']=user.Bsmachineid
        request.session['username']=user.username

        return Response({
            'success': True,
            'token': token,
            'username':user.username,
            'message': 'Login successful!',
        })
    
    except Usergreen.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Invalid username or password',
        }, status=401)
        

@api_view(['GET', 'POST'])
def plastic_collect(request):
    record_id = request.session.get('pyromachineid')   #get the sessions user id

    if not record_id:
        return Response({'error': 'Machine ID not found in session'}, status=400)

    try:
         
        instance = Usergreen.objects.get(machineid=record_id)  #user instace for particular row
    except Usergreen.DoesNotExist:
        return Response({'error': 'Machine record not found'}, status=404)

    if request.method == "GET":  # display all the details 
         
        serializer = user_serial(instance)
        return Response(serializer.data)
    elif request.method == "POST": # get the details and post it to the database 
        userid = request.data.get('userid')
        weight = request.data.get('weight')

        if not userid or not weight:
            return Response({'error': 'userid and weight are required fields'}, status=400)

        try:
    
            user_instance = Usergreen.objects.get(username=userid)   
        except Usergreen.DoesNotExist:
            return Response({'error': f'User with ID {userid} not found'}, status=404)

        user_instance.pyroweigh = weight   # post the weight to database
        user_instance.save()

        return Response({'message': f'Successfully updated weight for user {userid}'}, status=200)



@api_view(['GET', 'POST'])
def bsfl_collect(request):
    record_id = request.data.get('username')   #get the sessions user id

    if not record_id:
        return Response({'error': 'Machine ID not found in session'}, status=400)

    try:
         
        instance = Usergreen.objects.get(Bsmachineid=record_id)  #user instace for particular row
    except Usergreen.DoesNotExist:
        return Response({'error': 'Machine record not found'}, status=404)

    if request.method == "GET":  # display all the details 
         
        serializer = user_serial(instance)
        return Response(serializer.data)
    
    elif request.method == "POST": # get the details and post it to the database 
        userid = request.data.get('userid')
        weight = request.data.get('weight')

        if not userid or not weight:
            return Response({'error': 'userid and weight are required fields'}, status=400)

        try:
    
            user_instance = Usergreen.objects.get(username=userid)   
        except Usergreen.DoesNotExist:
            return Response({'error': f'User with ID {userid} not found'}, status=404)

        user_instance.bsflweight = weight   # post the weight to database
        user_instance.save()

        return Response({'message': f'Successfully updated weight for user {userid}'}, status=200)


@api_view(['GET'])
def get_user_ids(request):
    user_ids = Usergreen.objects.values_list('username', flat=True)  
    return Response(list(user_ids))


@api_view(['GET'])
def get_Pyroweight(request):
    record_id=request.session.get('pyromachineid')
    data = Usergreen.objects.filter(machineid=record_id)
    serializer =user_serial(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_Bsflweight(request):
    record_id=request.session.get('bsflmachineid')
    data = Usergreen.objects.filter(Bsmachineid=record_id)
    serializer = user_serial(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_current_user(request):
    record_id=request.session.get('username')
    data = Usergreen.objects.filter(username=record_id)
    serializer = user_serial(data, many=True)
    return Response(serializer.data.username)


# @api_view(['POST'])
# def weight(request):   # for esp32 to send data to server
    
#     """
#     API to receive weight data from Arduino and save it to the database.
#     """
    
     

#    # machine_id = request.data.get('machine_id') 
#     weight = request.data.get('weight')
#     if not weight:
#         return Response({'error': ' weight are required'}, status=400)
#     try:
#         machine = MachinePyro.objects.get(machineid=machine_id)
#         machine.pyro = int(weight)
#         machine.save()

#         serializer = Pyro_serial(machine)
#         return Response({
#             'message': 'Weight data saved successfully!',
#             'updated_machine_data': serializer.data
#         }, status=200)

#     except MachinePyro.DoesNotExist:
#         return Response({'error': 'Machine not found for the given ID'}, status=404)
#     except Exception as e:
#         return Response({'error': str(e)}, status=500)



@api_view(['POST'])
def update_weight(request):
    """
    API to receive weight data from Arduino and temporarily store it.
    """
    weight = request.data.get('weight')

    if not weight:
        return Response({'error': 'Weight is required'}, status=400)

    try:
        # Store the weight in the cache (expires in 5 minutes)
        cache.set('latest_weight', int(weight), timeout=300)
        return Response({'message': 'Weight updated successfully!'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def scan_weight(request):
    """
    API for users to scan QR code and retrieve the latest weight.
    """
    
    username = request.session.get('username')
    scantype=request.data.get('type')
    print(username)
    if not username:
        return Response({'error': 'User not logged in. Please log in to scan the QR code.'}, status=403)
     
    try:
        # Fetch the latest weight from the cache
        latest_weight = cache.get('latest_weight')

        if latest_weight is None:
            return Response({'error': 'No weight data available. Please try again later.'}, status=404)

        # Update the user's table with the latest weight
        if(scantype=='Plastic'):
             user = Usergreen.objects.get(username=username)
             user.pyroweigh = latest_weight
             user.addpyroweight+=latest_weight*12
             
             user.save()
        else:
            user = Usergreen.objects.get(username=username)
            user.bsflweight = latest_weight 
            user.addbsflweight+=latest_weight*12
            user.save()
        user = Usergreen.objects.get(username=username)
        user.carbon = ((user.pyroweigh+user.bsflweight)/2)*6 - ((user.pyroweigh+user.bsflweight)/2)*1.8
        user.save()
         
        return Response({
            'message': 'Weight successfully assigned to your dashboard.',
            'username': user.username,
            'weight': user.pyroweigh
        }, status=200)
    except Usergreen.DoesNotExist:
        return Response({'error': 'User not found. Please contact support.'}, status=404)
    except Exception as e:
        # Log unexpected errors (optional: add logging here)
        return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

@api_view(['POST'])
def update_user_weight(request):
    """
    API to receive weight data and update the user's pyroweigh field in the database.
    """
    username = request.data.get('username')  # Get the username from the request body
    weight = request.data.get('weight')  # Get the weight value from the request body
    
    if not username:
        return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not weight:
        return Response({'error': 'Weight data is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Find the user by their username
        user = Usergreen.objects.get(username=username)
        
        # Update the user's pyroweigh field with the provided weight
        user.pyroweigh = int(weight)
        user.save()

        # Return a success response
        return Response({
            'message': f'Weight for user {username} updated successfully!',
            'username': user.username,
            'weight': user.pyroweigh
        }, status=status.HTTP_200_OK)
    
    except Usergreen.DoesNotExist:
        # If the user does not exist
        return Response({'error': 'User not found. Please check the username.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Handle other unexpected errorsw
        return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)