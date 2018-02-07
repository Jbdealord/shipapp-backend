#Author: Debojit Kaushik ( 11th April 2017 )

'''Django Imports'''
from django.db.models import Q

'''Rest Framework Imports'''
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, api_view
from rest_framework.authentication import TokenAuthentication

'''Misc Imports'''
from common import api_response, error_codes

'''Model Imports'''
from departments.models import Department
from issues.models import Issue, Solution, Image

'''Serializer Imports'''
from .serializers import IssueSerializer, IssueSerializerFields, SolutionSerializer, ImageSerializer, SolutionSerializerFields

import traceback


class IssueHandler(APIView):
    '''
        Resource endpoint (Class Based View) for CRUD requests related to Issues.
        Methods: 
            GET, 
            POST, 
            PUT, 
            DELETE
    '''

    #GET endpoint.
    def get(self, request):
        try:   
            assert 'page_no' in request.GET
            p_no = int(request.GET.get("page_no"))
            
            filters = Q(deleted = False) 
            filterKeys = list(request.GET.keys())
            assert filterKeys
            
            avail_filters = ['ship', 'status', 'priority', 'reported_by','deparment']
            #Dynamic list for filters.
            for key in filterKeys:
                if key in avail_filters:
                    filters &= Q(**{key : request.GET[key]})
                else:
                    pass
            
            data_set = Issue.objects.filter(filters).order_by('-updated_time')[p_no*10:(p_no*10)+10]
            if data_set.exists():
                serialized_data_set = IssueSerializerFields(data_set, many = True)                    
                return api_response(
                    True, 
                    status = error_codes._OK, 
                    data = serialized_data_set.data
                )
            else: 
                return api_response(
                    True, 
                    status = error_codes._OK, 
                    data = []
                )
        except AssertionError as e:
            return api_response(
                success = False,
                status = error_codes._BAD_PARAM,
                error = error_codes._ASSERTION_ERROR
            )
        except Department.DoesNotExist:
            return api_response(
                success = False,
                status = error_codes._BAD_PARAM,
                error = error_codes._NOT_FOUND_ERROR
            )
        except Exception as e:
            print(e)
            return api_response(
                success = False,
                status = error_codes._SERVER_ERROR,
                error = error_codes._EXCEPTION_ERROR
            )
        
    #POST endpoint.
    def post(self, request):
        try:
            request.data['issue']['recorded_by'] = request.user.user_id
            created_issue = IssueSerializer(
                data = request.data['issue']
            )
            if created_issue.is_valid():
                created_issue.save()
                return api_response(
                    success = True, 
                    status = error_codes._OK,
                    data = created_issue.data
                )
            else:
                return api_response(
                    success = False,
                    status = error_codes._BAD_PARAM,
                    error = created_issue.errors
                )
        except AssertionError:
            return api_response(
                success = False,
                status = error_codes._BAD_PARAM,
                error = error_codes._ASSERTION_ERROR
            )
        except Exception as e:
            print(e)
            return api_response(
                success = False,
                status = error_codes._SERVER_ERROR,
                error = error_codes._EXCEPTION_ERROR
            )

    #PUT endpoint.
    def put(self, request):
        try:
            assert 'id' in request.data

            editable_issue = Issue.objects.get(iss_id = request.data['id'])

            assert 'images' in request.data
            if editable_issue.recorded_by.user_id == request.user.user_id:
                created_issue = IssueSerializer(
                    editable_issue,
                    data = request.data['issue']
                )
                if created_issue.is_valid():
                    created_issue.save()
                    return api_response(
                        success = True, 
                        status = error_codes._OK,
                        data = created_issue.data
                    )
                else:
                    return api_response(
                        success = False,
                        status = error_codes._BAD_PARAM,
                        error = created_issue.errors
                    )
            else:
                return api_response(
                    success = False,
                    status = error_codes._UNAUTHORISED,
                    data = []
                )
        except AssertionError as e:
            return api_response(
                success = False,
                status = error_codes._BAD_PARAM,
                error = error_codes._ASSERTION_ERROR
            )
        except Issue.DoesNotExist:
            return api_response(
                success = False,
                status = error_codes._BAD_PARAM,
                error = error_codes._NOT_FOUND_ERROR
            )
        except Exception as e:
            print(e)
            return api_response(
                success = False,
                status = error_codes._SERVER_ERROR,
                error = error_codes._EXCEPTION_ERROR
            )

    #Delete Endpoint for issues.
    def delete(self, request):
        try:
            assert 'id' in request.data
            issue_id = request.data['id']
            try:
                data = Issue.objects.get(iss_id = issue_id)
                assert data.deleted is False

                if data.recorded_by == request.user or request.user.is_staff:
                    data.deleted = True
                    data.save()
                    return api_response(
                        success = True,
                        status = error_codes._OK,
                        data = []
                    )
                else:
                    return api_response(
                        success = False,
                        status = error_codes._UNAUTHORISED,
                        data = "User is not authorised to delete this post."
                    )
            except Issue.DoesNotExist:
                return api_response(
                    success = False,
                    status = error_codes._NOT_FOUND,
                    error = error_codes._NOT_FOUND_ERROR
                )
            except AssertionError:
                return api_response(
                    success = False,
                    status = error_codes._NOT_FOUND,
                    error = error_codes._NOT_FOUND_ERROR
                )
        except AssertionError:
            return api_response(
                success = False,
                status = error_codes._BAD_PARAM,
                error = error_codes._ASSERTION_ERROR
            )
        except Exception as e:
            print(e)
            return api_response(
                success = False,
                status = error_codes._SERVER_ERROR,
                error = error_codes._EXCEPTION_ERROR
            )



class SolutionHandler(APIView):
    '''
        Resource endpoint (Class Based View) for CRUD requests related to Solutions.
        Methods: 
            GET, 
            POST, 
            PUT, 
            DELETE
    '''
    #GET endpoint.
    def get(self, request):
        try:   
            assert 'page_no' and 'id' in request.GET
            p_no = int(request.GET.get("page_no"))
            issue = Issue.objects.get(iss_id = request.GET.get('id'))
            assert issue
            
            data_set = Solution.objects.filter(parent_issue = issue, deleted = False).order_by('-updated_time')[p_no*10:(p_no*10)+10]
            if data_set.exists():
                serialized_data_set = SolutionSerializer(data_set, many = True)
                return api_response(
                    True, 
                    status = error_codes._OK, 
                    data = serialized_data_set.data
                )
            else: 
                return api_response(
                    success = True, 
                    status = error_codes._OK, 
                    data = []
                )
        except AssertionError as e:
            return api_response(
                success = False,
                status = error_codes._BAD_PARAM,
                error = error_codes._ASSERTION_ERROR
            )
        except Issue.DoesNotExist:
            return api_response(
                success = False,
                status = error_codes._BAD_PARAM,
                error = error_codes._NOT_FOUND_ERROR
            )
        except Exception as e:
            print(e)
            return api_response(
                success = False,
                status = error_codes._SERVER_ERROR,
                error = error_codes._EXCEPTION_ERROR
            )
        
    #POST endpoint.
    def post(self, request):
        try:
            request.data['solution']['poster'] = request.user.user_id
            created_solution = SolutionSerializerFields(
                data = request.data['solution']
            )
            if created_solution.is_valid():
                created_solution.save()
                try:
                    parent_issue = Issue.objects.get(iss_id = request.data['solution']['parent_issue'])
                    if parent_issue.status == 'pending' or parent_issue.status == 'unassigned':
                        parent_issue.status = 'submitted'
                        parent_issue.save()
                    else:
                        pass
                    return api_response(
                        success = True, 
                        status = error_codes._OK,
                        data = created_solution.data
                    )
                except Exception as e:
                    return api_response(
                        success = False, 
                        status = error_codes._SERVER_ERROR,
                        error = error_codes._EXCEPTION_ERROR
                    )
            else:
                return api_response(
                    success = False,
                    status = error_codes._BAD_PARAM,
                    error = created_solution.errors
                )
        except AssertionError:
            return api_response(
                success = False,
                status = error_codes._BAD_PARAM,
                error = error_codes._ASSERTION_ERROR
            )
        except Exception as e:
            print(e)
            return api_response(
                success = False,
                status = error_codes._SERVER_ERROR,
                error = error_codes._EXCEPTION_ERROR
            )

    #PUT endpoint.
    def put(self, request):
        try:
            assert 'id' in request.data

            editable_solution = Solution.objects.get(sol_id = request.data['id'])
            if editable_solution.poster == request.user:
                created_solution = SolutionSerializerFields(
                    editable_solution,
                    data = request.data['solution']
                )
                if created_solution.is_valid():
                    created_solution.save()
                    return api_response(
                        success = True, 
                        status = error_codes._OK,
                        data = created_solution.data
                    )
                else:
                    return api_response(
                        success = False,
                        status = error_codes._BAD_PARAM,
                        error = created_solution.errors
                    )
            else:
                return api_response(
                    success = False,
                    status = error_codes._UNAUTHORISED,
                    error = error_codes._UNAUTHORISED_ERROR
                )
        except AssertionError as e:
            print(e)
            return api_response(
                success = False,
                status = error_codes._BAD_PARAM,
                error = error_codes._ASSERTION_ERROR
            )
        except Exception as e:
            return api_response(
                success = False,
                status = error_codes._SERVER_ERROR,
                error = error_codes._EXCEPTION_ERROR
            )

    #Delete Endpoint for issues.
    def delete(self, request):
        try:
            assert 'id' in request.data
            solution_id = request.data['id']
            try:
                data = Solution.objects.get(sol_id = solution_id)
                assert data.deleted is False

                if data.poster == request.user:
                    data.deleted = True
                    data.save()
                    return api_response(
                        success = True,
                        status = error_codes._OK,
                        data = []
                    )
                else:
                    return api_response(
                        success = False,
                        status = error_codes._UNAUTHORISED,
                        data = "You are ont permitted to perform this action."
                    )
            except Solution.DoesNotExist:
                return api_response(
                    success = False,
                    status = error_codes._NOT_FOUND,
                    error = error_codes._NOT_FOUND_ERROR
                )
            except AssertionError:
                return api_response(
                    success = False,
                    status = error_codes._NOT_FOUND,
                    error = error_codes._NOT_FOUND_ERROR
                )
        except AssertionError:
            return api_response(
                success = False,
                status = error_codes._BAD_PARAM,
                error = error_codes._ASSERTION_ERROR
            )
        except Exception as e:
            print(e)
            return api_response(
                success = False,
                status = error_codes._SERVER_ERROR,
                error = error_codes._EXCEPTION_ERROR
            )


#Signing Off endpoint.
@api_view(['POST'])
def SignOff(request):
    try:
        assert 'solution_id' and 'issue_id' in request.data
        assert request.FILES

        issue = Issue.objects.get(iss_id = request.data['issue_id'])
        solution = Solution.objects.get(sol_id = request.data['solution_id'])
        if issue.status == 'submitted' or issue.status == 'pending' or issue.status == 'unassigned':
            if request.FILES:
                for i, img in enumerate(request.FILES):
                    temp = Image.objects.create(
                            parent_issue = issue,
                            parent_solution = solution,
                            image = request.FILES[img],
                            signature_of = issue
                        )
                    temp.save()
                    if i>1:
                        break
                    
            if request.user == issue.ship.owner:
                try:
                    assert not issue.resolved_by
                    sol = Solution.objects.get(sol_id = request.data['solution_id'])
                    issue.resolved_by = sol.poster
                    issue.status = 'resolved'
                    issue.save()

                    serialized_data = IssueSerializerFields(
                        issue
                    )   

                    return api_response(
                        success = True,
                        status = error_codes._OK,
                        data = serialized_data.data
                    )
                except AssertionError:
                    return api_response(
                        success = False,
                        status = error_codes._BAD_PARAM,
                        error = "This issue has already been signed off."
                    )
            else:
                return api_response(
                    success =False,
                    status = error_codes._UNAUTHORISED,
                    error = error_codes._UNAUTHORISED_ERROR
                )
        else:
            return api_response(
                success = False,
                status = error_codes._NOT_FOUND,
                error = "There is no solution to be signed off."
            )
    except AssertionError:
        return api_response(
            success = False,
            status = error_codes._BAD_PARAM,
            error = error_codes._ASSERTION_ERROR
        )
    except (Issue.DoesNotExist, Solution.DoesNotExist) as e:
        return api_response(
            success = False,
            status = error_codes._NOT_FOUND,
            error = error_codes._NOT_FOUND_ERROR
        )
    except Exception as e:
        print(e)
        return api_response(
            success = False,
            status = error_codes._SERVER_ERROR,
            error = error_codes._EXCEPTION_ERROR
        )



'''
	Image upload endpoint.
'''
@api_view(['POST'])
def UploadImages(request):
    try:
        assert 'id' and 'model' in request.data
        assert request.FILES

        if request.data['model'] == 'issue':
            try:
                assert Issue.objects.get(iss_id = request.data['id'])
                iss = Issue.objects.get(iss_id = request.data['id'])
                image = []
                for it , img in enumerate(request.FILES):
                    temp = Image.objects.create(
                        parent_issue = iss,
                        image = request.FILES[img]
                    )
                    temp.save()
                    image.append(temp)
                
                serialized_image = ImageSerializer(image, many = True)

                return api_response(
                    success = True,
                    status = error_codes._OK,
                    data = serialized_image.data    
                )
            except AssertionError:
                return api_response(
                    success = False, 
                    status = error_codes._NOT_FOUND,
                    error = error_codes._NOT_FOUND_ERROR
                )
            except Issue.DoesNotExist:
                return api_response(
                    success = False, 
                    status = error_codes._NOT_FOUND,
                    error = error_codes._NOT_FOUND_ERROR
                )
        elif request.data['model'] == 'solution':
            try:
                assert Solution.objects.get(sol_id = request.data['id'])
                sol = Solution.objects.get(sol_id = request.data['id'])
                image = []
                for it, img in enumerate(request.FILES):
                    temp = Image.objects.create(
                        parent_solution = sol,
                        image = request.FILES[img]
                    )
                    temp.save()
                    image.append(temp)

                    serialized_image = ImageSerializer(image, many = True)

                return api_response(
                    success = True,
                    status = error_codes._OK,
                    data = serialized_image.data
                )
            except AssertionError:
                return api_response(
                    success = False, 
                    status = error_codes._NOT_FOUND,
                    error = error_codes._NOT_FOUND_ERROR
                )
            except Solution.DoesNotExist:
                return api_response(
                    success = False, 
                    status = error_codes._NOT_FOUND,
                    error = error_codes._NOT_FOUND_ERROR
                )
    except AssertionError as e:
        print(e)
        return api_response(
            success = False,
            status = error_codes._BAD_PARAM,
            error = error_codes._ASSERTION_ERROR
        )
    except Exception as e:
        print(e)
        return api_response(
            success = True,
            status = error_codes._SERVER_ERROR,
            error = error_codes._EXCEPTION_ERROR
        )
