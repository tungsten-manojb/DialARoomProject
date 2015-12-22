from CorpRoomApp.models import *
import json
from django.db.models import Q
import datetime
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import pdb 
from django.shortcuts import render_to_response

"""
This class defines all the common functionality related to properties.
These can be used all over the project.
__author__ = 'ManojB'
"""
ADMIN       = 0
CORPORATE   = 1
OWNER       = 2
RETAIL      = 3



class PropertyCommonFunctionality():
    
    def get_searched_property_details(self,**request_data):
        print 'I am in function'
        print 'RE DATA : ',request_data
        data = []
        filter_args={}
        try:
            if request_data:
                if request_data['city_name']:
                    filter_args['property_location__icontains'] = request_data['city_name']
            filter_args['property_availability_status']=True

            print datetime.datetime.now()
            #property_list = Property.objects.filter(Q(property_id__in = Property.objects.filter(**filter_args)))
            property_list = Property.objects.filter(**filter_args)
            property_rate =  999.00
            for property in property_list:
                try:
                    rates = PropertyRate.objects.get(property_id=property)
                    property_rate = rates.single_occupancy_display_rate
                except Exception as err:
                    print 'ERR',err
                pr = { 'property_id': property.property_id, 'property_name': property.property_display_name,
                    'property_address':property.property_location, 'property_desc' : property.property_description, 'property_rate': property_rate,
                    'property_rating' : property.star_category, 'airport_distance' : property.distance_from_airport,
                    'railway_stop_distance' : property.distance_from_railway_station, 'star': str(property.star_category*20)  }
                data.append(pr)
            print datetime.datetime.now()
        except Exception as e:
            print 'Search Properties - Exception : ',e
        return data

    '''
    This method returns a list of all locations.
    '''
    def get_all_location_list(self):
        data = []
        try:
            locations = Location.objects.all()
            data = [location.__unicode__() for location in locations]
        except Exception as e:
            print e
        return data

    def get_all_state_name(self):
        state_list=[]
        try:
            state_list = [state.get_state_info() for state in State.objects.all()]
        except Exception as err:
            print 'City Exception ', err
        return state_list

    def get_all_city_name(self):
        city_list=[]
        try:
            city_list = [city.get_city_info() for city in City.objects.all()]
        except Exception as err:
            print 'City Exception ', err
        return city_list

    def get_all_cities_based_on_state(self, state_nm):
        city_list=[]
        try:
            state = State.objects.get(state_name = state_nm)
            city_list = [city.get_city_info() for city in City.objects.filter(state_id=state)]
        except Exception as err:
            print 'City Exception ', err
        return city_list

    def get_all_location_based_on_city(self, city_nm):
        print 'City Name', city_nm
        area_list =[]
        try:
            print 'Retrieving list of locations based on city'
            city = City.objects.get(city_name=city_nm)
            area_list = [location.get_location_info() for location in Location.objects.filter(city_id=city)]
        except Exception as err:
            print 'Exception ',err
        return area_list
            
        

def authenticate_system_user(request):
    """
    This api validate to the system user and its type and redirect to its
    respective users dashboard.
    """
    #pdb.set_trace()
    if request.user.is_authenticated():
        customer = Customer.objects.get(id=request.user.id)
        if customer.user_type == ADMIN:
            return redirect('/business/dashboard/')
        elif customer.user_type == CORPORATE:
            return redirect('/corporate/dashboard/')
        elif customer.user_type == OWNER:
            return redirect('/vendor/')
        else:
            return render_to_response('login.html')
    else:
        return render_to_response('login.html')

def store_user_track(request, tag):
    '''
    This method is used for tracking each activity of corporate user/vendor/ admin user
    '''
    v_path = '{ "path": "'+ request.path + '", "time" : "'+ datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') +'", "tag": "'+ tag +'"}'
    
    try:
        user_session = UserTrackingActivity.objects.get(user_id=request.session['user_id'], session_id= request.session._session_key)
        user_session.path = user_session.path + '$' + v_path
        #user_session.aggregate_time = user_session.session_out_time - user_session.session_in_time
        user_session.save()
    except UserTrackingActivity.DoesNotExist as err:
        user_session = UserTrackingActivity.objects.create(
            user_id=request.session['user_id'],
            session_id= request.session._session_key,
            session_in_time = datetime.datetime.now(),
            path = v_path
        )
        user_session.save()
    except KeyError as e:
        print 'common_functionality.py | store_user_track | KeyError ', e
        #return render_to_response('505.html')
        return redirect('/corporate/')
    return True

def user_track_sign_out(request):
    try:
        user_session = UserTrackingActivity.objects.get(user_id=request.session['user_id'], session_id= request.session._session_key)
        time_delta = datetime.datetime.now() - user_session.session_in_time
        user_session.aggregate_time = time_delta / 3600.00
        user_session.save()
    except UserTrackingActivity.DoesNotExist as err:
        print 'common_functionality.py | user_track_sign_out | DoesNotExist ', err
    except KeyError as e:
        print 'common_functionality.py | user_track_sign_out | KeyError ', e
        return render_to_response('505.html')
    except Exception as err:
        print 'common_functionality.py | user_track_sign_out | Exception ', err
    return True
